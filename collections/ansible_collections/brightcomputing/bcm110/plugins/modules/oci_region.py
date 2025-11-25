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
module: oci_region
description: ['Manages oci_regions']
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
      - The name of the cloud region.
      type: str
      required: true
    provider:
      description:
      - Cloud provider
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

requirements: [cmdaemon-pythoncm, deepdiff, python-box]
author:
- iiiteam <iiiteam@brightcomputing.com>
"""

EXAMPLES = r"""

"""

RETURN = r"""
---
oci_region:
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
    name:
      type: str
      description: The name of the cloud region.
      returned: success
    provider:
      type: complex
      description: Cloud provider
      returned: success
    timeZoneSettings:
      type: complex
      description: Time zone
      returned: success

"""
############################
# Imports
############################

from copy import deepcopy
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import OCIRegion
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
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.argspecs.oci_region import OCIRegion_ArgSpec

############################
# main
############################

def main():

    module = BaseModule(
        argument_spec=OCIRegion_ArgSpec.argument_spec,
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

    entity = entity_manager.lookup_entity(params, OCIRegion)

    changed = False

    diff = None

    desired_state = params["state"]

    if not entity:
        if desired_state == "present":
            entity, res = entity_manager.create_resource(OCIRegion, params, commit=not module.check_mode)
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