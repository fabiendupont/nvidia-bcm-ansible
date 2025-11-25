#!/cm/local/apps/python3/bin/python
#
# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.
#
#
# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.
#

from __future__ import annotations


############################
# Docs
############################
DOCUMENTATION = r"""
---
module: rack_sensor
description: ['Manages rack_sensors']
options:
    state:
      type: str
      choices:
      - present
      - absent
      default: present
      description:
      - The state the resource should have
    cloneFrom:
      type: str
      default: ''
      description:
      - The id or name of the entity that the new entity will be cloned from.
      - ' (take effect only at entity creation)'
    hostname:
      description:
      - Hostname
      type: str
      required: true
    mac:
      description:
      - MAC address
      type: str
      required: false
      default: 00:00:00:00:00:00
    defaultGateway:
      description:
      - Default gateway for the device
      type: str
      required: false
      default: 0.0.0.0
    defaultGatewayMetric:
      description:
      - Default gateway metric
      type: int
      required: false
      default: 0
    partition:
      description:
      - Partition to which this device belongs
      type: str
      required: false
    switchPorts:
      description:
      - Switch ports
      type: list
      required: false
      default: []
      elements: dict
      options:
        networkSwitch:
          description:
          - Switch
          type: str
          required: false
        port:
          description:
          - Port number on the switch
          type: int
          required: false
          default: 0
        breakout:
          description:
          - Breakout port number on the switch
          type: int
          required: false
          default: -1
    powerDistributionUnits:
      description:
      - List of outlets on powerdistributionunits
      type: list
      required: false
      default: []
      elements: dict
      options:
        pdu:
          description:
          - Pointer to a power distribution unit
          type: str
          required: false
        port:
          description:
          - Port number on the power distribution unit
          type: int
          required: false
          default: 0
    rackPosition:
      description:
      - Name of the rack in which the device resides
      type: dict
      required: false
      options:
        rack:
          description:
          - Name of the rack in which the device resides
          type: str
          required: false
        position:
          description:
          - Position of the device in the rack, top is 1
          type: int
          required: false
          default: 1
        height:
          description:
          - Height of the device
          type: int
          required: false
          default: 1
        trayId:
          description:
          - ID
          type: str
          required: false
        trayName:
          description:
          - ID
          type: str
          required: false
    chassisPosition:
      description:
      - Chassis position in which the device resides
      type: dict
      required: false
      options:
        chassis:
          description:
          - Name of the chassis in which the device resides
          type: str
          required: false
        slot:
          description:
          - Slot of device inside the chassis
          type: str
          required: false
        position:
          description:
          - Position of the device in the chassis
          type: int
          required: false
          default: 1
        width:
          description:
          - Width of the device
          type: int
          required: false
          default: 1
    accessSettings:
      description:
      - Configure the cluster wide Access settings
      type: dict
      required: false
      options:
        username:
          description:
          - Username for ssh and/or REST API
          type: str
          required: false
        password:
          description:
          - Password for ssh and/or REST API
          type: str
          required: false
        rest_port:
          description:
          - Rest port, set to 0 to disable all REST calls
          type: int
          required: false
          default: 8765
        updateInZtp:
          description:
          - Update the switch password during ztp
          type: bool
          required: false
          default: false
        updateInNV:
          description:
          - Update the switch password using the automatically generated nv commands
          type: bool
          required: false
          default: false
    bmcSettings:
      description:
      - Configure the baseboard management controller settings
      type: dict
      required: false
      options:
        userName:
          description:
          - Username used to send BMC commands
          type: str
          required: false
        userID:
          description:
          - User ID to send BMC commands
          type: int
          required: false
          default: -1
        password:
          description:
          - Password used to send BMC commands
          type: str
          required: false
        powerResetDelay:
          description:
          - Delay used for BMC power reset, if set to > 0 power off; sleep X; power on
            is used
          type: int
          required: false
          default: 0
        extraArguments:
          description:
          - Extra arguments passed to BMC commands
          type: str
          required: false
        privilege:
          description:
          - Privilege given to the user
          type: str
          required: false
          default: ADMINISTRATOR
          choices:
          - CALLBACK
          - USER
          - OPERATOR
          - ADMINISTRATOR
          - OEM_PROPRIETARY
          - NO_ACCESS
        firmwareManageMode:
          description:
          - Firmware management mode for devices
          type: str
          required: false
          default: AUTO
          choices:
          - NONE
          - AUTO
          - ILO
          - H100
          - B200
          - GB200
          - GB200SW
          - B300
          - GB300
          - GB300SW
        leakPolicy:
          description:
          - Leak policy inside the BMC itself
          type: str
          required: false
          default: NONE
          choices:
          - NONE
          - ENABLED
          - DISABLED
        leakReactionDelay:
          description: []
          type: float
          required: false
          default: 0.0
    powerControl:
      description:
      - 'Specifies which type of power control feature is being used (values: none, apc,
        custom, cloud, ipmi0, ilo0, drac0, rf0, cimc0 or rshim0)'
      type: str
      required: false
      default: none
    customPowerScript:
      description:
      - Script that will be used to perform power on/off/reset/status operations
      type: str
      required: false
    customPowerScriptArgument:
      description:
      - Argument for the custom power script
      type: str
      required: false
    customPingScript:
      description:
      - Script that will be used to ping a device
      type: str
      required: false
    customPingScriptArgument:
      description:
      - Argument for the custom ping script
      type: str
      required: false
    notes:
      description:
      - Administrator notes
      type: str
      required: false
    provisioningInterface:
      description:
      - Network interface on which the node will receive software image updates
      type: str
      required: false
    managementNetwork:
      description:
      - Determines what network should be used for management traffic. If not set, category
        or partition setting is used.
      type: str
      required: false
    userdefined1:
      description:
      - A free text field passed to custom scripts
      type: str
      required: false
    userdefined2:
      description:
      - A free text field passed to custom scripts
      type: str
      required: false
    userDefinedResources:
      description:
      - User defined resources used to filter monitoring data producers
      type: list
      required: false
      default: []
    supportsGNSS:
      description:
      - Supports GNSS location
      type: bool
      required: false
      default: false
    partNumber:
      description:
      - Part number
      type: str
      required: false
    serialNumber:
      description:
      - Serial number
      type: str
      required: false
    prometheusMetricForwarders:
      description:
      - Prometheus metric forwarders
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - The name of the prometheus metric forwarder
          type: str
          required: true
        urls:
          description:
          - One or more URLs to try connect to
          type: list
          required: false
          default: []
        method:
          description:
          - HTTP method to use
          type: str
          required: false
          default: POST
          choices:
          - POST
          - GET
        timeout:
          description:
          - Http get timeout
          type: int
          required: false
          default: 5
        username:
          description:
          - Username used in http call
          type: str
          required: false
        password:
          description:
          - Password used in http call
          type: str
          required: false
        caPath:
          description:
          - CA certificate path
          type: str
          required: false
        privateKeyPath:
          description:
          - Private key path
          type: str
          required: false
        certificatePath:
          description:
          - Certificate path
          type: str
          required: false
    snmpSettings:
      description:
      - Configure the cluster wide SNMP settings
      type: dict
      required: false
      options:
        version:
          description:
          - Version of SNMP that should be use to read information from the device
          type: str
          required: false
          default: V2c
          choices:
          - V1
          - V2c
          - V3
          - File
        timeout:
          description:
          - SNMP timeout, set to 0 for default
          type: float
          required: false
          default: 0.0
        vlanTimeout:
          description:
          - SNMP timeout for VLAN calls, set to 0 for default
          type: float
          required: false
          default: 0.0
        retries:
          description:
          - SNMP retries, set to -1 for default
          type: int
          required: false
          default: -1
        readString:
          description:
          - SNMP read-only community string
          type: str
          required: false
          default: public
        writeString:
          description:
          - SNMP read-write community string
          type: str
          required: false
          default: private
        securityName:
          description:
          - SNMP v3 security name
          type: str
          required: false
        context:
          description:
          - SNMP v3 context
          type: str
          required: false
        authProtocol:
          description:
          - SNMP v3 authentication protocol
          type: str
          required: false
          default: MD5
          choices:
          - MD5
          - SHA
        privProtocol:
          description:
          - SNMP v3 privacy protocol
          type: str
          required: false
          default: DES
          choices:
          - AES
          - DES
        authKey:
          description:
          - SNMP v3 authentication key
          type: str
          required: false
        privKey:
          description:
          - SNMP v3 private key
          type: str
          required: false
        securityLevel:
          description:
          - SNMP v3 security level
          type: str
          required: false
          default: authPriv
          choices:
          - noAuthNoPriv
          - authNoPriv
          - authPriv
        filename:
          description:
          - Filename for SNMP testing
          type: str
          required: false
        extra_values:
          description: []
          type: json
          required: false
    disableSNMP:
      description:
      - Disable SNMP calls
      type: bool
      required: false
      default: false
    interfaces_NetworkBmcInterface:
      description:
      - IP on the management network
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - The network interface device name
          type: str
          required: true
        ip:
          description:
          - The interfaces IP address
          type: str
          required: false
          default: 0.0.0.0
        ipv6Ip:
          description:
          - The interfaces IPv6 IP address
          type: str
          required: false
          default: ::0
        dhcp:
          description:
          - Get the ip via DHCP, leave ip blank
          type: bool
          required: false
          default: false
        ipv6Dhcp:
          description:
          - Get the IPv6IP via DHCP, leave IPv6IP blank
          type: bool
          required: false
          default: false
        bringupduringinstall:
          description:
          - Brings up interface during install if on
          type: str
          required: false
          default: 'NO'
          choices:
          - 'NO'
          - 'YES'
          - YESANDKEEP
        network:
          description:
          - Network the interface is connected to
          type: str
          required: false
        alternativeHostname:
          description:
          - An alternative hostname to use if this is second (startif != always) IP address
            on the same network
          type: str
          required: false
        additionalHostnames:
          description:
          - List of additional hostnames that should resolve to the interfaces IP address
          type: list
          required: false
          default: []
        startIf:
          description:
          - Only run this service in the specified state
          type: str
          required: false
          default: ALWAYS
          choices:
          - ALWAYS
          - ACTIVE
          - PASSIVE
          - PREFERPASSIVE
        connectedMode:
          description:
          - IB connected mode
          type: bool
          required: false
          default: false
        bootable:
          description:
          - Mark the interface bootable and write a DHCP entry with file information
          type: bool
          required: false
          default: false
        excludeFromDhcpd:
          description:
          - Exclude from being added in dhcpd, use when both the members of a bond request
            an IP
          type: bool
          required: false
          default: false
        switchPorts:
          description:
          - Switch ports
          type: list
          required: false
          default: []
          elements: dict
          options:
            networkSwitch:
              description:
              - Switch
              type: str
              required: false
            port:
              description:
              - Port number on the switch
              type: int
              required: false
              default: 0
            breakout:
              description:
              - Breakout port number on the switch
              type: int
              required: false
              default: -1
        mac:
          description:
          - The interfaces MAC address
          type: str
          required: false
          default: 00:00:00:00:00:00
        gateway:
          description:
          - Gateway IP address, usually the head node's IP on the BMC network.
          type: str
          required: false
          default: 0.0.0.0
        vlanid:
          description:
          - VLAN ID setting for the BMC card. When set to 0, VLAN capabilities are disabled.
          type: int
          required: false
          default: 0
        lanchannel:
          description:
          - LAN channel for BMC interface
          type: int
          required: false
          default: 1
        onNetworkPriority:
          description:
          - Priority of DNS resolution queries for the interface on its network
          type: int
          required: false
          default: 10
        extra_values:
          description: []
          type: json
          required: false
    interfaces_NetworkBondInterface:
      description:
      - IP on the management network
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - The network interface device name
          type: str
          required: true
        ip:
          description:
          - The interfaces IP address
          type: str
          required: false
          default: 0.0.0.0
        ipv6Ip:
          description:
          - The interfaces IPv6 IP address
          type: str
          required: false
          default: ::0
        dhcp:
          description:
          - Get the ip via DHCP, leave ip blank
          type: bool
          required: false
          default: false
        ipv6Dhcp:
          description:
          - Get the IPv6IP via DHCP, leave IPv6IP blank
          type: bool
          required: false
          default: false
        bringupduringinstall:
          description:
          - Brings up interface during install if on
          type: str
          required: false
          default: 'NO'
          choices:
          - 'NO'
          - 'YES'
          - YESANDKEEP
        network:
          description:
          - Network the interface is connected to
          type: str
          required: false
        alternativeHostname:
          description:
          - An alternative hostname to use if this is second (startif != always) IP address
            on the same network
          type: str
          required: false
        additionalHostnames:
          description:
          - List of additional hostnames that should resolve to the interfaces IP address
          type: list
          required: false
          default: []
        startIf:
          description:
          - Only run this service in the specified state
          type: str
          required: false
          default: ALWAYS
          choices:
          - ALWAYS
          - ACTIVE
          - PASSIVE
          - PREFERPASSIVE
        connectedMode:
          description:
          - IB connected mode
          type: bool
          required: false
          default: false
        bootable:
          description:
          - Mark the interface bootable and write a DHCP entry with file information
          type: bool
          required: false
          default: false
        excludeFromDhcpd:
          description:
          - Exclude from being added in dhcpd, use when both the members of a bond request
            an IP
          type: bool
          required: false
          default: false
        switchPorts:
          description:
          - Switch ports
          type: list
          required: false
          default: []
          elements: dict
          options:
            networkSwitch:
              description:
              - Switch
              type: str
              required: false
            port:
              description:
              - Port number on the switch
              type: int
              required: false
              default: 0
            breakout:
              description:
              - Breakout port number on the switch
              type: int
              required: false
              default: -1
        mac:
          description:
          - The interfaces MAC address
          type: str
          required: false
          default: 00:00:00:00:00:00
        mode:
          description:
          - Bonding mode, see bonding.txt in the kernel documentation.
          type: int
          required: false
          default: 0
        options:
          description:
          - Options to pass to the bonding driver, see kernel documentation.
          type: str
          required: false
        interfaces:
          description:
          - List of interfaces which should be channel-bonded.
          type: list
          required: false
          default: []
        onNetworkPriority:
          description:
          - Priority of DNS resolution queries for the interface on its network
          type: int
          required: false
          default: 70
        extra_values:
          description: []
          type: json
          required: false
    interfaces_NetworkBridgeInterface:
      description:
      - IP on the management network
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - The network interface device name
          type: str
          required: true
        ip:
          description:
          - The interfaces IP address
          type: str
          required: false
          default: 0.0.0.0
        ipv6Ip:
          description:
          - The interfaces IPv6 IP address
          type: str
          required: false
          default: ::0
        dhcp:
          description:
          - Get the ip via DHCP, leave ip blank
          type: bool
          required: false
          default: false
        ipv6Dhcp:
          description:
          - Get the IPv6IP via DHCP, leave IPv6IP blank
          type: bool
          required: false
          default: false
        bringupduringinstall:
          description:
          - Brings up interface during install if on
          type: str
          required: false
          default: 'NO'
          choices:
          - 'NO'
          - 'YES'
          - YESANDKEEP
        network:
          description:
          - Network the interface is connected to
          type: str
          required: false
        alternativeHostname:
          description:
          - An alternative hostname to use if this is second (startif != always) IP address
            on the same network
          type: str
          required: false
        additionalHostnames:
          description:
          - List of additional hostnames that should resolve to the interfaces IP address
          type: list
          required: false
          default: []
        startIf:
          description:
          - Only run this service in the specified state
          type: str
          required: false
          default: ALWAYS
          choices:
          - ALWAYS
          - ACTIVE
          - PASSIVE
          - PREFERPASSIVE
        connectedMode:
          description:
          - IB connected mode
          type: bool
          required: false
          default: false
        bootable:
          description:
          - Mark the interface bootable and write a DHCP entry with file information
          type: bool
          required: false
          default: false
        excludeFromDhcpd:
          description:
          - Exclude from being added in dhcpd, use when both the members of a bond request
            an IP
          type: bool
          required: false
          default: false
        switchPorts:
          description:
          - Switch ports
          type: list
          required: false
          default: []
          elements: dict
          options:
            networkSwitch:
              description:
              - Switch
              type: str
              required: false
            port:
              description:
              - Port number on the switch
              type: int
              required: false
              default: 0
            breakout:
              description:
              - Breakout port number on the switch
              type: int
              required: false
              default: -1
        stp:
          description:
          - Spanning Tree Protocol enabled.
          type: bool
          required: false
          default: false
        forward_delay:
          description:
          - Frame forward delay (in seconds)
          type: int
          required: false
          default: 15
        interfaces:
          description:
          - List of interfaces which should be bridged.
          type: list
          required: false
          default: []
        onNetworkPriority:
          description:
          - Priority of DNS resolution queries for the interface on its network
          type: int
          required: false
          default: 80
        extra_values:
          description: []
          type: json
          required: false
    interfaces_NetworkPhysicalInterface:
      description:
      - IP on the management network
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - The network interface device name
          type: str
          required: true
        ip:
          description:
          - The interfaces IP address
          type: str
          required: false
          default: 0.0.0.0
        ipv6Ip:
          description:
          - The interfaces IPv6 IP address
          type: str
          required: false
          default: ::0
        dhcp:
          description:
          - Get the ip via DHCP, leave ip blank
          type: bool
          required: false
          default: false
        ipv6Dhcp:
          description:
          - Get the IPv6IP via DHCP, leave IPv6IP blank
          type: bool
          required: false
          default: false
        bringupduringinstall:
          description:
          - Brings up interface during install if on
          type: str
          required: false
          default: 'NO'
          choices:
          - 'NO'
          - 'YES'
          - YESANDKEEP
        network:
          description:
          - Network the interface is connected to
          type: str
          required: false
        alternativeHostname:
          description:
          - An alternative hostname to use if this is second (startif != always) IP address
            on the same network
          type: str
          required: false
        additionalHostnames:
          description:
          - List of additional hostnames that should resolve to the interfaces IP address
          type: list
          required: false
          default: []
        startIf:
          description:
          - Only run this service in the specified state
          type: str
          required: false
          default: ALWAYS
          choices:
          - ALWAYS
          - ACTIVE
          - PASSIVE
          - PREFERPASSIVE
        connectedMode:
          description:
          - IB connected mode
          type: bool
          required: false
          default: false
        bootable:
          description:
          - Mark the interface bootable and write a DHCP entry with file information
          type: bool
          required: false
          default: false
        excludeFromDhcpd:
          description:
          - Exclude from being added in dhcpd, use when both the members of a bond request
            an IP
          type: bool
          required: false
          default: false
        switchPorts:
          description:
          - Switch ports
          type: list
          required: false
          default: []
          elements: dict
          options:
            networkSwitch:
              description:
              - Switch
              type: str
              required: false
            port:
              description:
              - Port number on the switch
              type: int
              required: false
              default: 0
            breakout:
              description:
              - Breakout port number on the switch
              type: int
              required: false
              default: -1
        mac:
          description:
          - The interfaces MAC address
          type: str
          required: false
          default: 00:00:00:00:00:00
        speed:
          description:
          - The interfaces network speed.
          type: str
          required: false
        cardtype:
          description:
          - The type of network interface.
          type: str
          required: false
        onNetworkPriority:
          description:
          - Priority of DNS resolution queries for the interface on its network
          type: int
          required: false
          default: 60
        extra_values:
          description: []
          type: json
          required: false
    interfaces_NetworkAliasInterface:
      description:
      - IP on the management network
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - The network interface device name
          type: str
          required: true
        ip:
          description:
          - The interfaces IP address
          type: str
          required: false
          default: 0.0.0.0
        ipv6Ip:
          description:
          - The interfaces IPv6 IP address
          type: str
          required: false
          default: ::0
        dhcp:
          description:
          - Get the ip via DHCP, leave ip blank
          type: bool
          required: false
          default: false
        ipv6Dhcp:
          description:
          - Get the IPv6IP via DHCP, leave IPv6IP blank
          type: bool
          required: false
          default: false
        bringupduringinstall:
          description:
          - Brings up interface during install if on
          type: str
          required: false
          default: 'NO'
          choices:
          - 'NO'
          - 'YES'
          - YESANDKEEP
        network:
          description:
          - Network the interface is connected to
          type: str
          required: false
        alternativeHostname:
          description:
          - An alternative hostname to use if this is second (startif != always) IP address
            on the same network
          type: str
          required: false
        additionalHostnames:
          description:
          - List of additional hostnames that should resolve to the interfaces IP address
          type: list
          required: false
          default: []
        startIf:
          description:
          - Only run this service in the specified state
          type: str
          required: false
          default: ALWAYS
          choices:
          - ALWAYS
          - ACTIVE
          - PASSIVE
          - PREFERPASSIVE
        connectedMode:
          description:
          - IB connected mode
          type: bool
          required: false
          default: false
        bootable:
          description:
          - Mark the interface bootable and write a DHCP entry with file information
          type: bool
          required: false
          default: false
        excludeFromDhcpd:
          description:
          - Exclude from being added in dhcpd, use when both the members of a bond request
            an IP
          type: bool
          required: false
          default: false
        switchPorts:
          description:
          - Switch ports
          type: list
          required: false
          default: []
          elements: dict
          options:
            networkSwitch:
              description:
              - Switch
              type: str
              required: false
            port:
              description:
              - Port number on the switch
              type: int
              required: false
              default: 0
            breakout:
              description:
              - Breakout port number on the switch
              type: int
              required: false
              default: -1
        onNetworkPriority:
          description:
          - Priority of DNS resolution queries for the interface on its network
          type: int
          required: false
          default: 40
        extra_values:
          description: []
          type: json
          required: false
    interfaces_NetworkVLANInterface:
      description:
      - IP on the management network
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - The network interface device name
          type: str
          required: true
        ip:
          description:
          - The interfaces IP address
          type: str
          required: false
          default: 0.0.0.0
        ipv6Ip:
          description:
          - The interfaces IPv6 IP address
          type: str
          required: false
          default: ::0
        dhcp:
          description:
          - Get the ip via DHCP, leave ip blank
          type: bool
          required: false
          default: false
        ipv6Dhcp:
          description:
          - Get the IPv6IP via DHCP, leave IPv6IP blank
          type: bool
          required: false
          default: false
        bringupduringinstall:
          description:
          - Brings up interface during install if on
          type: str
          required: false
          default: 'NO'
          choices:
          - 'NO'
          - 'YES'
          - YESANDKEEP
        network:
          description:
          - Network the interface is connected to
          type: str
          required: false
        alternativeHostname:
          description:
          - An alternative hostname to use if this is second (startif != always) IP address
            on the same network
          type: str
          required: false
        additionalHostnames:
          description:
          - List of additional hostnames that should resolve to the interfaces IP address
          type: list
          required: false
          default: []
        startIf:
          description:
          - Only run this service in the specified state
          type: str
          required: false
          default: ALWAYS
          choices:
          - ALWAYS
          - ACTIVE
          - PASSIVE
          - PREFERPASSIVE
        connectedMode:
          description:
          - IB connected mode
          type: bool
          required: false
          default: false
        bootable:
          description:
          - Mark the interface bootable and write a DHCP entry with file information
          type: bool
          required: false
          default: false
        excludeFromDhcpd:
          description:
          - Exclude from being added in dhcpd, use when both the members of a bond request
            an IP
          type: bool
          required: false
          default: false
        switchPorts:
          description:
          - Switch ports
          type: list
          required: false
          default: []
          elements: dict
          options:
            networkSwitch:
              description:
              - Switch
              type: str
              required: false
            port:
              description:
              - Port number on the switch
              type: int
              required: false
              default: 0
            breakout:
              description:
              - Breakout port number on the switch
              type: int
              required: false
              default: -1
        reorder_hdr:
          description:
          - When set to true the VLAN device will move the ethernet header around to make
            it look exactly like a real ethernet device.
          type: bool
          required: false
          default: true
        onNetworkPriority:
          description:
          - Priority of DNS resolution queries for the interface on its network
          type: int
          required: false
          default: 50
        extra_values:
          description: []
          type: json
          required: false
    interfaces_NetworkTunnelInterface:
      description:
      - IP on the management network
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - The network interface device name
          type: str
          required: true
        ip:
          description:
          - The interfaces IP address
          type: str
          required: false
          default: 0.0.0.0
        ipv6Ip:
          description:
          - The interfaces IPv6 IP address
          type: str
          required: false
          default: ::0
        dhcp:
          description:
          - Get the ip via DHCP, leave ip blank
          type: bool
          required: false
          default: false
        ipv6Dhcp:
          description:
          - Get the IPv6IP via DHCP, leave IPv6IP blank
          type: bool
          required: false
          default: false
        bringupduringinstall:
          description:
          - Brings up interface during install if on
          type: str
          required: false
          default: 'NO'
          choices:
          - 'NO'
          - 'YES'
          - YESANDKEEP
        network:
          description:
          - Network the interface is connected to
          type: str
          required: false
        alternativeHostname:
          description:
          - An alternative hostname to use if this is second (startif != always) IP address
            on the same network
          type: str
          required: false
        additionalHostnames:
          description:
          - List of additional hostnames that should resolve to the interfaces IP address
          type: list
          required: false
          default: []
        startIf:
          description:
          - Only run this service in the specified state
          type: str
          required: false
          default: ALWAYS
          choices:
          - ALWAYS
          - ACTIVE
          - PASSIVE
          - PREFERPASSIVE
        connectedMode:
          description:
          - IB connected mode
          type: bool
          required: false
          default: false
        bootable:
          description:
          - Mark the interface bootable and write a DHCP entry with file information
          type: bool
          required: false
          default: false
        excludeFromDhcpd:
          description:
          - Exclude from being added in dhcpd, use when both the members of a bond request
            an IP
          type: bool
          required: false
          default: false
        switchPorts:
          description:
          - Switch ports
          type: list
          required: false
          default: []
          elements: dict
          options:
            networkSwitch:
              description:
              - Switch
              type: str
              required: false
            port:
              description:
              - Port number on the switch
              type: int
              required: false
              default: 0
            breakout:
              description:
              - Breakout port number on the switch
              type: int
              required: false
              default: -1
        onNetworkPriority:
          description:
          - Priority of DNS resolution queries for the interface on its network
          type: int
          required: false
          default: 30
        extra_values:
          description: []
          type: json
          required: false
    interfaces_NetworkNetMapInterface:
      description:
      - IP on the management network
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - The network interface device name
          type: str
          required: true
        ip:
          description:
          - The interfaces IP address
          type: str
          required: false
          default: 0.0.0.0
        ipv6Ip:
          description:
          - The interfaces IPv6 IP address
          type: str
          required: false
          default: ::0
        dhcp:
          description:
          - Get the ip via DHCP, leave ip blank
          type: bool
          required: false
          default: false
        ipv6Dhcp:
          description:
          - Get the IPv6IP via DHCP, leave IPv6IP blank
          type: bool
          required: false
          default: false
        bringupduringinstall:
          description:
          - Brings up interface during install if on
          type: str
          required: false
          default: 'NO'
          choices:
          - 'NO'
          - 'YES'
          - YESANDKEEP
        network:
          description:
          - Network the interface is connected to
          type: str
          required: false
        alternativeHostname:
          description:
          - An alternative hostname to use if this is second (startif != always) IP address
            on the same network
          type: str
          required: false
        additionalHostnames:
          description:
          - List of additional hostnames that should resolve to the interfaces IP address
          type: list
          required: false
          default: []
        startIf:
          description:
          - Only run this service in the specified state
          type: str
          required: false
          default: ALWAYS
          choices:
          - ALWAYS
          - ACTIVE
          - PASSIVE
          - PREFERPASSIVE
        connectedMode:
          description:
          - IB connected mode
          type: bool
          required: false
          default: false
        bootable:
          description:
          - Mark the interface bootable and write a DHCP entry with file information
          type: bool
          required: false
          default: false
        excludeFromDhcpd:
          description:
          - Exclude from being added in dhcpd, use when both the members of a bond request
            an IP
          type: bool
          required: false
          default: false
        switchPorts:
          description:
          - Switch ports
          type: list
          required: false
          default: []
          elements: dict
          options:
            networkSwitch:
              description:
              - Switch
              type: str
              required: false
            port:
              description:
              - Port number on the switch
              type: int
              required: false
              default: 0
            breakout:
              description:
              - Breakout port number on the switch
              type: int
              required: false
              default: -1
        onNetworkPriority:
          description:
          - Priority of DNS resolution queries for the interface on its network
          type: int
          required: false
          default: 20
        extra_values:
          description: []
          type: json
          required: false
    extra_values:
      description: []
      type: json
      required: false

requirements: [cmdaemon-pythoncm, deepdiff, python-box]
author:
- iiiteam <iiiteam@brightcomputing.com>
"""

