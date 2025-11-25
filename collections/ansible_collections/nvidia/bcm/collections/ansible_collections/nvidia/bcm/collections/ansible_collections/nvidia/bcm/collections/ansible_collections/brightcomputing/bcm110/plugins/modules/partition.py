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
module: partition
description: ['Partition']
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
    name:
      description:
      - Partition name
      type: str
      required: true
    clusterName:
      description:
      - Cluster name
      type: str
      required: false
    clusterReferenceArchitecture:
      description:
      - Description of the cluster architecture
      type: str
      required: false
    primaryHeadNode:
      description:
      - Primary head node
      type: str
      required: false
    failover:
      description:
      - Manage failover setup for this cluster
      type: dict
      required: false
      options:
        secondaryHeadNode:
          description:
          - Secondary/failover head node
          type: str
          required: false
        keepalive:
          description:
          - Interval between pings
          type: int
          required: false
          default: 1
        warntime:
          description:
          - How quickly to issue a 'late' warning
          type: int
          required: false
          default: 5
        deadtime:
          description:
          - How quickly to decide that a node in a cluster is dead
          type: int
          required: false
          default: 10
        initdead:
          description:
          - Time between starting failover and declaring a cluster node dead
          type: int
          required: false
          default: 30
        quorumTime:
          description:
          - Time before deciding quorum ended in failure
          type: int
          required: false
          default: 60
        mountScript:
          description:
          - Script that mounts the shared storage device when a node becomes the active
            headnode
          type: str
          required: false
        unmountScript:
          description:
          - Script that unmounts the shared storage device when a node stoppes being the
            active headnode
          type: str
          required: false
        failoverNetwork:
          description:
          - Network for failover ping
          type: str
          required: false
        disableAutomaticFailover:
          description:
          - When automatic failover is disabled the passive headnode will not take over
            if it detects the active headnode is dead
          type: bool
          required: false
          default: false
        preFailoverScript:
          description:
          - Prefailover script will be run on both headnodes before failover has begun
          type: str
          required: false
        postFailoverScript:
          description:
          - Postfailover script will be run on both headnodes after failover has completed
          type: str
          required: false
        ipTakeOverMethod:
          description:
          - The manner in which shared IP gets transferred
          type: str
          required: false
          default: ARP
          choices:
          - ARP
          - SCRIPT
          - CLOUD
          - LOAD_BALANCER
        ipTakeOverScript:
          description:
          - IP take over script
          type: str
          required: false
    timeZoneSettings:
      description:
      - Time zone
      type: dict
      required: false
      options:
        timeZone:
          description:
          - Time zone
          type: str
          required: false
          choices:
          - Africa/Abidjan
          - Africa/Accra
          - Africa/Addis_Ababa
          - Africa/Algiers
          - Africa/Asmara
          - Africa/Asmera
          - Africa/Bamako
          - Africa/Bangui
          - Africa/Banjul
          - Africa/Bissau
          - Africa/Blantyre
          - Africa/Brazzaville
          - Africa/Bujumbura
          - Africa/Cairo
          - Africa/Casablanca
          - Africa/Ceuta
          - Africa/Conakry
          - Africa/Dakar
          - Africa/Dar_es_Salaam
          - Africa/Djibouti
          - Africa/Douala
          - Africa/El_Aaiun
          - Africa/Freetown
          - Africa/Gaborone
          - Africa/Harare
          - Africa/Johannesburg
          - Africa/Juba
          - Africa/Kampala
          - Africa/Khartoum
          - Africa/Kigali
          - Africa/Kinshasa
          - Africa/Lagos
          - Africa/Libreville
          - Africa/Lome
          - Africa/Luanda
          - Africa/Lubumbashi
          - Africa/Lusaka
          - Africa/Malabo
          - Africa/Maputo
          - Africa/Maseru
          - Africa/Mbabane
          - Africa/Mogadishu
          - Africa/Monrovia
          - Africa/Nairobi
          - Africa/Ndjamena
          - Africa/Niamey
          - Africa/Nouakchott
          - Africa/Ouagadougou
          - Africa/Porto-Novo
          - Africa/Sao_Tome
          - Africa/Timbuktu
          - Africa/Tripoli
          - Africa/Tunis
          - Africa/Windhoek
          - America/Adak
          - America/Anchorage
          - America/Anguilla
          - America/Antigua
          - America/Araguaina
          - America/Argentina/Buenos_Aires
          - America/Argentina/Catamarca
          - America/Argentina/ComodRivadavia
          - America/Argentina/Cordoba
          - America/Argentina/Jujuy
          - America/Argentina/La_Rioja
          - America/Argentina/Mendoza
          - America/Argentina/Rio_Gallegos
          - America/Argentina/Salta
          - America/Argentina/San_Juan
          - America/Argentina/San_Luis
          - America/Argentina/Tucuman
          - America/Argentina/Ushuaia
          - America/Aruba
          - America/Asuncion
          - America/Atikokan
          - America/Atka
          - America/Bahia
          - America/Bahia_Banderas
          - America/Barbados
          - America/Belem
          - America/Belize
          - America/Blanc-Sablon
          - America/Boa_Vista
          - America/Bogota
          - America/Boise
          - America/Buenos_Aires
          - America/Cambridge_Bay
          - America/Campo_Grande
          - America/Cancun
          - America/Caracas
          - America/Catamarca
          - America/Cayenne
          - America/Cayman
          - America/Chicago
          - America/Chihuahua
          - America/Coral_Harbour
          - America/Cordoba
          - America/Costa_Rica
          - America/Creston
          - America/Cuiaba
          - America/Curacao
          - America/Danmarkshavn
          - America/Dawson
          - America/Dawson_Creek
          - America/Denver
          - America/Detroit
          - America/Dominica
          - America/Edmonton
          - America/Eirunepe
          - America/El_Salvador
          - America/Ensenada
          - America/Fort_Nelson
          - America/Fort_Wayne
          - America/Fortaleza
          - America/Glace_Bay
          - America/Godthab
          - America/Goose_Bay
          - America/Grand_Turk
          - America/Grenada
          - America/Guadeloupe
          - America/Guatemala
          - America/Guayaquil
          - America/Guyana
          - America/Halifax
          - America/Havana
          - America/Hermosillo
          - America/Indiana/Indianapolis
          - America/Indiana/Knox
          - America/Indiana/Marengo
          - America/Indiana/Petersburg
          - America/Indiana/Tell_City
          - America/Indiana/Vevay
          - America/Indiana/Vincennes
          - America/Indiana/Winamac
          - America/Indianapolis
          - America/Inuvik
          - America/Iqaluit
          - America/Jamaica
          - America/Jujuy
          - America/Juneau
          - America/Kentucky/Louisville
          - America/Kentucky/Monticello
          - America/Knox_IN
          - America/Kralendijk
          - America/La_Paz
          - America/Lima
          - America/Los_Angeles
          - America/Louisville
          - America/Lower_Princes
          - America/Maceio
          - America/Managua
          - America/Manaus
          - America/Marigot
          - America/Martinique
          - America/Matamoros
          - America/Mazatlan
          - America/Mendoza
          - America/Menominee
          - America/Merida
          - America/Metlakatla
          - America/Mexico_City
          - America/Miquelon
          - America/Moncton
          - America/Monterrey
          - America/Montevideo
          - America/Montreal
          - America/Montserrat
          - America/Nassau
          - America/New_York
          - America/Nipigon
          - America/Nome
          - America/Noronha
          - America/North_Dakota/Beulah
          - America/North_Dakota/Center
          - America/North_Dakota/New_Salem
          - America/Nuuk
          - America/Ojinaga
          - America/Panama
          - America/Pangnirtung
          - America/Paramaribo
          - America/Phoenix
          - America/Port-au-Prince
          - America/Port_of_Spain
          - America/Porto_Acre
          - America/Porto_Velho
          - America/Puerto_Rico
          - America/Punta_Arenas
          - America/Rainy_River
          - America/Rankin_Inlet
          - America/Recife
          - America/Regina
          - America/Resolute
          - America/Rio_Branco
          - America/Rosario
          - America/Santa_Isabel
          - America/Santarem
          - America/Santiago
          - America/Santo_Domingo
          - America/Sao_Paulo
          - America/Scoresbysund
          - America/Shiprock
          - America/Sitka
          - America/St_Barthelemy
          - America/St_Johns
          - America/St_Kitts
          - America/St_Lucia
          - America/St_Thomas
          - America/St_Vincent
          - America/Swift_Current
          - America/Tegucigalpa
          - America/Thule
          - America/Thunder_Bay
          - America/Tijuana
          - America/Toronto
          - America/Tortola
          - America/Vancouver
          - America/Virgin
          - America/Whitehorse
          - America/Winnipeg
          - America/Yakutat
          - America/Yellowknife
          - Antarctica/Casey
          - Antarctica/Davis
          - Antarctica/DumontDUrville
          - Antarctica/Macquarie
          - Antarctica/Mawson
          - Antarctica/McMurdo
          - Antarctica/Palmer
          - Antarctica/Rothera
          - Antarctica/South_Pole
          - Antarctica/Syowa
          - Antarctica/Troll
          - Antarctica/Vostok
          - Arctic/Longyearbyen
          - Asia/Aden
          - Asia/Almaty
          - Asia/Amman
          - Asia/Anadyr
          - Asia/Aqtau
          - Asia/Aqtobe
          - Asia/Ashgabat
          - Asia/Ashkhabad
          - Asia/Atyrau
          - Asia/Baghdad
          - Asia/Bahrain
          - Asia/Baku
          - Asia/Bangkok
          - Asia/Barnaul
          - Asia/Beirut
          - Asia/Bishkek
          - Asia/Brunei
          - Asia/Calcutta
          - Asia/Chita
          - Asia/Choibalsan
          - Asia/Chongqing
          - Asia/Chungking
          - Asia/Colombo
          - Asia/Dacca
          - Asia/Damascus
          - Asia/Dhaka
          - Asia/Dili
          - Asia/Dubai
          - Asia/Dushanbe
          - Asia/Famagusta
          - Asia/Gaza
          - Asia/Harbin
          - Asia/Hebron
          - Asia/Ho_Chi_Minh
          - Asia/Hong_Kong
          - Asia/Hovd
          - Asia/Irkutsk
          - Asia/Istanbul
          - Asia/Jakarta
          - Asia/Jayapura
          - Asia/Jerusalem
          - Asia/Kabul
          - Asia/Kamchatka
          - Asia/Karachi
          - Asia/Kashgar
          - Asia/Kathmandu
          - Asia/Katmandu
          - Asia/Khandyga
          - Asia/Kolkata
          - Asia/Krasnoyarsk
          - Asia/Kuala_Lumpur
          - Asia/Kuching
          - Asia/Kuwait
          - Asia/Macao
          - Asia/Macau
          - Asia/Magadan
          - Asia/Makassar
          - Asia/Manila
          - Asia/Muscat
          - Asia/Nicosia
          - Asia/Novokuznetsk
          - Asia/Novosibirsk
          - Asia/Omsk
          - Asia/Oral
          - Asia/Phnom_Penh
          - Asia/Pontianak
          - Asia/Pyongyang
          - Asia/Qatar
          - Asia/Qostanay
          - Asia/Qyzylorda
          - Asia/Rangoon
          - Asia/Riyadh
          - Asia/Saigon
          - Asia/Sakhalin
          - Asia/Samarkand
          - Asia/Seoul
          - Asia/Shanghai
          - Asia/Singapore
          - Asia/Srednekolymsk
          - Asia/Taipei
          - Asia/Tashkent
          - Asia/Tbilisi
          - Asia/Tehran
          - Asia/Tel_Aviv
          - Asia/Thimbu
          - Asia/Thimphu
          - Asia/Tokyo
          - Asia/Tomsk
          - Asia/Ujung_Pandang
          - Asia/Ulaanbaatar
          - Asia/Ulan_Bator
          - Asia/Urumqi
          - Asia/Ust-Nera
          - Asia/Vientiane
          - Asia/Vladivostok
          - Asia/Yakutsk
          - Asia/Yangon
          - Asia/Yekaterinburg
          - Asia/Yerevan
          - Atlantic/Azores
          - Atlantic/Bermuda
          - Atlantic/Canary
          - Atlantic/Cape_Verde
          - Atlantic/Faeroe
          - Atlantic/Faroe
          - Atlantic/Jan_Mayen
          - Atlantic/Madeira
          - Atlantic/Reykjavik
          - Atlantic/South_Georgia
          - Atlantic/St_Helena
          - Atlantic/Stanley
          - Australia/ACT
          - Australia/Adelaide
          - Australia/Brisbane
          - Australia/Broken_Hill
          - Australia/Canberra
          - Australia/Currie
          - Australia/Darwin
          - Australia/Eucla
          - Australia/Hobart
          - Australia/LHI
          - Australia/Lindeman
          - Australia/Lord_Howe
          - Australia/Melbourne
          - Australia/NSW
          - Australia/North
          - Australia/Perth
          - Australia/Queensland
          - Australia/South
          - Australia/Sydney
          - Australia/Tasmania
          - Australia/Victoria
          - Australia/West
          - Australia/Yancowinna
          - Brazil/Acre
          - Brazil/DeNoronha
          - Brazil/East
          - Brazil/West
          - CET
          - CST6CDT
          - Canada/Atlantic
          - Canada/Central
          - Canada/Eastern
          - Canada/Mountain
          - Canada/Newfoundland
          - Canada/Pacific
          - Canada/Saskatchewan
          - Canada/Yukon
          - Chile/Continental
          - Chile/EasterIsland
          - Cuba
          - EET
          - EST
          - EST5EDT
          - Egypt
          - Eire
          - Etc/GMT
          - Etc/GMT+0
          - Etc/GMT+1
          - Etc/GMT+10
          - Etc/GMT+11
          - Etc/GMT+12
          - Etc/GMT+2
          - Etc/GMT+3
          - Etc/GMT+4
          - Etc/GMT+5
          - Etc/GMT+6
          - Etc/GMT+7
          - Etc/GMT+8
          - Etc/GMT+9
          - Etc/GMT-0
          - Etc/GMT-1
          - Etc/GMT-10
          - Etc/GMT-11
          - Etc/GMT-12
          - Etc/GMT-13
          - Etc/GMT-14
          - Etc/GMT-2
          - Etc/GMT-3
          - Etc/GMT-4
          - Etc/GMT-5
          - Etc/GMT-6
          - Etc/GMT-7
          - Etc/GMT-8
          - Etc/GMT-9
          - Etc/GMT0
          - Etc/Greenwich
          - Etc/UCT
          - Etc/UTC
          - Etc/Universal
          - Etc/Zulu
          - Europe/Amsterdam
          - Europe/Andorra
          - Europe/Astrakhan
          - Europe/Athens
          - Europe/Belfast
          - Europe/Belgrade
          - Europe/Berlin
          - Europe/Bratislava
          - Europe/Brussels
          - Europe/Bucharest
          - Europe/Budapest
          - Europe/Busingen
          - Europe/Chisinau
          - Europe/Copenhagen
          - Europe/Dublin
          - Europe/Gibraltar
          - Europe/Guernsey
          - Europe/Helsinki
          - Europe/Isle_of_Man
          - Europe/Istanbul
          - Europe/Jersey
          - Europe/Kaliningrad
          - Europe/Kiev
          - Europe/Kirov
          - Europe/Lisbon
          - Europe/Ljubljana
          - Europe/London
          - Europe/Luxembourg
          - Europe/Madrid
          - Europe/Malta
          - Europe/Mariehamn
          - Europe/Minsk
          - Europe/Monaco
          - Europe/Moscow
          - Europe/Nicosia
          - Europe/Oslo
          - Europe/Paris
          - Europe/Podgorica
          - Europe/Prague
          - Europe/Riga
          - Europe/Rome
          - Europe/Samara
          - Europe/San_Marino
          - Europe/Sarajevo
          - Europe/Saratov
          - Europe/Simferopol
          - Europe/Skopje
          - Europe/Sofia
          - Europe/Stockholm
          - Europe/Tallinn
          - Europe/Tirane
          - Europe/Tiraspol
          - Europe/Ulyanovsk
          - Europe/Uzhgorod
          - Europe/Vaduz
          - Europe/Vatican
          - Europe/Vienna
          - Europe/Vilnius
          - Europe/Volgograd
          - Europe/Warsaw
          - Europe/Zagreb
          - Europe/Zaporozhye
          - Europe/Zurich
          - Factory
          - GB
          - GB-Eire
          - GMT
          - GMT+0
          - GMT-0
          - GMT0
          - Greenwich
          - HST
          - Hongkong
          - Iceland
          - Indian/Antananarivo
          - Indian/Chagos
          - Indian/Christmas
          - Indian/Cocos
          - Indian/Comoro
          - Indian/Kerguelen
          - Indian/Mahe
          - Indian/Maldives
          - Indian/Mauritius
          - Indian/Mayotte
          - Indian/Reunion
          - Iran
          - Israel
          - Jamaica
          - Japan
          - Kwajalein
          - Libya
          - MET
          - MST
          - MST7MDT
          - Mexico/BajaNorte
          - Mexico/BajaSur
          - Mexico/General
          - NZ
          - NZ-CHAT
          - Navajo
          - PRC
          - PST8PDT
          - Pacific/Apia
          - Pacific/Auckland
          - Pacific/Bougainville
          - Pacific/Chatham
          - Pacific/Chuuk
          - Pacific/Easter
          - Pacific/Efate
          - Pacific/Enderbury
          - Pacific/Fakaofo
          - Pacific/Fiji
          - Pacific/Funafuti
          - Pacific/Galapagos
          - Pacific/Gambier
          - Pacific/Guadalcanal
          - Pacific/Guam
          - Pacific/Honolulu
          - Pacific/Johnston
          - Pacific/Kanton
          - Pacific/Kiritimati
          - Pacific/Kosrae
          - Pacific/Kwajalein
          - Pacific/Majuro
          - Pacific/Marquesas
          - Pacific/Midway
          - Pacific/Nauru
          - Pacific/Niue
          - Pacific/Norfolk
          - Pacific/Noumea
          - Pacific/Pago_Pago
          - Pacific/Palau
          - Pacific/Pitcairn
          - Pacific/Pohnpei
          - Pacific/Ponape
          - Pacific/Port_Moresby
          - Pacific/Rarotonga
          - Pacific/Saipan
          - Pacific/Samoa
          - Pacific/Tahiti
          - Pacific/Tarawa
          - Pacific/Tongatapu
          - Pacific/Truk
          - Pacific/Wake
          - Pacific/Wallis
          - Pacific/Yap
          - Poland
          - Portugal
          - ROC
          - ROK
          - Singapore
          - Turkey
          - UCT
          - US/Alaska
          - US/Aleutian
          - US/Arizona
          - US/Central
          - US/East-Indiana
          - US/Eastern
          - US/Hawaii
          - US/Indiana-Starke
          - US/Michigan
          - US/Mountain
          - US/Pacific
          - US/Samoa
          - UTC
          - Universal
          - W-SU
          - WET
          - Zulu
        biosUTC:
          description:
          - Store BIOS time in UTC
          type: bool
          required: false
          default: false
    adminEmail:
      description:
      - Administrator email
      type: list
      required: false
      default: []
    slaveName:
      description:
      - Default prefix to identify nodes. eg node003 (basename = node)
      type: str
      required: false
    slaveDigits:
      description:
      - Number of digits used to identify nodes. eg node003 (digits = 3)
      type: int
      required: false
      default: 3
    nameServers:
      description:
      - Name servers
      type: list
      required: false
      default: []
    nameServersFromDhcp:
      description:
      - Name servers provided by DHCP, edit the name servers property instead
      type: list
      required: false
      default: []
    timeServers:
      description:
      - NTP time servers
      type: list
      required: false
      default: []
    searchDomains:
      description:
      - DNS search domains
      type: list
      required: false
      default: []
    externallyVisibleIp:
      description:
      - IP that external sites see when headnode connects
      type: str
      required: false
      default: 0.0.0.0
    externalNetwork:
      description:
      - The external network
      type: str
      required: false
    defaultCategory:
      description:
      - Default category for new nodes
      type: str
      required: false
    archOS:
      description:
      - Architecture operating system
      type: list
      required: false
      default: []
      elements: dict
      options:
        arch:
          description:
          - Architecture
          type: str
          required: false
          default: x86_64
          choices:
          - x86_64
          - aarch64
        os:
          description:
          - Operating system
          type: str
          required: false
          default: rhel9
          choices:
          - rhel8
          - sles15
          - ubuntu2004
          - ubuntu2204
          - rhel9
          - ubuntu2404
        primaryImage:
          description:
          - Image used to boot new nodes and keep /cm/shared up to date, empty if head
            node is to be used
          type: str
          required: false
        shared:
          description:
          - Shared directory
          type: str
          required: false
        installer:
          description:
          - Node installer
          type: str
          required: false
        priority:
          description:
          - Priority
          type: int
          required: false
          default: 0
    burnConfigs:
      description:
      - Available burn configurations
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - A short name to identify this burn configuration.
          type: str
          required: true
        description:
          description:
          - A more extensive description of this burn configuration.
          type: str
          required: false
        configuration:
          description:
          - This XML data describes which burn tests should be used.
          type: str
          required: false
    failoverGroups:
      description:
      - Failover group configurations
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        nodes:
          description:
          - List of nodes belonging to this group
          type: list
          required: false
          default: []
        alsoTakeOverAfterGraciousShutdown:
          description:
          - Also perform automatic failover if the active group member was gracefully
            shut down
          type: bool
          required: false
          default: false
        disableAutomaticFailover:
          description:
          - When automatic failover is disabled the no node in the group will not take
            over if the active node is dead
          type: bool
          required: false
          default: false
        warntime:
          description:
          - How quickly to issue a 'late' warning
          type: int
          required: false
          default: 5
        deadtime:
          description:
          - How quickly to decide that a node in a group is dead
          type: int
          required: false
          default: 10
        mountScript:
          description:
          - Script that mounts the shared storage device when a node becomes the active
            head node
          type: str
          required: false
        unmountScript:
          description:
          - Script that unmounts the shared storage device when a node stoppes being the
            active head node
          type: str
          required: false
        preFailoverScript:
          description:
          - Prefailover script will be run on all nodes before failover has begun
          type: str
          required: false
        postFailoverScript:
          description:
          - Postfailover script will be run on all nodes after failover has completed
          type: str
          required: false
        ipTakeOverMethod:
          description:
          - The manner in which shared IP gets transferred
          type: str
          required: false
          default: ARP
          choices:
          - ARP
          - SCRIPT
          - CLOUD
          - LOAD_BALANCER
        ipTakeOverScript:
          description:
          - Shared IP transfer script
          type: str
          required: false
    resourcePools:
      description:
      - Resource pools
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        nodes:
          description:
          - List of nodes who share the resources
          type: list
          required: false
          default: []
        configurationOverlay:
          description:
          - Configuration overlay which defines the nodes that share the resources
          type: str
          required: false
        priority:
          description:
          - Distribution priorities for the nodes
          type: list
          required: false
          default: []
        hostname:
          description:
          - Hostname all IP resources will point to
          type: str
          required: false
        waitTime:
          description:
          - How long to wait after a node goes down before migrating it's resources
          type: int
          required: false
          default: 5
        disabled:
          description:
          - Disabled the entire resource pool
          type: bool
          required: false
          default: false
        generateDNSZone:
          description:
          - Specify which DNS zones should be written
          type: str
          required: false
          default: BOTH
          choices:
          - BOTH
          - FORWARD
          - REVERSE
          - NEITHER
        resources_IPResource:
          description:
          - Resources to be divided among the given nodes
          type: list
          required: false
          default: []
          elements: dict
          options:
            name:
              description:
              - Name
              type: str
              required: true
            dependency:
              description:
              - Dependency on another resource, run this resource on the same node as
                the dependency
              - (Field should be formatted as a UUID)
              type: str
              required: false
              default: 00000000-0000-0000-0000-000000000000
            exclude:
              description:
              - Do not run this resource on any node running one of the excluded resources
              - (Field elements should be formatted as a UUID)
              type: list
              required: false
              default: '[]'
            disabled:
              description:
              - Disable the resource from being given to any node
              type: bool
              required: false
              default: false
            stopOnRemove:
              description:
              - Automatically stop resource when removed
              type: bool
              required: false
              default: true
            ip:
              description:
              - IP
              type: str
              required: false
              default: 0.0.0.0
            networkDeviceName:
              description:
              - The network device name to start this IP on. Leave blank to automatically
                determine based on IP.
              type: str
              required: false
            alias:
              description:
              - The network device name alias
              type: str
              required: false
            timeout:
              description:
              - Timeout
              type: int
              required: false
              default: 5
        resources_GenericResource:
          description:
          - Resources to be divided among the given nodes
          type: list
          required: false
          default: []
          elements: dict
          options:
            name:
              description:
              - Name
              type: str
              required: true
            dependency:
              description:
              - Dependency on another resource, run this resource on the same node as
                the dependency
              - (Field should be formatted as a UUID)
              type: str
              required: false
              default: 00000000-0000-0000-0000-000000000000
            exclude:
              description:
              - Do not run this resource on any node running one of the excluded resources
              - (Field elements should be formatted as a UUID)
              type: list
              required: false
              default: '[]'
            disabled:
              description:
              - Disable the resource from being given to any node
              type: bool
              required: false
              default: false
            stopOnRemove:
              description:
              - Automatically stop resource when removed
              type: bool
              required: false
              default: true
            activateScript:
              description:
              - Script to be executed when the resource is given to a node
              type: str
              required: false
            deactivateScript:
              description:
              - Script to be executed when the resource is taken a way from a node
              type: str
              required: false
            checkScript:
              description:
              - Script to be executed periodically to verify the resource is still running
              type: str
              required: false
            arguments:
              description:
              - Arguments to pass to the script
              type: list
              required: false
              default: []
            scriptTimeout:
              description:
              - Script timeout
              type: int
              required: false
              default: 15
    defaultBurnConfig:
      description:
      - Default burn configuration
      type: str
      required: false
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
    dpuSettings:
      description:
      - Configure the DPU settings
      type: dict
      required: false
      options:
        operation_mode:
          description:
          - Operation mode
          type: str
          required: false
          default: NIC_MODE
          choices:
          - NIC_MODE
          - DPU_MODE
        display_level:
          description:
          - Display level
          type: str
          required: false
          default: BASIC
          choices:
          - BASIC
          - ADVANCED
          - LOG
        boot_mode:
          description:
          - Boot mode
          type: str
          required: false
          default: EMMC
          choices:
          - RSHIM
          - EMMC
          - EMMC_BOOT_SWAP
        drop_mode:
          description:
          - Drop mode
          type: str
          required: false
          default: NORMAL
          choices:
          - NORMAL
          - DROP
        boot_timeout:
          description:
          - Boot timeout
          type: int
          required: false
          default: 100
        boot_order:
          description:
          - Boot order
          type: list
          required: false
          default:
          - NET-OOB-IPV4
          - DISK
        interface_mode_port1:
          description:
          - Interface mode port 1
          type: str
          required: false
          default: ETH
          choices:
          - IB
          - ETH
        interface_mode_port2:
          description:
          - Interface mode port 2
          type: str
          required: false
          default: ETH
          choices:
          - IB
          - ETH
        hw_offload:
          description:
          - Offload OVS to hardware
          type: bool
          required: false
          default: true
        keyValueSettings:
          description:
          - Key value settings which can be passed to the DPU manage script
          type: dict
          required: false
          options:
            keyValues:
              description:
              - List of key=value pairs
              type: list
              required: false
              default: []
    ztpSettings:
      description:
      - Configure the ZTP settings
      type: dict
      required: false
      options:
        ztpScriptTemplate:
          description:
          - ZTP script template
          type: str
          required: false
          default: cumulus-ztp.sh
        ztpJsonTemplate:
          description:
          - ZTP JSON template for NVOS
          type: str
          required: false
        switchImage:
          description:
          - Image loaded via ONIE
          type: str
          required: false
        checkImageOnBoot:
          description:
          - Check image matches on boot, if not clear switch and start from scratch
          type: bool
          required: false
          default: false
        runZtpOnEachBoot:
          description:
          - Run ZTP on each boot
          type: bool
          required: false
          default: true
        watchDisabledZtp:
          description:
          - Watch switch with potential disabled ZTP
          type: bool
          required: false
          default: false
        installLiteDaemon:
          description:
          - Install lite daemon during ZTP
          type: bool
          required: false
          default: true
        authorizedKeyFileRoot:
          description:
          - Authorized key file to be copied for root user
          type: str
          required: false
        authorizedKeyFileCumulus:
          description:
          - Authorized key file to be copied for cumulus user
          type: str
          required: false
        authorizedKeyFileAdmin:
          description:
          - Authorized key file to be copied for admin user
          type: str
          required: false
        enableAPI:
          description:
          - Enable access to API
          type: bool
          required: false
          default: false
        enableExternalAccessAPI:
          description:
          - Enable external access to API instead of only localhost
          type: bool
          required: false
          default: false
        updateEtcHosts:
          description:
          - Update the /etc/hosts with the BCM master entry
          type: bool
          required: false
          default: false
        firmwares:
          description:
          - List of firmwares to check and install
          type: list
          required: false
          default: []
        preInstallScripts:
          description:
          - List of scripts executed at the start of ZTP
          type: list
          required: false
          default: []
        postInstallScripts:
          description:
          - List of scripts executed at the end of ZTP
          type: list
          required: false
          default: []
        ptmTopologyFile:
          description: []
          type: str
          required: false
        mergeKeyValueSettingsPartition:
          description:
          - Merge key value settings partition
          type: bool
          required: false
          default: false
        keyValueSettings:
          description:
          - Key value settings which can be passed to the ZTP script
          type: dict
          required: false
          options:
            keyValues:
              description:
              - List of key=value pairs
              type: list
              required: false
              default: []
        extra_values:
          description: []
          type: json
          required: false
    ztpNewSwitchSettings:
      description:
      - Configure the ZTP settings
      type: dict
      required: false
      options:
        ztpScriptTemplate:
          description:
          - ZTP script template for new switches
          type: str
          required: false
          default: new-switch-ztp.sh
        switchImage:
          description:
          - Image loaded via ONIE
          type: str
          required: false
        keyValueSettings:
          description:
          - Key value settings which can be passed to the ZTP script
          type: dict
          required: false
          options:
            keyValues:
              description:
              - List of key=value pairs
              type: list
              required: false
              default: []
    seLinuxSettings:
      description:
      - Configure the SELinux settings
      type: dict
      required: false
      options:
        initialize:
          description:
          - Determines whether SELinux is to be initialized by the node installer
          type: bool
          required: false
          default: true
        rebootAfterContextRestore:
          description:
          - This directive determines whether the compute node is to reboot after performing
            a full filesystem security context restore
          type: bool
          required: false
          default: false
        allowNFSHomeDirectories:
          description:
          - This directive determines whether to allow using a remote NFS server for the
            home directories on the node
          type: bool
          required: false
          default: true
        contextActionAutoInstall:
          description:
          - This directive specifies the action which is to be performed by the Node Installer
            when the node is being installed in the AUTO mode
          type: str
          required: false
          default: AUTO
          choices:
          - AUTO
          - OS
          - ALWAYS
          - CHECK
        contextActionFullInstall:
          description:
          - This directive specifies the action which is to be performed by the Node Installer
            when the node is being installed in the FULL mode
          type: str
          required: false
          default: AUTO
          choices:
          - AUTO
          - OS
          - ALWAYS
          - CHECK
        contextActionNoSyncInstall:
          description:
          - This directive specifies the action which is to be performed by the Node Installer
            when the node is being installed in the NOSYNC mode
          type: str
          required: false
          default: ALWAYS
          choices:
          - AUTO
          - OS
          - ALWAYS
          - CHECK
        mode:
          description:
          - Process policy mode
          type: str
          required: false
          default: PERMISSIVE
          choices:
          - ENFORCING
          - PERMISSIVE
          - DISABLED
        policy:
          description:
          - Process protection policy
          type: str
          required: false
          default: TARGETED
          choices:
          - TARGETED
          - MINIMUM
          - MLS
        keyValueSettings:
          description:
          - Key value settings which can be used to override SELinux options
          type: dict
          required: false
          options:
            keyValues:
              description:
              - List of key=value pairs
              type: list
              required: false
              default: []
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
    netQSettings:
      description:
      - Configure NetQ settings
      type: dict
      required: false
      options:
        server:
          description:
          - NetQ server
          type: str
          required: false
        username:
          description:
          - Username to use for NetQ API calls
          type: str
          required: false
        password:
          description:
          - Password to use for NetQ API calls
          type: str
          required: false
        port:
          description:
          - Port
          type: int
          required: false
          default: 443
        verifySSL:
          description:
          - Verify SSL host certificate
          type: bool
          required: false
          default: false
        cacert:
          description:
          - The CA certificate of the server
          type: str
          required: false
        certificate:
          description:
          - The certificate used to connect to the server
          type: str
          required: false
        privateKey:
          description:
          - The certificate private key used to connect to the server
          type: str
          required: false
        nodes:
          description:
          - List of nodes that can be used as server
          type: list
          required: false
          default: []
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
    ufmSettings:
      description:
      - Configure UFM settings
      type: dict
      required: false
      options:
        server:
          description:
          - UFM server
          type: str
          required: false
        username:
          description:
          - Username to use for UFM API calls
          type: str
          required: false
        password:
          description:
          - Password to use for UFM API calls
          type: str
          required: false
        port:
          description:
          - Port
          type: int
          required: false
          default: 443
        verifySSL:
          description:
          - Verify SSL host certificate
          type: bool
          required: false
          default: false
        cacert:
          description:
          - The CA certificate of the server
          type: str
          required: false
        certificate:
          description:
          - The certificate used to connect to the server
          type: str
          required: false
        privateKey:
          description:
          - The certificate private key used to connect to the server
          type: str
          required: false
        nodes:
          description:
          - List of nodes that can be used as server
          type: list
          required: false
          default: []
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
    nmxmSettings:
      description:
      - Configure NMX Manager settings
      type: dict
      required: false
      options:
        server:
          description:
          - NMX-M server
          type: str
          required: false
        username:
          description:
          - Username to use for NMX-M API calls
          type: str
          required: false
        password:
          description:
          - Password to use for NMX-M API calls
          type: str
          required: false
        port:
          description:
          - Port
          type: int
          required: false
          default: 443
        verifySSL:
          description:
          - Verify SSL host certificate
          type: bool
          required: false
          default: false
        cacert:
          description:
          - The CA certificate of the server
          type: str
          required: false
        certificate:
          description:
          - The certificate used to connect to the server
          type: str
          required: false
        privateKey:
          description:
          - The certificate private key used to connect to the server
          type: str
          required: false
        nodes:
          description:
          - List of nodes that can be used as server
          type: list
          required: false
          default: []
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
    managementNetwork:
      description:
      - Determines what network should be used for management traffic.
      type: str
      required: false
    notes:
      description:
      - Administrator notes
      type: str
      required: false
    provisioningSettings:
      description:
      - Configure the provisioning settings
      type: dict
      required: false
      options:
        dirtyAutoUpdateTimeout:
          description:
          - Delay after which a provisioning node is considered out of date and automatically
            updated when needed (0 to disable automatic updates)
          type: int
          required: false
          default: 300
        autoUpdatePeriod:
          description:
          - Period after which all provisioning nodes are automatically updated (0 to
            disable automatic updates)
          type: int
          required: false
          default: 86400
        noRestartRequiredPeriod:
          description:
          - Period in which a second request doesn't require a restart of a recently started
            rsync
          type: int
          required: false
          default: 10
        minimalLoadForOffload:
          description:
          - Minimal provisioning load on the active head node before which dirty provisioning
            nodes are updated
          type: float
          required: false
          default: 0.25
        headNodeLoadMultiplier:
          description:
          - Load multiplier to reduce the work for the head node and offload more to the
            provisioning nodes
          type: float
          required: false
          default: 0.25
        useGNSSLocationData:
          description:
          - Use GNSS location data where available to find and prefer the closest provisioning
            node
          type: bool
          required: false
          default: true
    relayHost:
      description:
      - SMTP mail relay host
      type: str
      required: false
    noZeroConf:
      description:
      - Add nozeroconf to network configuration
      type: bool
      required: false
      default: false
    proxySettings:
      description:
      - Configure the proxy server settings
      type: dict
      required: false
      options:
        proxyHttp:
          description:
          - HTTP proxy address which will be used for the node connections to HTTP resources
          type: str
          required: false
        proxyHttpUser:
          description:
          - HTTP proxy username for authentication
          type: str
          required: false
        proxyHttpPass:
          description:
          - HTTP proxy password for authentication
          type: str
          required: false
        proxyHttps:
          description:
          - HTTPS proxy address which will be used for the node connections to HTTPS resources
          type: str
          required: false
        proxyHttpsUser:
          description:
          - HTTPS proxy username for authentication
          type: str
          required: false
        proxyHttpsPass:
          description:
          - HTTPS proxy password for authentication
          type: str
          required: false
        proxyFtp:
          description:
          - FTP proxy address which will be used for the node connections to FTP resources
          type: str
          required: false
        proxyFtpUser:
          description:
          - FTP proxy username for authentication
          type: str
          required: false
        proxyFtpPass:
          description:
          - FTP proxy password for authentication
          type: str
          required: false
        noProxy:
          description:
          - Hosts to be accessed without proxy
          type: list
          required: false
          default: []
    wlmJobPowerUsageSettings:
      description:
      - Configure the Wlm job power usage settings
      type: dict
      required: false
      options:
        disabled:
          description:
          - Disable power usage calculation
          type: bool
          required: false
          default: false
        jobAge:
          description:
          - Job complation age before power is calculated
          type: int
          required: false
          default: 300
        timeout:
          description:
          - Plot timeout
          type: int
          required: false
          default: 30
        nodePowerMetrics:
          description:
          - Preference of metrics to use for calculating the power usage for the entire
            node
          type: list
          required: false
          default: []
        gpuPowerMetrics:
          description:
          - Preference of metrics to use for calculating the GPU power usage
          type: list
          required: false
          default: []
        cpuPowerMetrics:
          description:
          - Preference of metrics to use for calculating the CPU power usage
          type: list
          required: false
          default: []
        powerUnderAllocationMetrics:
          description:
          - All metrics that indicate if a device was allocated insufficient power
          type: list
          required: false
          default: []
    leakActionPolicies:
      description:
      - Leak action policies
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        rules:
          description:
          - Rules for this policy
          type: list
          required: false
          default: []
          elements: dict
          options:
            name:
              description:
              - Name
              type: str
              required: true
            scope:
              description:
              - Scope of the leak action rule
              type: str
              required: false
              default: RACK
              choices:
              - DEVICE
              - RACK
              - CDU
              - ROW
              - ROOM
              - BUILDING
              - LOCATION
            disabled:
              description:
              - Disable the rule
              type: bool
              required: false
              default: false
            minimalDevices:
              description:
              - Minimal devices that need to report leaks before the rule to become active
              type: int
              required: false
              default: 1
            maximalDevices:
              description:
              - Maximal devices that are allowed to report leaks before the rule to become
                inactive
              type: int
              required: false
              default: 100
            gracePeriod:
              description:
              - Delay since the rule becomes active before running the actions
              type: int
              required: false
              default: 0
            correlationWindow:
              description:
              - Temporal window in which two separate leaks are considered correlated
              type: int
              required: false
              default: 300
            powerOff:
              description:
              - Power off devices in the scope of the rule
              type: bool
              required: false
              default: true
            powerOffRack:
              description:
              - Power off all devices in the scope of the rule, via rack power operation
                and fallback to per device
              type: bool
              required: false
              default: false
            electricalIsolation:
              description:
              - Electrically isolate the devices in the scope of the rule
              type: bool
              required: false
              default: false
            liquidIsolation:
              description:
              - Liquid isolate the devices in the scope of the rule
              type: bool
              required: false
              default: false
            minimalSeverity:
              description:
              - Minimal severity that need to report leaks before the rule to become active
              type: int
              required: false
              default: 1
            maximalSeverity:
              description:
              - Maximal severity that is allowed to report leaks before the rule to become
                inactive
              type: int
              required: false
              default: 100
    activeLeakActionPolicy:
      description:
      - Active leak action policy
      type: str
      required: false
    autosign:
      description:
      - Sign certificates for node installer request according to network settings.
      type: str
      required: false
      default: AUTO
      choices:
      - AUTO
      - MANUAL
    bms:
      description:
      - Specify the type of BMS
      type: str
      required: false
      default: CRONUS
      choices:
      - CRONUS
      - PIPE
      - FILE
      - URL
    bmsPath:
      description:
      - The path/url used to push information to BMS
      type: str
      required: false
    bmsCertificate:
      description:
      - The certificate used to push information to BMS url
      type: str
      required: false
    bmsPrivateKey:
      description:
      - The private key used to push information to BMS url
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

