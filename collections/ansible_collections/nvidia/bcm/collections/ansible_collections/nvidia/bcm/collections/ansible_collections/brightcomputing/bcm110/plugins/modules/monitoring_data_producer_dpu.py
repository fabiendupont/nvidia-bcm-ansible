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
module: monitoring_data_producer_dpu
description: ['Manages monitoring_data_producer_dpus']
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
      - Name
      type: str
      required: true
    description:
      description:
      - Description
      type: str
      required: false
    notes:
      description:
      - Administrator notes
      type: str
      required: false
    when:
      description:
      - When the producer should run
      type: str
      required: false
      default: TIMED
      choices:
      - TIMED
      - ONDEMAND
      - OOB
      - ONSTART
    preJob:
      description:
      - Run as pre job in prolog
      type: bool
      required: false
      default: false
    postJob:
      description:
      - Run as post job in epilog
      type: bool
      required: false
      default: false
    maxAge:
      description:
      - Maximal age of historic data, 0 for infinite
      type: float
      required: false
      default: 0.0
    maxSamples:
      description:
      - Maximal samples of historic data, 0 for infinite
      type: int
      required: false
      default: 4096
    interval:
      description:
      - Sampling interval
      type: float
      required: false
      default: 120.0
    offset:
      description:
      - Time offset for sampling interval
      type: float
      required: false
      default: 0.0
    startupDelay:
      description:
      - Delay the first sampling the specified time after cmd starts
      type: float
      required: false
      default: 0.0
    intervals:
      description:
      - Out of band sampling interval
      type: list
      required: false
      default: []
    gap:
      description:
      - Number of missed samples before we add a NaN
      type: int
      required: false
      default: 0
    fuzzyOffset:
      description:
      - Automatic fuzzy offset factor [0-1]. Multiplied by interval
      type: float
      required: false
      default: 0.0
    introduceNaN:
      description:
      - Introduce NaN if device goes up/down/up
      type: bool
      required: false
      default: true
    maxMeasurables:
      description:
      - Maximal number of measurables the producer can introduce
      type: int
      required: false
      default: 512
    automaticReinitialize:
      description:
      - Automatic run --initialize when a new metric has been detected
      type: bool
      required: false
      default: true
    disabled:
      description:
      - Disabled
      type: bool
      required: false
      default: false
    disableTriggers:
      description:
      - Disable triggers from being evaluated
      type: bool
      required: false
      default: false
    disableOnHighLoad:
      description:
      - Disable when nodes are very busy
      type: bool
      required: false
      default: false
    consolidator:
      description:
      - Consolidator configuration
      type: str
      required: false
    suppressedByGoingDown:
      description:
      - Suppress running action if device is going down
      type: bool
      required: false
      default: false
    access:
      description:
      - User access control
      type: str
      required: false
      default: PUBLIC
      choices:
      - PUBLIC
      - PRIVATE
      - INDIVIDUAL
    associatedUser:
      description:
      - User associated with this measurable
      type: str
      required: false
    dpuSettings:
      description:
      - Submode containing DPU settings
      type: dict
      required: false
      options:
        enable_pcie0:
          description:
          - Enable pcie0 metrics
          type: bool
          required: false
          default: false
        enable_pcie1:
          description:
          - Enable pcie0 metrics
          type: bool
          required: false
          default: false
        enable_ecc:
          description:
          - Enable ecc metrics
          type: bool
          required: false
          default: true
        configured_events_MonitoringDataProducerDPUSettingsEventGic:
          description:
          - Configured of the event
          type: list
          required: false
          default: []
          elements: dict
          options:
            index:
              description:
              - Index
              type: int
              required: false
              default: 0
            counter:
              description:
              - Counter
              type: int
              required: false
              default: 0
            event:
              description:
              - Event value from the event list that will be sampled
              type: str
              required: false
              default: DISABLED
              choices:
              - AW_REQ
              - AW_BEATS
              - AW_TRANS
              - AW_RESP
              - AW_STL
              - AW_LAT
              - AW_REQ_TBU
              - AR_REQ
              - AR_BEATS
              - AR_TRANS
              - AR_STL
              - AR_LAT
              - AR_REQ_TBU
              - TBU_MISS
              - TX_DAT_AF
              - RX_DAT_AF
              - RETRYQ_CRED
              - DISABLED
        configured_events_MonitoringDataProducerDPUSettingsEventSmmu:
          description:
          - Configured of the event
          type: list
          required: false
          default: []
          elements: dict
          options:
            index:
              description:
              - Index
              type: int
              required: false
              default: 0
            counter:
              description:
              - Counter
              type: int
              required: false
              default: 0
            event:
              description:
              - Event value from the event list that will be sampled
              type: str
              required: false
              default: DISABLED
              choices:
              - AW_REQ
              - AW_BEATS
              - AW_TRANS
              - AW_RESP
              - AW_STL
              - AW_LAT
              - AW_REQ_TBU
              - AR_REQ
              - AR_BEATS
              - AR_TRANS
              - AR_STL
              - AR_LAT
              - AR_REQ_TBU
              - TBU_MISS
              - TX_DAT_AF
              - RX_DAT_AF
              - RETRYQ_CRED
              - DISABLED
        configured_events_MonitoringDataProducerDPUSettingsEventTriogen:
          description:
          - Configured of the event
          type: list
          required: false
          default: []
          elements: dict
          options:
            index:
              description:
              - Index
              type: int
              required: false
              default: 0
            counter:
              description:
              - Counter
              type: int
              required: false
              default: 0
            event:
              description:
              - Event value from the event list that will be sampled
              type: str
              required: false
              default: DISABLED
              choices:
              - AW_REQ
              - AW_BEATS
              - AW_TRANS
              - AW_RESP
              - AW_STL
              - AW_LAT
              - AW_REQ_TBU
              - AR_REQ
              - AR_BEATS
              - AR_TRANS
              - AR_STL
              - AR_LAT
              - AR_REQ_TBU
              - TBU_MISS
              - TX_DAT_AF
              - RX_DAT_AF
              - RETRYQ_CRED
              - DISABLED
        configured_events_MonitoringDataProducerDPUSettingsEventTile:
          description:
          - Configured of the event
          type: list
          required: false
          default: []
          elements: dict
          options:
            index:
              description:
              - Index
              type: int
              required: false
              default: 0
            counter:
              description:
              - Counter
              type: int
              required: false
              default: 0
            event:
              description:
              - Event value from the event list that will be sampled
              type: str
              required: false
              default: DISABLED
              choices:
              - HNF_REQUESTS
              - HNF_REJECTS
              - ALL_BUSY
              - MAF_BUSY
              - MAF_REQUESTS
              - RNF_REQUESTS
              - REQUEST_TYPE
              - MEMORY_READS
              - MEMORY_WRITES
              - VICTIM_WRITE
              - POC_FULL
              - POC_FAIL
              - POC_SUCCESS
              - POC_WRITES
              - POC_READS
              - FORWARD
              - RXREQ_HNF
              - RXRSP_HNF
              - RXDAT_HNF
              - TXREQ_HNF
              - TXRSP_HNF
              - TXDAT_HNF
              - TXSNP_HNF
              - INDEX_MATCH
              - A72_ACCESS
              - IO_ACCESS
              - TSO_WRITE
              - TSO_CONFLICT
              - DIR_HIT
              - HNF_ACCEPTS
              - REQ_BUF_EMPTY
              - REQ_BUF_IDLE_MAF
              - TSO_NOARB
              - TSO_NOARB_CYCLES
              - MSS_NO_CREDIT
              - TXDAT_NO_LCRD
              - TXSNP_NO_LCRD
              - TXRSP_NO_LCRD
              - TXREQ_NO_LCRD
              - TSO_CL_MATCH
              - MEMORY_READS_BYPASS
              - TSO_NOARB_TIMEOUT
              - ALLOCATE
              - VICTIM
              - A72_WRITE
              - A72_READ
              - IO_WRITE
              - IO_READ
              - TSO_REJECT
              - TXREQ_RN
              - TXRSP_RN
              - TXDAT_RN
              - RXSNP_RN
              - RXRSP_RN
              - RXDAT_RN
              - DISABLED
        configured_events_MonitoringDataProducerDPUSettingsEventL3CacheHalf:
          description:
          - Configured of the event
          type: list
          required: false
          default: []
          elements: dict
          options:
            index:
              description:
              - Index
              type: int
              required: false
              default: 0
            counter:
              description:
              - Counter
              type: int
              required: false
              default: 0
            event:
              description:
              - Event value from the event list that will be sampled
              type: str
              required: false
              default: DISABLED
              choices:
              - DISABLED
              - CYCLES
              - TOTAL_RD_REQ_IN
              - TOTAL_WR_REQ_IN
              - TOTAL_WR_DBID_ACK
              - TOTAL_WR_DATA_IN
              - TOTAL_WR_COMP
              - TOTAL_RD_DATA_OUT
              - TOTAL_CDN_REQ_IN_BANK0
              - TOTAL_CDN_REQ_IN_BANK1
              - TOTAL_DDN_REQ_IN_BANK0
              - TOTAL_DDN_REQ_IN_BANK1
              - TOTAL_EMEM_RD_RES_IN_BANK0
              - TOTAL_EMEM_RD_RES_IN_BANK1
              - TOTAL_CACHE_RD_RES_IN_BANK0
              - TOTAL_CACHE_RD_RES_IN_BANK1
              - TOTAL_EMEM_RD_REQ_BANK0
              - TOTAL_EMEM_RD_REQ_BANK1
              - TOTAL_EMEM_WR_REQ_BANK0
              - TOTAL_EMEM_WR_REQ_BANK1
              - TOTAL_RD_REQ_OUT
              - TOTAL_WR_REQ_OUT
              - TOTAL_RD_RES_IN
              - HITS_BANK0
              - HITS_BANK1
              - MISSES_BANK0
              - MISSES_BANK1
              - ALLOCATIONS_BANK0
              - ALLOCATIONS_BANK1
              - EVICTIONS_BANK0
              - EVICTIONS_BANK1
              - DBID_REJECT
              - WRDB_REJECT_BANK0
              - WRDB_REJECT_BANK1
              - CMDQ_REJECT_BANK0
              - CMDQ_REJECT_BANK1
              - COB_REJECT_BANK0
              - COB_REJECT_BANK1
              - TRB_REJECT_BANK0
              - TRB_REJECT_BANK1
              - TAG_REJECT_BANK0
              - TAG_REJECT_BANK1
              - ANY_REJECT_BANK0
              - ANY_REJECT_BANK1
        configured_events_MonitoringDataProducerDPUSettingsEventTrio:
          description:
          - Configured of the event
          type: list
          required: false
          default: []
          elements: dict
          options:
            index:
              description:
              - Index
              type: int
              required: false
              default: 0
            counter:
              description:
              - Counter
              type: int
              required: false
              default: 0
            event:
              description:
              - Event value from the event list that will be sampled
              type: str
              required: false
              default: DISABLED
              choices:
              - TPIO_DATA_BEAT
              - TDMA_DATA_BEAT
              - MAP_DATA_BEAT
              - TXMSG_DATA_BEAT
              - TPIO_DATA_PACKET
              - TDMA_DATA_PACKET
              - MAP_DATA_PACKET
              - TXMSG_DATA_PACKET
              - TDMA_RT_AF
              - TDMA_PBUF_MAC_AF
              - TRIO_MAP_WRQ_BUF_EMPTY
              - TRIO_MAP_CPL_BUF_EMPTY
              - TRIO_MAP_RDQ0_BUF_EMPTY
              - TRIO_MAP_RDQ1_BUF_EMPTY
              - TRIO_MAP_RDQ2_BUF_EMPTY
              - TRIO_MAP_RDQ3_BUF_EMPTY
              - TRIO_MAP_RDQ4_BUF_EMPTY
              - TRIO_MAP_RDQ5_BUF_EMPTY
              - TRIO_MAP_RDQ6_BUF_EMPTY
              - TRIO_MAP_RDQ7_BUF_EMPTY
              - TRIO_RING_TX_FLIT_CH0
              - TRIO_RING_TX_FLIT_CH1
              - TRIO_RING_TX_FLIT_CH2
              - TRIO_RING_TX_FLIT_CH3
              - TRIO_RING_TX_FLIT_CH4
              - TRIO_RING_RX_FLIT_CH0
              - TRIO_RING_RX_FLIT_CH1
              - TRIO_RING_RX_FLIT_CH2
              - TRIO_RING_RX_FLIT_CH3
              - DISABLED
        configured_events_MonitoringDataProducerDPUSettingsEventTilenet:
          description:
          - Configured of the event
          type: list
          required: false
          default: []
          elements: dict
          options:
            index:
              description:
              - Index
              type: int
              required: false
              default: 0
            counter:
              description:
              - Counter
              type: int
              required: false
              default: 0
            event:
              description:
              - Event value from the event list that will be sampled
              type: str
              required: false
              default: DISABLED
              choices:
              - CDN_REQ
              - DDN_REQ
              - NDN_REQ
              - CDN_DIAG_N_OUT_OF_CRED
              - CDN_DIAG_S_OUT_OF_CRED
              - CDN_DIAG_E_OUT_OF_CRED
              - CDN_DIAG_W_OUT_OF_CRED
              - CDN_DIAG_C_OUT_OF_CRED
              - CDN_DIAG_N_EGRESS
              - CDN_DIAG_S_EGRESS
              - CDN_DIAG_E_EGRESS
              - CDN_DIAG_W_EGRESS
              - CDN_DIAG_C_EGRESS
              - CDN_DIAG_N_INGRESS
              - CDN_DIAG_S_INGRESS
              - CDN_DIAG_E_INGRESS
              - CDN_DIAG_W_INGRESS
              - CDN_DIAG_C_INGRESS
              - CDN_DIAG_CORE_SENT
              - DDN_DIAG_N_OUT_OF_CRED
              - DDN_DIAG_S_OUT_OF_CRED
              - DDN_DIAG_E_OUT_OF_CRED
              - DDN_DIAG_W_OUT_OF_CRED
              - DDN_DIAG_C_OUT_OF_CRED
              - DDN_DIAG_N_EGRESS
              - DDN_DIAG_S_EGRESS
              - DDN_DIAG_E_EGRESS
              - DDN_DIAG_W_EGRESS
              - DDN_DIAG_C_EGRESS
              - DDN_DIAG_N_INGRESS
              - DDN_DIAG_S_INGRESS
              - DDN_DIAG_E_INGRESS
              - DDN_DIAG_W_INGRESS
              - DDN_DIAG_C_INGRESS
              - DDN_DIAG_CORE_SENT
              - NDN_DIAG_N_OUT_OF_CRED
              - NDN_DIAG_S_OUT_OF_CRED
              - NDN_DIAG_E_OUT_OF_CRED
              - NDN_DIAG_W_OUT_OF_CRED
              - NDN_DIAG_C_OUT_OF_CRED
              - NDN_DIAG_N_EGRESS
              - NDN_DIAG_S_EGRESS
              - NDN_DIAG_E_EGRESS
              - NDN_DIAG_W_EGRESS
              - NDN_DIAG_C_EGRESS
              - NDN_DIAG_N_INGRESS
              - NDN_DIAG_S_INGRESS
              - NDN_DIAG_E_INGRESS
              - NDN_DIAG_W_INGRESS
              - NDN_DIAG_C_INGRESS
              - NDN_DIAG_CORE_SENT
              - DISABLED
    nodeExecutionFilters_MonitoringResourceExecutionFilter:
      description:
      - 'Filter nodes which should run this data producer. If none are specified: execute
        on each node.'
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
        filterOperation:
          description:
          - The filter operation to be performed
          type: str
          required: false
          default: INCLUDE
          choices:
          - NONE
          - INCLUDE
          - EXCLUDE
        resources:
          description:
          - Resources
          type: list
          required: false
          default: []
        op:
          description:
          - Operator
          type: str
          required: false
          default: OR
          choices:
          - OR
          - AND
    nodeExecutionFilters_MonitoringOverlayListExecutionFilter:
      description:
      - 'Filter nodes which should run this data producer. If none are specified: execute
        on each node.'
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
        filterOperation:
          description:
          - The filter operation to be performed
          type: str
          required: false
          default: INCLUDE
          choices:
          - NONE
          - INCLUDE
          - EXCLUDE
        overlays:
          description:
          - List of overlays belonging to this group
          type: list
          required: false
          default: []
    nodeExecutionFilters_MonitoringTypeExecutionFilter:
      description:
      - 'Filter nodes which should run this data producer. If none are specified: execute
        on each node.'
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
        filterOperation:
          description:
          - The filter operation to be performed
          type: str
          required: false
          default: INCLUDE
          choices:
          - NONE
          - INCLUDE
          - EXCLUDE
        headNode:
          description:
          - Head node
          type: bool
          required: false
          default: false
        physicalNode:
          description:
          - Physical node
          type: bool
          required: false
          default: false
        cloudNode:
          description:
          - Cloud node
          type: bool
          required: false
          default: false
        liteNode:
          description:
          - Lite node
          type: bool
          required: false
          default: false
        dpuNode:
          description:
          - DPU node
          type: bool
          required: false
          default: false
    nodeExecutionFilters_MonitoringNodeListExecutionFilter:
      description:
      - 'Filter nodes which should run this data producer. If none are specified: execute
        on each node.'
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
        filterOperation:
          description:
          - The filter operation to be performed
          type: str
          required: false
          default: INCLUDE
          choices:
          - NONE
          - INCLUDE
          - EXCLUDE
        nodes:
          description:
          - List of nodes belonging to this group
          type: list
          required: false
          default: []
    nodeExecutionFilters_MonitoringLuaExecutionFilter:
      description:
      - 'Filter nodes which should run this data producer. If none are specified: execute
        on each node.'
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
        filterOperation:
          description:
          - The filter operation to be performed
          type: str
          required: false
          default: INCLUDE
          choices:
          - NONE
          - INCLUDE
          - EXCLUDE
        code:
          description:
          - Lua code
          type: str
          required: false
        notes:
          description:
          - Notes
          type: str
          required: false
    nodeExecutionFilters_MonitoringCategoryListExecutionFilter:
      description:
      - 'Filter nodes which should run this data producer. If none are specified: execute
        on each node.'
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
        filterOperation:
          description:
          - The filter operation to be performed
          type: str
          required: false
          default: INCLUDE
          choices:
          - NONE
          - INCLUDE
          - EXCLUDE
        categories:
          description:
          - List of categories belonging to this group
          type: list
          required: false
          default: []
    executionMultiplexers_MonitoringResourceExecutionMultiplexer:
      description:
      - 'Execute the producer once for each entity which matches one of the criteria.
        If none are specified: only execute it for the node itself.'
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
        filterOperation:
          description:
          - The filter operation to be performed
          type: str
          required: false
          default: INCLUDE
          choices:
          - NONE
          - INCLUDE
          - EXCLUDE
        resources:
          description:
          - Resources
          type: list
          required: false
          default: []
        op:
          description:
          - Operator
          type: str
          required: false
          default: OR
          choices:
          - OR
          - AND
    executionMultiplexers_MonitoringDynamicExecutionMultiplexer:
      description:
      - 'Execute the producer once for each entity which matches one of the criteria.
        If none are specified: only execute it for the node itself.'
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
        filterOperation:
          description:
          - The filter operation to be performed
          type: str
          required: false
          default: INCLUDE
          choices:
          - NONE
          - INCLUDE
          - EXCLUDE
        local:
          description:
          - Run on the local node
          type: bool
          required: false
          default: false
        host:
          description:
          - Run on the host node of a DPU
          type: bool
          required: false
          default: false
        offload:
          description:
          - Run on the nodes offloaded onto this node
          type: bool
          required: false
          default: false
    executionMultiplexers_MonitoringTypeExecutionMultiplexer:
      description:
      - 'Execute the producer once for each entity which matches one of the criteria.
        If none are specified: only execute it for the node itself.'
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
        filterOperation:
          description:
          - The filter operation to be performed
          type: str
          required: false
          default: INCLUDE
          choices:
          - NONE
          - INCLUDE
          - EXCLUDE
        types:
          description:
          - Types
          type: list
          required: false
          default: []
    executionMultiplexers_MonitoringNodeListExecutionMultiplexer:
      description:
      - 'Execute the producer once for each entity which matches one of the criteria.
        If none are specified: only execute it for the node itself.'
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
        filterOperation:
          description:
          - The filter operation to be performed
          type: str
          required: false
          default: INCLUDE
          choices:
          - NONE
          - INCLUDE
          - EXCLUDE
        nodes:
          description:
          - List of nodes belonging to this group
          type: list
          required: false
          default: []
    executionMultiplexers_MonitoringLuaExecutionMultiplexer:
      description:
      - 'Execute the producer once for each entity which matches one of the criteria.
        If none are specified: only execute it for the node itself.'
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
        filterOperation:
          description:
          - The filter operation to be performed
          type: str
          required: false
          default: INCLUDE
          choices:
          - NONE
          - INCLUDE
          - EXCLUDE
        code:
          description:
          - Lua code
          type: str
          required: false
        notes:
          description:
          - Notes
          type: str
          required: false
    executionMultiplexers_MonitoringCategoryListExecutionMultiplexer:
      description:
      - 'Execute the producer once for each entity which matches one of the criteria.
        If none are specified: only execute it for the node itself.'
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
        filterOperation:
          description:
          - The filter operation to be performed
          type: str
          required: false
          default: INCLUDE
          choices:
          - NONE
          - INCLUDE
          - EXCLUDE
        categories:
          description:
          - List of categories belonging to this group
          type: list
          required: false
          default: []
    executionMultiplexers_MonitoringOverlayListExecutionMultiplexer:
      description:
      - 'Execute the producer once for each entity which matches one of the criteria.
        If none are specified: only execute it for the node itself.'
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
        filterOperation:
          description:
          - The filter operation to be performed
          type: str
          required: false
          default: INCLUDE
          choices:
          - NONE
          - INCLUDE
          - EXCLUDE
        overlays:
          description:
          - List of overlays belonging to this group
          type: list
          required: false
          default: []
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
monitoring_data_producer_dpu:
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
      description: Name
      returned: success
    description:
      type: str
      description: Description
      returned: success
    notes:
      type: str
      description: Administrator notes
      returned: success
    when:
      type: str
      description: When the producer should run
      returned: success
    preJob:
      type: bool
      description: Run as pre job in prolog
      returned: success
    postJob:
      type: bool
      description: Run as post job in epilog
      returned: success
    maxAge:
      type: float
      description: Maximal age of historic data, 0 for infinite
      returned: success
    maxSamples:
      type: int
      description: Maximal samples of historic data, 0 for infinite
      returned: success
    interval:
      type: float
      description: Sampling interval
      returned: success
    offset:
      type: float
      description: Time offset for sampling interval
      returned: success
    startupDelay:
      type: float
      description: Delay the first sampling the specified time after cmd starts
      returned: success
    intervals:
      type: float
      description: Out of band sampling interval
      returned: success
    gap:
      type: int
      description: Number of missed samples before we add a NaN
      returned: success
    fuzzyOffset:
      type: float
      description: Automatic fuzzy offset factor [0-1]. Multiplied by interval
      returned: success
    introduceNaN:
      type: bool
      description: Introduce NaN if device goes up/down/up
      returned: success
    maxMeasurables:
      type: int
      description: Maximal number of measurables the producer can introduce
      returned: success
    automaticReinitialize:
      type: bool
      description: Automatic run --initialize when a new metric has been detected
      returned: success
    disabled:
      type: bool
      description: Disabled
      returned: success
    disableTriggers:
      type: bool
      description: Disable triggers from being evaluated
      returned: success
    disableOnHighLoad:
      type: bool
      description: Disable when nodes are very busy
      returned: success
    nodeExecutionFilters:
      type: list
      description: 'Filter nodes which should run this data producer. If none are
        specified: execute on each node.'
      returned: success
    executionMultiplexers:
      type: list
      description: 'Execute the producer once for each entity which matches one of
        the criteria. If none are specified: only execute it for the node itself.'
      returned: success
    consolidator:
      type: complex
      description: Consolidator configuration
      returned: success
    suppressedByGoingDown:
      type: bool
      description: Suppress running action if device is going down
      returned: success
    access:
      type: str
      description: User access control
      returned: success
    associatedUser:
      type: str
      description: User associated with this measurable
      returned: success
    dpuSettings:
      type: complex
      description: Submode containing DPU settings
      returned: success

"""
############################
# Imports
############################

from copy import deepcopy
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import MonitoringDataProducerDPU
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
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.argspecs.monitoring_data_producer_dpu import MonitoringDataProducerDPU_ArgSpec

############################
# main
############################

def main():

    module = BaseModule(
        argument_spec=MonitoringDataProducerDPU_ArgSpec.argument_spec,
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

    entity = entity_manager.lookup_entity(params, MonitoringDataProducerDPU)

    changed = False

    diff = None

    desired_state = params["state"]

    if not entity:
        if desired_state == "present":
            entity, res = entity_manager.create_resource(MonitoringDataProducerDPU, params, commit=not module.check_mode)
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