EXAMPLES = r"""

"""

RETURN = r"""
---
rack_sensor:
  type: complex
  description: ''
  returned: success
  contains:
    uuid:
      type: str
      description: ''
      returned: success
    baseType:
      type: str
      description: ''
      returned: success
    childType:
      type: str
      description: ''
      returned: success
    revision:
      type: str
      description: ''
      returned: success
    modified:
      type: bool
      description: ''
      returned: success
    is_committed:
      type: bool
      description: ''
      returned: success
    to_be_removed:
      type: bool
      description: ''
      returned: success
    extra_values:
      type: json
      description: ''
      returned: success
    hostname:
      type: str
      description: Hostname
      returned: success
    mac:
      type: str
      description: MAC address
      returned: success
    defaultGateway:
      type: str
      description: Default gateway for the device
      returned: success
    defaultGatewayMetric:
      type: int
      description: Default gateway metric
      returned: success
    creationTime:
      type: int
      description: Date on which node was defined
      returned: success
    partition:
      type: complex
      description: Partition to which this device belongs
      returned: success
    switchPorts:
      type: list
      description: Switch ports
      returned: success
    powerDistributionUnits:
      type: list
      description: List of outlets on powerdistributionunits
      returned: success
    rackPosition:
      type: complex
      description: Name of the rack in which the device resides
      returned: success
    chassisPosition:
      type: complex
      description: Chassis position in which the device resides
      returned: success
    accessSettings:
      type: complex
      description: Configure the cluster wide Access settings
      returned: success
    bmcSettings:
      type: complex
      description: Configure the baseboard management controller settings
      returned: success
    powerControl:
      type: str
      description: 'Specifies which type of power control feature is being used (values:
        none, apc, custom, cloud, ipmi0, ilo0, drac0, rf0, cimc0 or rshim0)'
      returned: success
    customPowerScript:
      type: str
      description: Script that will be used to perform power on/off/reset/status operations
      returned: success
    customPowerScriptArgument:
      type: str
      description: Argument for the custom power script
      returned: success
    customPingScript:
      type: str
      description: Script that will be used to ping a device
      returned: success
    customPingScriptArgument:
      type: str
      description: Argument for the custom ping script
      returned: success
    notes:
      type: str
      description: Administrator notes
      returned: success
    interfaces:
      type: list
      description: IP on the management network
      returned: success
    provisioningInterface:
      type: complex
      description: Network interface on which the node will receive software image
        updates
      returned: success
    managementNetwork:
      type: complex
      description: Determines what network should be used for management traffic.
        If not set, category or partition setting is used.
      returned: success
    userdefined1:
      type: str
      description: A free text field passed to custom scripts
      returned: success
    userdefined2:
      type: str
      description: A free text field passed to custom scripts
      returned: success
    userDefinedResources:
      type: str
      description: User defined resources used to filter monitoring data producers
      returned: success
    supportsGNSS:
      type: bool
      description: Supports GNSS location
      returned: success
    partNumber:
      type: str
      description: Part number
      returned: success
    serialNumber:
      type: str
      description: Serial number
      returned: success
    prometheusMetricForwarders:
      type: list
      description: Prometheus metric forwarders
      returned: success
    model:
      type: str
      description: Device model name
      returned: success
    sensors:
      type: list
      description: Sensors in the rackmon kit
      returned: success
    snmpSettings:
      type: complex
      description: Configure the cluster wide SNMP settings
      returned: success
    disableSNMP:
      type: bool
      description: Disable SNMP calls
      returned: success

"""
############################
# Imports
############################