requirements: [cmdaemon-pythoncm, deepdiff, python-box]
author:
- iiiteam <iiiteam@brightcomputing.com>
"""

EXAMPLES = r"""

"""

RETURN = r"""
---
partition:
  type: complex
  description: Partition
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
    name:
      type: str
      description: Partition name
      returned: success
    clusterName:
      type: str
      description: Cluster name
      returned: success
    clusterReferenceArchitecture:
      type: str
      description: Description of the cluster architecture
      returned: success
    primaryHeadNode:
      type: complex
      description: Primary head node
      returned: success
    failover:
      type: complex
      description: Manage failover setup for this cluster
      returned: success
    timeZoneSettings:
      type: complex
      description: Time zone
      returned: success
    adminEmail:
      type: str
      description: Administrator email
      returned: success
    slaveName:
      type: str
      description: Default prefix to identify nodes. eg node003 (basename = node)
      returned: success
    slaveDigits:
      type: int
      description: Number of digits used to identify nodes. eg node003 (digits = 3)
      returned: success
    nameServers:
      type: str
      description: Name servers
      returned: success
    nameServersFromDhcp:
      type: str
      description: Name servers provided by DHCP, edit the name servers property instead
      returned: success
    timeServers:
      type: str
      description: NTP time servers
      returned: success
    searchDomains:
      type: str
      description: DNS search domains
      returned: success
    externallyVisibleIp:
      type: str
      description: IP that external sites see when headnode connects
      returned: success
    externalNetwork:
      type: complex
      description: The external network
      returned: success
    defaultCategory:
      type: complex
      description: Default category for new nodes
      returned: success
    archOS:
      type: list
      description: Architecture operating system
      returned: success
    burnConfigs:
      type: list
      description: Available burn configurations
      returned: success
    failoverGroups:
      type: list
      description: Failover group configurations
      returned: success
    resourcePools:
      type: list
      description: Resource pools
      returned: success
    defaultBurnConfig:
      type: complex
      description: Default burn configuration
      returned: success
    bmcSettings:
      type: complex
      description: Configure the baseboard management controller settings
      returned: success
    snmpSettings:
      type: complex
      description: Configure the cluster wide SNMP settings
      returned: success
    dpuSettings:
      type: complex
      description: Configure the DPU settings
      returned: success
    ztpSettings:
      type: complex
      description: Configure the ZTP settings
      returned: success
    ztpNewSwitchSettings:
      type: complex
      description: Configure the ZTP settings
      returned: success
    seLinuxSettings:
      type: complex
      description: Configure the SELinux settings
      returned: success
    accessSettings:
      type: complex
      description: Configure the cluster wide Access settings
      returned: success
    netQSettings:
      type: complex
      description: Configure NetQ settings
      returned: success
    ufmSettings:
      type: complex
      description: Configure UFM settings
      returned: success
    nmxmSettings:
      type: complex
      description: Configure NMX Manager settings
      returned: success
    managementNetwork:
      type: complex
      description: Determines what network should be used for management traffic.
      returned: success
    notes:
      type: str
      description: Administrator notes
      returned: success
    provisioningSettings:
      type: complex
      description: Configure the provisioning settings
      returned: success
    relayHost:
      type: str
      description: SMTP mail relay host
      returned: success
    noZeroConf:
      type: bool
      description: Add nozeroconf to network configuration
      returned: success
    proxySettings:
      type: complex
      description: Configure the proxy server settings
      returned: success
    wlmJobPowerUsageSettings:
      type: complex
      description: Configure the Wlm job power usage settings
      returned: success
    leakActionPolicies:
      type: list
      description: Leak action policies
      returned: success
    activeLeakActionPolicy:
      type: complex
      description: Active leak action policy
      returned: success
    autosign:
      type: str
      description: Sign certificates for node installer request according to network
        settings.
      returned: success
    bms:
      type: str
      description: Specify the type of BMS
      returned: success
    bmsPath:
      type: str
      description: The path/url used to push information to BMS
      returned: success
    bmsCertificate:
      type: str
      description: The certificate used to push information to BMS url
      returned: success
    bmsPrivateKey:
      type: str
      description: The private key used to push information to BMS url
      returned: success
    prometheusMetricForwarders:
      type: list
      description: Prometheus metric forwarders
      returned: success

"""
############################
# Imports
############################

from copy import deepcopy
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import Partition
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
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.argspecs.partition import Partition_ArgSpec

############################
# main
############################

def main():

    module = BaseModule(
        argument_spec=Partition_ArgSpec.argument_spec,
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

    entity = entity_manager.lookup_entity(params, Partition)

    changed = False

    diff = None

    desired_state = params["state"]

    if not entity:
        if desired_state == "present":
            entity, res = entity_manager.create_resource(Partition, params, commit=not module.check_mode)
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