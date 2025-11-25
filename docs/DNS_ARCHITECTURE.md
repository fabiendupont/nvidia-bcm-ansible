# DNS Architecture for OpenShift on BCM

## Problem Statement

OpenShift requires DNS resolution for internal cluster domains:
- `api.<cluster-name>.<domain>` - Kubernetes API endpoint
- `api-int.<cluster-name>.<domain>` - Internal API endpoint
- `*.apps.<cluster-name>.<domain>` - Application ingress wildcard

Public DNS servers (8.8.8.8, 1.1.1.1, etc.) cannot resolve these private cluster domains. The Agent-Based Installer validates DNS resolution during the pre-installation phase and **will not proceed** if these domains don't resolve.

## Solution: BCM Head Node as DNS Server

The BCM head node runs BIND (named) and provides DNS services for:
1. **BCM internal infrastructure** (existing zones)
2. **OpenShift clusters** (dynamically created zones)

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      BCM Head Node                           │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ BIND (named) - DNS Server                              │ │
│  │ - Listen: 10.141.255.254:53                           │ │
│  │                                                        │ │
│  │ Zones:                                                 │ │
│  │ ├── cm.cluster (BCM infrastructure)                   │ │
│  │ └── test.local (OpenShift cluster)                    │ │
│  │     ├── api.test-ocp.test.local      → 10.141.160.50 │ │
│  │     ├── api-int.test-ocp.test.local  → 10.141.160.50 │ │
│  │     ├── *.apps.test-ocp.test.local   → 10.141.160.50-52 │
│  │     ├── ocp-master-0.test-ocp.test.local → 10.141.160.50 │
│  │     ├── ocp-master-1.test-ocp.test.local → 10.141.160.51 │
│  │     └── ocp-master-2.test-ocp.test.local → 10.141.160.52 │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                           │
                           │ DNS queries (port 53)
                           ▼
┌───────────────────────────────────────────────────────────────┐
│                    OpenShift Nodes                            │
│  /etc/resolv.conf: nameserver 10.141.255.254                  │
│                                                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ ocp-master-0 │  │ ocp-master-1 │  │ ocp-master-2 │       │
│  │ 10.141.160.50│  │ 10.141.160.51│  │ 10.141.160.52│       │
│  │              │  │              │  │              │       │
│  │ assisted-    │  │              │  │              │       │
│  │ service:8090 │  │              │  │              │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│                                                                │
│  Agent-Based Installer validates:                             │
│  ✓ api.test-ocp.test.local resolves                          │
│  ✓ api-int.test-ocp.test.local resolves                      │
│  ✓ *.apps.test-ocp.test.local resolves                       │
└───────────────────────────────────────────────────────────────┘
```

## DNS Resolution Flow

1. **Node boots** via PXE from BCM
2. **CoreOS starts** with network configuration
3. **NetworkManager** sets DNS server to BCM head node (10.141.255.254)
4. **assisted-service** validates cluster requirements
5. **DNS validation** queries BCM head node for cluster domains
6. **BIND responds** with IP addresses from dynamically created zone
7. **Installation proceeds** once all validations pass

## Automated DNS Setup

The `dns_setup` role automatically:

### 1. Creates Zone File
```bash
/var/named/test.local.zone
```
Contains:
- NS record pointing to BCM head node
- A record for BCM head node
- API endpoint records (api, api-int)
- Apps wildcard records
- Node records

### 2. Updates BIND Configuration
```bash
/etc/named.conf.include
```
Adds zone definition:
```
zone "test.local" in {
  type master;
  file "test.local.zone";
};
```

### 3. Validates and Reloads
- Runs `named-checkconf` to validate configuration
- Runs `named-checkzone` to validate zone file
- Reloads `named` service to activate changes

### 4. Verifies Resolution
- Tests DNS resolution from BCM head node
- Optionally configures nodes to use BCM DNS

## Node DNS Configuration

Nodes must be configured to use the BCM head node as their DNS server.

### Current Implementation: Static in agent-config.yaml ✅

The `agent-config.yaml` template now includes DNS configuration pointing to BCM head node:

```yaml
dns-resolver:
  config:
    server:
      - {{ bcm_internal_ip | default('10.141.255.254') }}
```

**Default**: `10.141.255.254` (BCM head node internal IP)
**Override**: Set `openshift_dns_server` or `bcm_internal_ip` in inventory

### BCM DHCP Configuration (Already Configured)

BCM DHCP is already configured to provide the BCM head node as DNS:

```bash
# Check DHCP DNS configuration
cat /etc/dhcpd.conf | grep domain-name-servers
# Output: option domain-name-servers 10.141.255.254;
```

However, since OpenShift uses **static IP configuration** (`dhcp: false` in agent-config), the DHCP DNS setting is not used. The DNS server must be explicitly configured in the static network configuration.

### Manual Override (If Needed)

If nodes are already deployed with wrong DNS:
```bash
ssh core@ocp-master-0 \
  'sudo nmcli con mod enp1s0 ipv4.dns "10.141.255.254" && \
   sudo nmcli con up enp1s0'
```

## DNS Zone Structure

For cluster `test-ocp` in domain `test.local`:

```dns
$TTL 604800
@    IN  SOA     bcm11-headnode.test.local.  root.test.local. (
                  1        ; serial
                  86400    ; refresh
                  14400    ; retry
                  3628800  ; expire
                  604800 ) ; min TTL

     IN NS bcm11-headnode.test.local.

; Nameserver
bcm11-headnode           IN A 10.141.255.254

; API endpoints - rendezvous host
api.test-ocp             IN A 10.141.160.50
api-int.test-ocp         IN A 10.141.160.50

; Apps wildcard - all masters
*.apps.test-ocp          IN A 10.141.160.50
*.apps.test-ocp          IN A 10.141.160.51
*.apps.test-ocp          IN A 10.141.160.52

; Nodes
ocp-master-0.test-ocp    IN A 10.141.160.50
ocp-master-1.test-ocp    IN A 10.141.160.51
ocp-master-2.test-ocp    IN A 10.141.160.52
```

## Why Each Record is Needed

### `api.<cluster>.<domain>` → Rendezvous Host
- Kubernetes API server endpoint
- Used by `kubectl`, `oc`, and cluster components
- Points to rendezvous host (first master) during installation
- Later load-balanced across all API servers

### `api-int.<cluster>.<domain>` → Rendezvous Host
- Internal Kubernetes API endpoint
- Used for internal cluster communication
- Same IP as external API during initial installation

### `*.apps.<cluster>.<domain>` → All Masters
- Wildcard for application ingress routes
- Allows applications to be accessed via `<app-name>.apps.<cluster>.<domain>`
- Round-robin across all master nodes (they run ingress controllers)

### Node Records
- Direct node access via DNS name
- Helpful for troubleshooting and node-specific operations
- Format: `<node-name>.<cluster>.<domain>`

## Installation Validation Timeline

The Agent-Based Installer performs DNS validation:

1. **17:56:00** - Nodes boot, agent starts, DNS validation begins
2. **17:56:07** - DNS validation fails (using public DNS 8.8.8.8)
   ```
   Status: insufficient
   Validation: api-domain-name-resolved-correctly - FAILED
   ```
3. **17:58:15** - DNS configured on BCM, nodes updated to use BCM DNS
4. **17:58:17** - DNS validation passes
   ```
   Status: ready
   Message: Cluster ready to be installed
   ```
5. **17:58:21** - Installation begins
   ```
   Status: preparing-for-installation
   install_started_at: 2025-11-23T17:58:21.398Z
   ```

## Multiple Clusters

The BCM head node can serve DNS for multiple OpenShift clusters:

```
/var/named/
├── cm.cluster.zone          # BCM infrastructure
├── test.local.zone          # Cluster 1 (test-ocp)
├── prod.local.zone          # Cluster 2 (prod-ocp)
└── staging.local.zone       # Cluster 3 (staging-ocp)
```

Each cluster gets its own zone file with cluster-specific records.

## Troubleshooting

### DNS Not Resolving from Nodes

**Check resolv.conf:**
```bash
ssh core@ocp-master-0 'cat /etc/resolv.conf'
# Should show: nameserver 10.141.255.254
```

**Test resolution:**
```bash
ssh core@ocp-master-0 'dig +short api.test-ocp.test.local'
# Should return: 10.141.160.50
```

**Fix DNS configuration:**
```bash
ssh core@ocp-master-0 \
  'sudo nmcli con mod enp1s0 ipv4.dns "10.141.255.254" && \
   sudo nmcli con up enp1s0'
```

### BIND Not Responding

**Check named status:**
```bash
systemctl status named
```

**Check zone file:**
```bash
named-checkzone test.local /var/named/test.local.zone
```

**Check configuration:**
```bash
named-checkconf
```

**Restart named:**
```bash
systemctl restart named
```

### Installation Still Failing

**Check assisted-service logs:**
```bash
ssh core@ocp-master-0 \
  'sudo journalctl -u assisted-service -f | grep -i dns'
```

**Verify all DNS records:**
```bash
for record in api api-int "*.apps"; do
  echo -n "$record.test-ocp.test.local -> "
  dig +short @10.141.255.254 $record.test-ocp.test.local
done
```

## Future Enhancements

1. **DHCP Integration**: Configure BCM DHCP to automatically provide BCM head node as DNS
2. **agent-config.yaml DNS**: Include DNS configuration in generated agent-config
3. **External DNS Records**: Optionally create records in external DNS for cluster access from outside BCM network
4. **Load Balancer Integration**: Update API records to point to load balancer instead of single node

## References

- [OpenShift Agent-Based Installer DNS Requirements](https://docs.openshift.com/container-platform/4.20/installing/installing_with_agent_based_installer/preparing-to-install-with-agent-based-installer.html#agent-install-networking-config_preparing-to-install-with-agent-based-installer)
- [BIND Configuration Guide](https://bind9.readthedocs.io/)
- [BCM DNS Configuration](https://www.brightcomputing.com/documentation)