from copy import deepcopy
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import RackSensor
except ImportError:
    HAS_PYTHONCM = False
    PYTHONCM_IMP_ERR = traceback.format_exc()
else:
    HAS_PYTHONCM = True
    PYTHONCM_IMP_ERR = None

try:
    import deepdiff
except ImportError:
    HAS_DEEPDIFF = False
    DEEPDIFF_IMP_ERR = traceback.format_exc()
else:
    HAS_DEEPDIFF = True
    DEEPDIFF_IMP_ERR = None

try:
    from box import Box
except ImportError:
    HAS_BOX = False
    BOX_IMP_ERR = traceback.format_exc()
else:
    HAS_BOX = True
    BOX_IMP_ERR = None

from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.base_module import BaseModule
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.core import EntityManager
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.utils import json_encode_entity
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.argspecs.rack_sensor import RackSensor_ArgSpec

############################
# main
############################

def main():

    module = BaseModule(
        argument_spec=RackSensor_ArgSpec.argument_spec,
        supports_check_mode=True,
    )

    if not HAS_PYTHONCM:
        module.fail_json(msg=missing_required_lib("cmdaemon-pythoncm"), exception=PYTHONCM_IMP_ERR)

    if not HAS_DEEPDIFF:
        module.fail_json(msg=missing_required_lib("deepdiff"), exception=DEEPDIFF_IMP_ERR)

    if not HAS_BOX:
        module.fail_json(msg=missing_required_lib("python-box"), exception=BOX_IMP_ERR)

    params =  module.bright_params

    cluster = Cluster()  # TODO make this configurable

    entity_manager = EntityManager(cluster, module.log)

    entity = entity_manager.lookup_entity(params, RackSensor)

    changed = False

    diff = None

    desired_state = params["state"]

    if not entity:
        if desired_state == "present":
            entity, res = entity_manager.create_resource(RackSensor, params, commit=not module.check_mode)
            changed = True
    else:

        if desired_state == "present":
            diff = entity_manager.check_diff(entity, params)
            if diff:
                entity, res = entity_manager.update_resource(entity, params, commit=not module.check_mode)
                changed = True

        if desired_state == "absent":
            entity, res = entity_manager.delete_resource(entity, params, commit=not module.check_mode)
            changed = True

    entity_as_dict = json_encode_entity(entity)

    cluster.disconnect()

    if not changed:
        module.exit_json(changed=changed, **entity_as_dict)

    if res.good:
        module.exit_json(changed=changed, diff=diff, **entity_as_dict)
    else:
        if hasattr(res, 'validation'):
            msg = "|".join(it.message for it in res.validation)
        else:
            msg = "Operation failed."
        module.fail_json(msg=msg, **entity_as_dict)


if __name__ == '__main__':
    main()