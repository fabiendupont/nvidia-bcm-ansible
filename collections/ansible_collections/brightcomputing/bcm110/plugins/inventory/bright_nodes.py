from __future__ import annotations

from ipaddress import ip_interface
import json
import re
from ssl import SSLCertVerificationError

from ansible.errors import AnsibleError
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable, Cacheable

from pythoncm import entity
from pythoncm.cluster import Cluster
from pythoncm.settings import Settings

from ansible_collections.brightcomputing.bcm110.plugins.module_utils.utils import json_encode_entity


DOCUMENTATION = r"""
    module: bright_nodes
    description: Get ansible inventory from cmdaemon
    version_added: "9.2.0"
    requirements: [cmdaemon-pythoncm]
    author:
    - iiiteam <iiiteam@brightcomputing.com>
    extends_documentation_fragment:
        - constructed
        - inventory_cache
    options:
        plugin:
            choices: ['brightcomputing.bcm110.bright_nodes']
            description: Token that ensures this is a source file for the bright_nodes plugin.
            required: true
            type: str
        head_node:
            description:
            - Hostname of the head node.
            - Required if ansible is not being run on the head node.
            type: str
        port:
            default: 8081
            description: Port the cmdaemon service is listening on.
            type: int
        cert_file:
            description:
            - Path to the cmdaemon service client certificate file.
            - Required if ansible is not being run on the head node.
            type: str
        key_file:
            description:
            - Path to the cmdaemon service client key file.
            - Required if ansible is not being run on the head node.
            type: str
        ca_file:
            description:
            - Path to the cmdaemon service CA certificate file.
            - Required if ansible is not being run on the head node.
            type: str
        group_by:
            choices:
            - category
            - device_roles
            - device_type
            - kernel_version
            - nodegroup
            - network
            - partition
            - rack
            - software-image
            default: []
            description: Keys used to greate inventory groups.
            type: list
        interfaces:
            default: False
            description: If true, adds interface information to the host vars.
            type: boolean
        primary_network:
            description:
            - Sets the network name to be considered primary for all devices
            - If not set, the primary network will be the node's management network (if set), or that of the node's category, or that of the node's partition.
            type: str
"""


EXAMPLES = r"""
        # bright_inventory.yml file in YAML format
        # Example command line: ansible-inventory -v --list -i bright_inventory.yml

        plugin: brightcomputing.bcm110.bright_nodes

        group_by:
          - nodegroup
          - category

        compose:
          ansible_host: provisioning_interface.ip
"""


