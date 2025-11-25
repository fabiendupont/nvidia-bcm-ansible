# Ansible Collection: brightcomputing.bcm110

Ansible collection for managing Bright Computing Cluster Manager resources.
Each module defined here corresponds to a top level Entity managed by the cmdaemon API.

## Requirements
* ansible-base version 2.10.0+

## External requirements
* python3.9+
* Bright Cluster Manager v11.0+
* pythoncm; python binding for cmdaemon
* [python-box](https://github.com/cdgriffith/Box)
* [deepdiff](https://github.com/seperman/deepdiff)

## Installing this collection
Currently you can install this collection using Ansible Galaxy CLI:
	ansible-galaxy collection install brightcomputing.bcm110


## Using this collection
As mentioned before, using this collection requires the Ansible node to have a usable version of pythoncm.
This is simply the case because this collection uses the pythoncm API to ensure the state of a specific resource in a module invocation.
One way to do this is to configure Ansible to use cm-python3.  An ansible configuration that uses the cm-python3 interpeter looks like this:
```yaml
[defaults]
interpreter_python = /cm/local/apps/python3/bin/python
```
Doing so ensures that the module code will have access to pythoncm, since pythoncm is installed, as part of Python (installed at
/cm/local/app/python3/bin/python3 by Bright), out-of-the-box, for any version 9.1+ cluster.


## Included content

### Modules
Name | Description
--- | ---
azure_location | ['Manages azure_locations']
azure_location_info | Query cmdaemon for entity of type AzureLocation
azure_provider | ['Manages azure_providers']
azure_provider_info | Query cmdaemon for entity of type AzureProvider
azure_vm_size | ['Manages azure_vm_sizes']
azure_vm_size_info | Query cmdaemon for entity of type AzureVMSize
bee_gfs_cluster | ['Manages bee_gfs_clusters']
bee_gfs_cluster_info | Query cmdaemon for entity of type BeeGFSCluster
category | ['Manages categories']
category_info | Query cmdaemon for entity of type Category
certificate | ['Certificate']
certificate_info | Query cmdaemon for entity of type Certificate
certificate_request | ['Certificate request']
certificate_request_info | Query cmdaemon for entity of type CertificateRequest
charge_back_request | ['Manages charge_back_requests']
charge_back_request_info | Query cmdaemon for entity of type ChargeBackRequest
chassis | ['Chassis']
chassis_info | Query cmdaemon for entity of type Chassis
cloud_node | ['Manages cloud_nodes']
cloud_node_info | Query cmdaemon for entity of type CloudNode
configuration_overlay | ['Configuration overlay']
configuration_overlay_info | Query cmdaemon for entity of type ConfigurationOverlay
cooling_distribution_unit | ['Manages cooling_distribution_units']
cooling_distribution_unit_info | Query cmdaemon for entity of type CoolingDistributionUnit
dpu_node | ['Manages dpu_nodes']
dpu_node_info | Query cmdaemon for entity of type DPUNode
drain_action | ['Manages drain_actions']
drain_action_info | Query cmdaemon for entity of type DrainAction
ec2_provider | ['Manages ec2_providers']
ec2_provider_info | Query cmdaemon for entity of type EC2Provider
ec2_region | ['Manages ec2_regions']
ec2_region_info | Query cmdaemon for entity of type EC2Region
ec2_type | ['Manages ec2_types']
ec2_type_info | Query cmdaemon for entity of type EC2Type
edge_site | ['Manages edge_sites']
edge_site_info | Query cmdaemon for entity of type EdgeSite
etcd_cluster | ['Manages etcd_clusters']
etcd_cluster_info | Query cmdaemon for entity of type EtcdCluster
forge_instance_type | ['Manages forge_instance_types']
forge_instance_type_info | Query cmdaemon for entity of type ForgeInstanceType
forge_provider | ['Manages forge_providers']
forge_provider_info | Query cmdaemon for entity of type ForgeProvider
fs_part | ['Manages fs_parts']
fs_part_info | Query cmdaemon for entity of type FSPart
gcp_machine_type | ['Manages gcp_machine_types']
gcp_machine_type_info | Query cmdaemon for entity of type GCPMachineType
gcp_provider | ['Manages gcp_providers']
gcp_provider_info | Query cmdaemon for entity of type GCPProvider
gcp_zone | ['Manages gcp_zones']
gcp_zone_info | Query cmdaemon for entity of type GCPZone
generic_device | ['Manages generic_devices']
generic_device_info | Query cmdaemon for entity of type GenericDevice
group | ['Group']
group_info | Query cmdaemon for entity of type Group
head_node | ['Head node']
head_node_info | Query cmdaemon for entity of type HeadNode
kube_cluster | ['Manages kube_clusters']
kube_cluster_info | Query cmdaemon for entity of type KubeCluster
labeled_entity | ['Manages labeled_entities']
labeled_entity_info | Query cmdaemon for entity of type LabeledEntity
lite_node | ['Manages lite_nodes']
lite_node_info | Query cmdaemon for entity of type LiteNode
lsf_job_queue | ['LSF job queues']
lsf_job_queue_info | Query cmdaemon for entity of type LSFJobQueue
lsf_wlm_cluster | ['Manages lsf_wlm_clusters']
lsf_wlm_cluster_info | Query cmdaemon for entity of type LSFWlmCluster
monitoring_consolidator | ['Manages monitoring_consolidators']
monitoring_consolidator_info | Query cmdaemon for entity of type MonitoringConsolidator
monitoring_data_producer_aggregate_cdu | ['Manages monitoring_data_producer_aggregate_cdus']
monitoring_data_producer_aggregate_cdu_info | Query cmdaemon for entity of type MonitoringDataProducerAggregateCDU
monitoring_data_producer_aggregate_pdu | ['Manages monitoring_data_producer_aggregate_pdus']
monitoring_data_producer_aggregate_pdu_info | Query cmdaemon for entity of type MonitoringDataProducerAggregatePDU
monitoring_data_producer_aggregate_power_circuit | ['Manages monitoring_data_producer_aggregate_power_circuits']
monitoring_data_producer_aggregate_power_circuit_info | Query cmdaemon for entity of type MonitoringDataProducerAggregatePowerCircuit
monitoring_data_producer_aggregate_power_shelf | ['Manages monitoring_data_producer_aggregate_power_shelfs']
monitoring_data_producer_aggregate_power_shelf_info | Query cmdaemon for entity of type MonitoringDataProducerAggregatePowerShelf
monitoring_data_producer_aggregate_switch | ['Manages monitoring_data_producer_aggregate_switchs']
monitoring_data_producer_aggregate_switch_info | Query cmdaemon for entity of type MonitoringDataProducerAggregateSwitch
monitoring_data_producer_cm_daemon_state | ['Manages monitoring_data_producer_cm_daemon_states']
monitoring_data_producer_cm_daemon_state_info | Query cmdaemon for entity of type MonitoringDataProducerCMDaemonState
monitoring_data_producer_cpu | ['Manages monitoring_data_producer_cpus']
monitoring_data_producer_cpu_info | Query cmdaemon for entity of type MonitoringDataProducerCPU
monitoring_data_producer_dpu | ['Manages monitoring_data_producer_dpus']
monitoring_data_producer_dpu_info | Query cmdaemon for entity of type MonitoringDataProducerDPU
monitoring_data_producer_ec2_spot_prices | ['Manages monitoring_data_producer_ec2_spot_pricess']
monitoring_data_producer_ec2_spot_prices_info | Query cmdaemon for entity of type MonitoringDataProducerEC2SpotPrices
monitoring_data_producer_gpu | ['Manages monitoring_data_producer_gpus']
monitoring_data_producer_gpu_info | Query cmdaemon for entity of type MonitoringDataProducerGPU
monitoring_data_producer_network_utilization | ['Manages monitoring_data_producer_network_utilizations']
monitoring_data_producer_network_utilization_info | Query cmdaemon for entity of type MonitoringDataProducerNetworkUtilization
monitoring_data_producer_nmx_controller | ['Manages monitoring_data_producer_nmx_controllers']
monitoring_data_producer_nmx_controller_info | Query cmdaemon for entity of type MonitoringDataProducerNMXController
monitoring_data_producer_proc_vm_stat | ['Manages monitoring_data_producer_proc_vm_stats']
monitoring_data_producer_proc_vm_stat_info | Query cmdaemon for entity of type MonitoringDataProducerProcVMStat
monitoring_data_producer_prs | ['Manages monitoring_data_producer_prss']
monitoring_data_producer_prs_info | Query cmdaemon for entity of type MonitoringDataProducerPRS
monitoring_data_producer_red_fish_subscription | ['Manages monitoring_data_producer_red_fish_subscriptions']
monitoring_data_producer_red_fish_subscription_info | Query cmdaemon for entity of type MonitoringDataProducerRedFishSubscription
monitoring_data_producer_script | ['Manages monitoring_data_producer_scripts']
monitoring_data_producer_script_info | Query cmdaemon for entity of type MonitoringDataProducerScript
monitoring_data_producer_single_line_health_check_script | ['Manages monitoring_data_producer_single_line_health_check_scripts']
monitoring_data_producer_single_line_health_check_script_info | Query cmdaemon for entity of type MonitoringDataProducerSingleLineHealthCheckScript
monitoring_data_producer_single_line_metric_script | ['Manages monitoring_data_producer_single_line_metric_scripts']
monitoring_data_producer_single_line_metric_script_info | Query cmdaemon for entity of type MonitoringDataProducerSingleLineMetricScript
monitoring_data_producer_wlm_slot | ['Manages monitoring_data_producer_wlm_slots']
monitoring_data_producer_wlm_slot_info | Query cmdaemon for entity of type MonitoringDataProducerWlmSlot
monitoring_drain_action | ['Manages monitoring_drain_actions']
monitoring_drain_action_info | Query cmdaemon for entity of type MonitoringDrainAction
monitoring_email_action | ['Manages monitoring_email_actions']
monitoring_email_action_info | Query cmdaemon for entity of type MonitoringEmailAction
monitoring_event_action | ['Manages monitoring_event_actions']
monitoring_event_action_info | Query cmdaemon for entity of type MonitoringEventAction
monitoring_image_update_action | ['Manages monitoring_image_update_actions']
monitoring_image_update_action_info | Query cmdaemon for entity of type MonitoringImageUpdateAction
monitoring_measurable_enum | ['Manages monitoring_measurable_enums']
monitoring_measurable_enum_info | Query cmdaemon for entity of type MonitoringMeasurableEnum
monitoring_measurable_health_check | ['Manages monitoring_measurable_health_checks']
monitoring_measurable_health_check_info | Query cmdaemon for entity of type MonitoringMeasurableHealthCheck
monitoring_measurable_metric | ['Manages monitoring_measurable_metrics']
monitoring_measurable_metric_info | Query cmdaemon for entity of type MonitoringMeasurableMetric
monitoring_nvsm_health_dump_action | ['Manages monitoring_nvsm_health_dump_actions']
monitoring_nvsm_health_dump_action_info | Query cmdaemon for entity of type MonitoringNVSMHealthDumpAction
monitoring_script_action | ['Manages monitoring_script_actions']
monitoring_script_action_info | Query cmdaemon for entity of type MonitoringScriptAction
monitoring_trigger | ['Manages monitoring_triggers']
monitoring_trigger_info | Query cmdaemon for entity of type MonitoringTrigger
monitoring_undrain_action | ['Manages monitoring_undrain_actions']
monitoring_undrain_action_info | Query cmdaemon for entity of type MonitoringUndrainAction
network | ['Network']
network_info | Query cmdaemon for entity of type Network
node_group | ['Manages node_groups']
node_group_info | Query cmdaemon for entity of type NodeGroup
oci_instance_pool | ['Manages oci_instance_pools']
oci_instance_pool_info | Query cmdaemon for entity of type OCIInstancePool
oci_provider | ['Manages oci_providers']
oci_provider_info | Query cmdaemon for entity of type OCIProvider
oci_region | ['Manages oci_regions']
oci_region_info | Query cmdaemon for entity of type OCIRegion
oci_shape | ['Manages oci_shapes']
oci_shape_info | Query cmdaemon for entity of type OCIShape
ocigpu_memory_cluster | ['Manages ocigpu_memory_clusters']
ocigpu_memory_cluster_info | Query cmdaemon for entity of type OCIGPUMemoryCluster
os_cloud_flavor | ['Manages os_cloud_flavors']
os_cloud_flavor_info | Query cmdaemon for entity of type OSCloudFlavor
os_cloud_provider | ['Manages os_cloud_providers']
os_cloud_provider_info | Query cmdaemon for entity of type OSCloudProvider
os_cloud_region | ['Manages os_cloud_regions']
os_cloud_region_info | Query cmdaemon for entity of type OSCloudRegion
partition | ['Partition']
partition_info | Query cmdaemon for entity of type Partition
pbs_pro_job_queue | ['PBSPro job queue']
pbs_pro_job_queue_info | Query cmdaemon for entity of type PbsProJobQueue
pbs_pro_wlm_cluster | ['Manages pbs_pro_wlm_clusters']
pbs_pro_wlm_cluster_info | Query cmdaemon for entity of type PbsProWlmCluster
physical_node | ['Node']
physical_node_info | Query cmdaemon for entity of type PhysicalNode
power_circuit | ['Power circuit']
power_circuit_info | Query cmdaemon for entity of type PowerCircuit
power_distribution_unit | ['Manages power_distribution_units']
power_distribution_unit_info | Query cmdaemon for entity of type PowerDistributionUnit
power_shelf | ['Manages power_shelfs']
power_shelf_info | Query cmdaemon for entity of type PowerShelf
profile | ['Manages profiles']
profile_info | Query cmdaemon for entity of type Profile
prometheus_query | ['Manages prometheus_queries']
prometheus_query_info | Query cmdaemon for entity of type PrometheusQuery
rack | ['Rack']
rack_info | Query cmdaemon for entity of type Rack
rack_sensor | ['Manages rack_sensors']
rack_sensor_info | Query cmdaemon for entity of type RackSensor
report_query | ['Manages report_queries']
report_query_info | Query cmdaemon for entity of type ReportQuery
slurm_job_queue | ['Slurm job queues']
slurm_job_queue_info | Query cmdaemon for entity of type SlurmJobQueue
slurm_wlm_cluster | ['Manages slurm_wlm_clusters']
slurm_wlm_cluster_info | Query cmdaemon for entity of type SlurmWlmCluster
software_image | ['Software image']
software_image_file_selection | ['Software image file selection']
software_image_file_selection_info | Query cmdaemon for entity of type SoftwareImageFileSelection
software_image_info | Query cmdaemon for entity of type SoftwareImage
standalone_monitored_entity | ['Manages standalone_monitored_entities']
standalone_monitored_entity_info | Query cmdaemon for entity of type StandaloneMonitoredEntity
switch | ['Manages switchs']
switch_info | Query cmdaemon for entity of type Switch
user | ['User']
user_info | Query cmdaemon for entity of type User

## Licensing
Bright Ansible collection is distributed under a GPL 2.0 license.
The license text can be found at [link](https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt)