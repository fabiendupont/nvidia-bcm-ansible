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

from pythoncm.entity.entity import Entity


class SoftwareImage(Entity):
    def remove(self, wait_for_task=False, force=False, data_on_disk=False, derived_revisions=False):
        """
        Remove the software image
        """
        return super().remove(
            wait_for_task,
            force,
            data_on_disk,
            derived_revisions,
        )

    def clone(self, cluster=None, add_to_cluster=True, clear_cloned=True, copy_directory_structure=True):
        """
        Special clone function
        """
        cloned_image = super().clone(cluster, add_to_cluster, clear_cloned)
        if copy_directory_structure:
            cloned_image.originalImage = self.uuid
        return cloned_image

    def wait_for_provisioning(self, timeout=None, include_pending=True):
        """
        Wait for all active provisioning tasks for this node to be completed
        """
        return self._cluster.provisioning.wait_path(self.path, timeout=timeout, include_pending=include_pending)

    def get_fsparts(self, resolve: bool = True):
        from pythoncm.entity import ArchOSInfo

        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmprov',
            call='getFSPartsForSoftwareImage',
            args=[self.uuid],
        )
        if code:
            raise OSError(out)
        if resolve:

            def get(name):
                entity = out.get(name, None)
                if entity is not None:
                    entity = self._cluster.get_by_uuid(entity['uuid'])
                return entity

            return (
                get('fspart'),
                get('boot'),
                get('shared'),
                get('installer'),
                ArchOSInfo(self._cluster, out.get('archOS', None)),
            )
        return (
            out.get('fspart', None),
            out.get('boot', None),
            out.get('shared', None),
            out.get('installer', None),
            out.get('archOS', None),
        )

    def get_kernel_versions(self) -> list[str]:
        """Retrieve all available kernel versions in this image."""
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(service='cmpart', call='getSoftwareImageKernelVersions', args=[self.to_dict()])
        if code:
            raise OSError(out)
        return out

    @property
    def nodes(self):
        """
        Get all nodes using this image
        """

        # CM-18430: load order issue
        from pythoncm.entity.computenode import ComputeNode

        return [node for node in self._cluster.get_by_type(ComputeNode) if node.software_image == self]

    def lock(self):
        """
        Lock the file system part, so it cannot be used anymore
        """
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmprov',
            call='lockFSParts',
            args=[[self.fspart.uuid, self.bootfspart.uuid]],
        )
        if code:
            raise OSError(out)
        return out

    def unlock(self):
        """
        Lock the file system part, so it cannot be used anymore
        """
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmprov',
            call='unlockFSParts',
            args=[[self.fspart.uuid, self.bootfspart.uuid]],
        )
        if code:
            raise OSError(out)
        return out

    def is_locked(self):
        """
        Determine of if the file system part is locked
        """
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmprov',
            call='islockedFSParts',
            args=[self.fspart.uuid],
        )
        if code:
            raise OSError(out)
        return out

    def get_capi_versions(self, debug: bool = False):
        """
        Get the CAPI versions installed on the image
        """
        from pythoncm.entity import ExternalOperationResult

        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmkube',
            call='getCapiImageVersions',
            args=[[self.uuid], debug],
        )
        if code:
            raise OSError(out)
        return ExternalOperationResult(self._cluster, out)

    def add_capi_versions(self, versions: list[str], repo_refresh: bool = False, debug: bool = False):
        """
        Add CAPI versions to the image
        """
        from pythoncm.entity import ExternalOperationResult

        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmkube',
            call='addCapiImageVersions',
            args=[[self.uuid], versions, repo_refresh, debug],
        )
        if code:
            raise OSError(out)
        return ExternalOperationResult(self._cluster, out)

    def remove_capi_versions(self, versions: list[str], debug: bool = False):
        """
        Remove CAPI versions installed in the image
        """
        from pythoncm.entity import ExternalOperationResult

        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmkube',
            call='removeCapiImageVersions',
            args=[[self.uuid], versions, debug],
        )
        if code:
            raise OSError(out)
        return ExternalOperationResult(self._cluster, out)

    def clear_capi_versions(self, debug: bool = False):
        """
        Clear all installed CAPI versions from the image
        """
        from pythoncm.entity import ExternalOperationResult

        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmkube',
            call='clearCapiImageVersions',
            args=[[self.uuid], debug],
        )
        if code:
            raise OSError(out)
        return ExternalOperationResult(self._cluster, out)