class InventoryModule(BaseInventoryPlugin, Constructable, Cacheable):
    NAME = "brightcomputing.bcm110.bright_nodes"

    def __init__(self):
        super().__init__()
        self.head_node = None
        self.port = 8081
        self.cert_file = None
        self.key_file = None
        self.ca_file = None

        self.use_cache = None
        self.interfaces = None
        self.group_by = None
        self.primary_network = None

        self.devices_list = {}
        self.node_group_list = {}

    def _get_primary_network(self, host):
        """
        Returns the primary network for the node.

        Primary network is determined, in order, by the primary_network option,
        the managementNetwork setting on the node, the managementNetwork
        setting on the node's category, or the managementNetwork setting
        on the node's partition.
        """
        if self.primary_network is None:
            return (
                host.managementNetwork if hasattr(host, 'managementNetwork')
                and host.managementNetwork is not None
                else host.category.managementNetwork
                if hasattr(host, 'category')
                and host.category.managementNetwork is not None
                else host.partition.managementNetwork
            )

        for interface in host.interfaces:
            if interface.network.name == self.primary_network:
                return interface.network

        return None

    def _set_host_variables(self, host, hostname):
        # IP Addresses
        primary_ip4, primary_ip6 = self.get_primary_ip(host)

        if primary_ip4:
            self.inventory.set_variable(hostname, 'ansible_host', primary_ip4)
            self.inventory.set_variable(hostname, 'primary_ip4', primary_ip4)

        if primary_ip6:
            self.inventory.set_variable(hostname, 'primary_ip6', primary_ip6)

        # Device roles
        self.inventory.set_variable(
            hostname,
            'device_roles',
            [role.name for role in host.roles]
        )

        # Services
        self.inventory.set_variable(
            hostname,
            'services',
            [{'name': service.name, 'run_if': service.runIf.name,
              'autostart': service.autostart} for service in host.services]
        )

        self.inventory.set_variable(
            hostname,
            'category',
            host.category.name if hasattr(host, 'category') else ''
        )

        software_image = self.get_software_image(host)
        self.inventory.set_variable(
            hostname,
            'software_image',
            {
                'name': software_image.name,
                'revision_id': software_image.revisionID,
                'revision': software_image.revision,
                'kernel_version': software_image.kernelVersion,
            } if software_image is not None else {}
        )

        self.inventory.set_variable(hostname, 'id', str(host.uuid))
        self.inventory.set_variable(hostname, 'userdefined1', host.userdefined1)
        self.inventory.set_variable(hostname, 'userdefined2', host.userdefined2)
        self.inventory.set_variable(hostname, 'pxelabel', host.pxelabel)
        self.inventory.set_variable(
            hostname,
            'use_exclusively_for',
            host.useExclusivelyFor
        )
        self.inventory.set_variable(
            hostname,
            'provisioning_interface',
            getattr(host.provisioningInterface, 'name', '')
        )
        self.inventory.set_variable(
            hostname,
            'rack',
            getattr(host.rack, 'name', '')
        )
        self.inventory.set_variable(
            hostname,
            'install_mode',
            getattr(host, 'installMode', '')
        )
        self.inventory.set_variable(
            hostname,
            'data_node',
            getattr(host, 'dataNode', '')
        )

        host_status = host.status()
        self.inventory.set_variable(
            hostname,
            'status',
            {
                'status': host_status.status.name,
                'reported_status': host_status.reportedStatus.name
            }
        )

        if self.interfaces:
            interfaces = [
                self._snakify_keys(json_encode_entity(interface))
                for interface in host.interfaces
            ]
            self.inventory.set_variable(hostname, 'interfaces', interfaces)

    def _snakify(self, string):
        name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", string)
        return re.sub("([a-z\\d])([A-Z])", r"\1_\2", name).lower()

    def _snakify_keys(self, camel_values):
        snake_values = {}
        for key, value in camel_values.items():
            snake_key = self._snakify(key)
            if isinstance(value, dict):
                snake_values[snake_key] = self._snakify_keys(value)
            else:
                snake_values[snake_key] = value

        return snake_values

    def create_groups(self, host, hostname):
        for group in self.group_by:
            try:
                host_groups = self.host_group_mappers[group](host)
            except KeyError:
                raise AnsibleError('group_by option %s in invalid.', group)

            if not host_groups or host_groups is None:
                continue

            if not isinstance(host_groups, list):
                host_groups = [host_groups]

            for host_group in host_groups:
                group_name = "_".join([group, host_group])
                if not group_name:
                    continue

                transformed_group_name = self.inventory.add_group(group=group_name)
                self.inventory.add_host(group=transformed_group_name, host=hostname)

    def fetch_hosts(self):
        if self.head_node is not None:
            settings = Settings(host=self.head_node,
                                port=self.port,
                                cert_file=self.cert_file,
                                key_file=self.key_file,
                                ca_file=self.ca_file)

            if not settings.check_certificate_files():
                raise AnsibleError("Unable to load certs")

            # The default generated server certificate has fewer bits than the
            # default check on Ubuntu allows. To work around that, check for
            # the exception and turn off ssl verification...
            try:
                cluster = Cluster(settings)
            except OSError as oserror:
                if (oserror.args and
                        isinstance(oserror.args[0], SSLCertVerificationError)):
                    settings.context.verify_mode = 0
                    cluster = Cluster(settings)
                else:
                    raise oserror
        else:
            cluster = Cluster()

        nodes = cluster.get_by_type(entity.Node)
        for node in nodes:
            self.devices_list[node.hostname] = node

        node_groups = cluster.get_by_type(entity.NodeGroup)
        for node_group in node_groups:
            name = node_group.name
            self.node_group_list[name] = {'nodes': []}

            for node in node_group.nodes:
                self.node_groups[name]['nodes'].append(node.hostname)

        cluster.disconnect()

    def get_group_category(self, host):
        if hasattr(host, 'category'):
            return getattr(host.category, 'name', None)

    def get_group_device_roles(self, host):
        return [role for role in host.roles]

    def get_group_device_type(self, host):
        return host.childType

    def get_group_kernel_version(self, host):
        if host.childType == "HeadNode":
            return None

        if host.kernelVersion:
            return host.kernelVersion

        image = self.get_software_image(host)
        if image is not None:
            return getattr(image, 'kernelVersion', None)

    def get_group_nodegroup(self, host):
        return [group for group in self.node_group_list
                if host.hostname in self.node_group_list[group]['nodes']]

    def get_group_network(self, host):
        return self._get_primary_network(host)

    def get_group_partition(self, host):
        return self.partition.name

    def get_group_rack(self, host):
        return getattr(host.rack, 'name', None)

    def get_group_software_image(self, host):
        image = self.get_software_image(host)
        return getattr(image, 'name', None)

    def get_primary_ip(self, host):
        primary_network = self._get_primary_network(host)

        for interface in host.interfaces:
            if interface.network.name == primary_network.name:
                ipv4 = (None if interface.ip == "0.0.0.0"
                        else str(ip_interface(interface.ip).ip))
                ipv6 = (None if interface.ipv6Ip == "::0"
                        else str(ip_interface(interface.ipv6Ip).ip))
                return ipv4, ipv6

        return None, None

    def get_software_image(self, host):
        try:
            return host.softwareImageProxy.parentSoftwareImage
        except AttributeError:
            try:
                return host.category.softwareImageProxy.parentSoftwareImage
            except AttributeError:
                return None

    @property
    def host_group_mappers(self):
        return {
            'category': self.get_group_category,
            'device_roles': self.get_group_device_roles,
            'device_type': self.get_group_device_type,
            'kernel_version': self.get_group_kernel_version,
            'nodegroup': self.get_group_nodegroup,
            'network': self.get_group_network,
            'partition': self.get_group_partition,
            'rack': self.get_group_rack,
            'software_image': self.get_group_software_image
        }

    def main(self):
        self.fetch_hosts()

        for hostname, host in self.devices_list.items():
            self.inventory.add_host(host=hostname)
            self._set_host_variables(host, hostname)

            strict = self.get_option('strict')
            host_as_json = json_encode_entity(host)
            self._set_composite_vars(
                self.get_option('compose'), host_as_json, hostname, strict=strict
            )

            # Complex groups based on jinja2 conditionals, hosts that meet the
            # conditional are added to group
            self._add_host_to_composed_groups(
                self.get_option("groups"), host_as_json, hostname, strict=strict
            )

            # Create groups based on variable values and add the
            # corresponding hosts
            # to it
            self._add_host_to_keyed_groups(
                self.get_option("keyed_groups"), host_as_json, hostname, strict=strict
            )

            self.create_groups(host, hostname)

    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path)
        self._read_config_data(path=path)
        self.use_cache = cache

        # Connection options
        self.head_node = self.get_option('head_node')
        if self.get_option('port') is not None:
            self.port = self.get_option('port')
        self.cert_file = self.get_option('cert_file')
        self.key_file = self.get_option('key_file')
        self.ca_file = self.get_option('ca_file')

        # Config options
        self.interfaces = self.get_option('interfaces')
        self.group_by = self.get_option('group_by')
        self.primary_network = self.get_option('primary_network')

        self.main()