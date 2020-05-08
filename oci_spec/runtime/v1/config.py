# Copyright (C) 2019-2020 Guillermo Adrián Molina.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http:#mozilla.org/MPL/2.0/.

from oci_spec.struct import Struct
from oci_spec.digest import Digest

from datetime import datetime

SpecOCIVersion = "1.0.0"

class LinuxIntelRdt(Struct):
    # LinuxIntelRdt has container runtime resource constraints for Intel RDT
    # CAT and MBA features which introduced in Linux 4.10 and 4.12 kernel
          
    def __init__(
        self
    ):

        super().__init__()

        # The identity for RDT Class of Service
        self.newAttr(name="ClosID", attType=str, jsonName="closID", omitempty=True)
        # The schema for L3 cache id and capacity bitmask (CBM)
        # Format: "L3:<cache_id0>=<cbm0>;<cache_id1>=<cbm1>;...")
        self.newAttr(name="L3CacheSchema", attType=str, jsonName="l3CacheSchema", omitempty=True)

        # The schema of memory bandwidth per L3 cache id
        # Format: "MB:<cache_id0>=bandwidth0;<cache_id1>=bandwidth1;...")
        # The unit of memory bandwidth is specified in "percentages" by
        # default, and in "MBps" if MBA Software Controller is enabled.
        self.newAttr(name="MemBwSchema", attType=str, jsonName="memBwSchema", omitempty=True)


class LinuxSyscall(Struct):
    # LinuxSyscall is used to match a syscall in Seccomp
          
    def __init__(
        self
    ):

        super().__init__()

        self.newAttr(name="Names", attType=[str], jsonName="names", required=True)
        self.newAttr(name="Action", attType=str, jsonName="action", required=True)
        self.newAttr(name="Args", attType=[LinuxSeccompArg], jsonName="args", omitempty=True)


class LinuxSeccompArg(Struct):
    # LinuxSeccompArg used for matching specific syscall arguments in Seccomp
          
    def __init__(
        self
    ):

        super().__init__()

        self.newAttr(name="Index", attType=int, jsonName="index", required=True)
        self.newAttr(name="Value", attType=int, jsonName="value", required=True)
        self.newAttr(name="ValueTwo", attType=int, jsonName="valueTwo", omitempty=True)
        self.newAttr(name="Op", attType=str, jsonName="op", required=True)


class LinuxSeccomp(Struct):
    # LinuxSeccomp represents syscall restrictions
          
    def __init__(
        self
    ):

        super().__init__()

        self.newAttr(name="DefaultAction", attType=str, jsonName="defaultAction", required=True)
        self.newAttr(name="Architectures", attType=[str], jsonName="architectures", omitempty=True)
        self.newAttr(name="Flags ", attType=[str], jsonName="flags", omitempty=True)
        self.newAttr(name="Syscalls ", attType=[LinuxSyscall], jsonName="syscalls", omitempty=True)


class VMImage(Struct):
    # VMImage contains information about the virtual machine root image.
          
    def __init__(
        self
    ):

        super().__init__()

        # Path is the host path to the root image that the VM kernel would boot into.
        self.newAttr(name="Path", attType=str, jsonName="path", required=True)
        # Format is the root image format type (e.g. "qcow2", "raw", "vhd", etc).
        self.newAttr(name="Format", attType=str, jsonName="format", required=True)


class VMKernel(Struct):
    # VMKernel contains information about the kernel to use for a virtual machine.
          
    def __init__(
        self
    ):

        super().__init__()

        # Path is the host path to the kernel used to boot the virtual machine.
        self.newAttr(name="Path", attType=str, jsonName="path", required=True)
        # Parameters specifies parameters to pass to the kernel.
        self.newAttr(name="Parameters", attType=[str], jsonName="parameters", omitempty=True)
        # InitRD is the host path to an initial ramdisk to be used by the kernel.
        self.newAttr(name="InitRD", attType=str, jsonName="initrd", omitempty=True)


class VMHypervisor(Struct):
    # VMHypervisor contains information about the hypervisor to use for a virtual machine.
          
    def __init__(
        self
    ):

        super().__init__()

        # Path is the host path to the hypervisor used to manage the virtual machine.
        self.newAttr(name="Path", attType=str, jsonName="path", required=True)
        # Parameters specifies parameters to pass to the hypervisor.
        self.newAttr(name="Parameters", attType=[str], jsonName="parameters", omitempty=True)


class VM(Struct):
    # VM contains information for virtual-machine-based containers.
          
    def __init__(
        self
    ):

        super().__init__()

        # Hypervisor specifies hypervisor-related configuration for virtual-machine-based containers.
        self.newAttr(name="Hypervisor", attType=VMHypervisor, jsonName="hypervisor", omitempty=True)
        # Kernel specifies kernel-related configuration for virtual-machine-based containers.
        self.newAttr(name="Kernel", attType=VMKernel, jsonName="kernel", required=True)
        # Image specifies guest image related configuration for virtual-machine-based containers.
        self.newAttr(name="Image", attType=VMImage, jsonName="image", omitempty=True)


class WindowsHyperV(Struct):
    # WindowsHyperV contains information for configuring a container to run with Hyper-V isolation.
          
    def __init__(
        self
    ):

        super().__init__()

        # UtilityVMPath is an optional path to the image used for the Utility VM.
        self.newAttr(name="UtilityVMPath", attType=str, jsonName="utilityVMPath", omitempty=True)


class WindowsNetwork(Struct):
    # WindowsNetwork contains network settings for Windows containers.
          
    def __init__(
        self
    ):

        super().__init__()

        # List of HNS endpoints that the container should connect to.
        self.newAttr(name="EndpointList", attType=[str], jsonName="endpointList", omitempty=True)
        # Specifies if unqualified DNS name resolution is allowed.
        self.newAttr(name="AllowUnqualifiedDNSQuery", attType=bool, jsonName="allowUnqualifiedDNSQuery", omitempty=True)
        # Comma separated list of DNS suffixes to use for name resolution.
        self.newAttr(name="DNSSearchList", attType=[str], jsonName="DNSSearchList", omitempty=True)
        # Name (ID) of the container that we will share with the network stack.
        self.newAttr(name="NetworkSharedContainerName", attType=str, jsonName="networkSharedContainerName", omitempty=True)
        # name (ID) of the network namespace that will be used for the container.
        self.newAttr(name="NetworkNamespace", attType=str, jsonName="networkNamespace", omitempty=True)


class WindowsStorageResources(Struct):
    # WindowsStorageResources contains storage resource management settings.
          
    def __init__(
        self
    ):

        super().__init__()

        # Specifies maximum Iops for the system drive.
        self.newAttr(name="Iops", attType=int, jsonName="iops", omitempty=True)
        # Specifies maximum bytes per second for the system drive.
        self.newAttr(name="Bps", attType=int, jsonName="bps", omitempty=True)
        # Sandbox size specifies the minimum size of the system drive in bytes.
        self.newAttr(name="SandboxSize", attType=int, jsonName="sandboxSize", omitempty=True)


class WindowsCPUResources(Struct):
    # WindowsCPUResources contains CPU resource management settings.
          
    def __init__(
        self
    ):

        super().__init__()

        # Number of CPUs available to the container.
        self.newAttr(name="Count", attType=int, jsonName="count", omitempty=True)
        # CPU shares (relative weight to other containers with cpu shares).
        self.newAttr(name="Shares", attType=int, jsonName="shares", omitempty=True)
        # Specifies the portion of processor cycles that this container can use as a percentage times 100.
        self.newAttr(name="Maximum", attType=int, jsonName="maximum", omitempty=True)


class WindowsMemoryResources(Struct):
    # WindowsMemoryResources contains memory resource management settings.
     
    def __init__(
        self
    ):

        super().__init__()

        # Memory limit in bytes.
        self.newAttr(name="Limit", attType=int, jsonName="limit", omitempty=True)


class WindowsResources(Struct):
    # WindowsResources has container runtime resource constraints for containers running on Windows.
     
    def __init__(
        self
    ):

        super().__init__()

             # Memory restriction configuration.
        self.newAttr(name="Memory", attType=WindowsMemoryResources, jsonName="memory", omitempty=True)
        # CPU resource restriction configuration.
        self.newAttr(name="CPU", attType=WindowsCPUResources, jsonName="cpu", omitempty=True)
        # Storage restriction configuration.
        self.newAttr(name="Storage", attType=WindowsStorageResources, jsonName="storage", omitempty=True)


class WindowsDevice(Struct):
    # WindowsDevice represents information about a host device to be mapped into the container.
          
    def __init__(
        self
    ):

        super().__init__()

        # Device identifier: interface class GUID, etc.
        self.newAttr(name="ID", attType=str, jsonName="id", required=True)
        # Device identifier type: "class", etc.
        self.newAttr(name="IDType", attType=str, jsonName="idType", required=True)


class Windows(Struct):
    # Windows defines the runtime configuration for Windows based containers, including Hyper-V containers.
          
    def __init__(
        self
    ):

        super().__init__()

        # LayerFolders contains a list of absolute paths to directories containing image layers.
        self.newAttr(name="LayerFolders", attType=[str], jsonName="layerFolders", required=True)
        # Devices are the list of devices to be mapped into the container.
        self.newAttr(name="Devices", attType=[WindowsDevice], jsonName="devices", omitempty=True)
        # Resources contains information for handling resource constraints for the container.
        self.newAttr(name="Resources", attType=WindowsResources, jsonName="resources", omitempty=True)
        # CredentialSpec contains a JSON object describing a group Managed Service Account (gMSA) specification.
        self.newAttr(name="CredentialSpec", attType=dict, jsonName="credentialSpec", omitempty=True)
        # Servicing indicates if the container is being started in a mode to apply a Windows Update servicing operation.
        self.newAttr(name="Servicing", attType=bool, jsonName="servicing", omitempty=True)
        # IgnoreFlushesDuringBoot indicates if the container is being started in a mode where disk writes are not flushed during its boot process.
        self.newAttr(name="IgnoreFlushesDuringBoot", attType=bool, jsonName="ignoreFlushesDuringBoot", omitempty=True)
        # HyperV contains information for running a container with Hyper-V isolation.
        self.newAttr(name="HyperV", attType=WindowsHyperV, jsonName="hyperv", omitempty=True)
        # Network restriction configuration.
        self.newAttr(name="Network", attType=WindowsNetwork, jsonName="network", omitempty=True)


class SolarisAnet(Struct):
    # SolarisAnet provides the specification for automatic creation of network resources for this container.
          
    def __init__(
        self,
        linkname=None,
        lowerLink=None,
        allowedAddress=None,
        configureAllowedAddress=None,
        defrouter=None,
        linkProtection=None,
        macAddress=None
    ):

        super().__init__()

        # Specify a name for the automatically created VNIC datalink.
        self.newAttr(name="Linkname", attType=str, jsonName="linkname", omitempty=True)
        # Specify the link over which the VNIC will be created.
        self.newAttr(name="Lowerlink", attType=str, jsonName="lowerLink", omitempty=True)
        # The set of IP addresses that the container can use.
        self.newAttr(name="Allowedaddr", attType=str, jsonName="allowedAddress", omitempty=True)
        # Specifies whether allowedAddress limitation is to be applied to the VNIC.
        self.newAttr(name="Configallowedaddr", attType=str, jsonName="configureAllowedAddress", omitempty=True)
        # The value of the optional default router.
        self.newAttr(name="Defrouter", attType=str, jsonName="defrouter", omitempty=True)
        # Enable one or more types of link protection.
        self.newAttr(name="Linkprotection", attType=str, jsonName="linkProtection", omitempty=True)
        # Set the VNIC's macAddress
        self.newAttr(name="Macaddress", attType=str, jsonName="macAddress", omitempty=True)

        self.add("Linkname", linkname)
        self.add("Lowerlink", lowerLink)
        self.add("Allowedaddr", allowedAddress)
        self.add("Configallowedaddr", configureAllowedAddress)
        self.add("Defrouter", defrouter)
        self.add("Linkprotection", linkProtection)
        self.add("Macaddress", macAddress)



class SolarisCappedMemory(Struct):
    # SolarisCappedMemory allows users to set the physical and swap caps on the memory that can be used by this container.
          
    def __init__(
        self
    ):

        super().__init__()

        self.newAttr(name="Physical", attType=str, jsonName="physical", omitempty=True)
        self.newAttr(name="Swap", attType=str, jsonName="swap", omitempty=True)


class SolarisCappedCPU(Struct):
    # SolarisCappedCPU allows users to set limit on the amount of CPU time that can be used by container.
          
    def __init__(
        self
    ):

        super().__init__()

        self.newAttr(name="Ncpus", attType=str, jsonName="ncpus", omitempty=True)


class Solaris(Struct):
    # Solaris contains platform-specific configuration for Solaris application containers.
          
    def __init__(
        self,
        milestone=None,
        limitpriv=None,
        maxShmMemory=None,
        anet=None,
        cappedCPU=None,
        cappedMemory=None
    ):

        super().__init__()

        # SMF FMRI which should go "online" before we start the container process.
        self.newAttr(name="Milestone", attType=str, jsonName="milestone", omitempty=True)
        # Maximum set of privileges any process in this container can obtain.
        self.newAttr(name="LimitPriv", attType=str, jsonName="limitpriv", omitempty=True)
        # The maximum amount of shared memory allowed for this container.
        self.newAttr(name="MaxShmMemory", attType=str, jsonName="maxShmMemory", omitempty=True)
        # Specification for automatic creation of network resources for this container.
        self.newAttr(name="Anet", attType=[SolarisAnet], jsonName="anet", omitempty=True)
        # Set limit on the amount of CPU time that can be used by container.
        self.newAttr(name="CappedCPU", attType=SolarisCappedCPU, jsonName="cappedCPU", omitempty=True)
        # The physical and swap caps on the memory that can be used by this container.
        self.newAttr(name="CappedMemory", attType=SolarisCappedMemory, jsonName="cappedMemory", omitempty=True)

        self.add("Milestone", milestone)
        self.add("LimitPriv", limitpriv)
        self.add("MaxShmMemory", maxShmMemory)
        self.add("Anet", anet)
        self.add("CappedCPU", cappedCPU)
        self.add("CappedMemory", cappedMemory)


class LinuxPersonality(Struct):
    # LinuxPersonality represents the Linux personality syscall input
          
    def __init__(
        self
    ):

        super().__init__()

        # Domain for the personality
        self.newAttr(name="Domain", attType=str, jsonName="domain", required=True)
        # Additional flags
        self.newAttr(name="Flags", attType=[str], jsonName="flags", omitempty=True)


class LinuxDeviceCgroup(Struct):
    # LinuxDeviceCgroup represents a device rule for the whitelist controller
          
    def __init__(
        self
    ):

        super().__init__()

        # Allow or deny
        self.newAttr(name="Allow", attType=bool, jsonName="allow", required=True)
        # Device type, block, char, etc.
        self.newAttr(name="Type", attType=str, jsonName="type", omitempty=True)
        # Major is the device's major number.
        self.newAttr(name="Major", attType=int, jsonName="major", omitempty=True)
        # Minor is the device's minor number.
        self.newAttr(name="Minor", attType=int, jsonName="minor", omitempty=True)
        # Cgroup access permissions format, rwm.
        self.newAttr(name="Access", attType=str, jsonName="access", omitempty=True)


class LinuxDevice(Struct):
    # LinuxDevice represents the mknod information for a Linux special device file
          
    def __init__(
        self
    ):

        super().__init__()

        # Path to the device.
        self.newAttr(name="Path", attType=str, jsonName="path", required=True)
        # Device type, block, char, etc.
        self.newAttr(name="Type", attType=str, jsonName="type", required=True)
        # Major is the device's major number.
        self.newAttr(name="Major", attType=int, jsonName="major", required=True)
        # Minor is the device's minor number.
        self.newAttr(name="Minor", attType=int, jsonName="minor", required=True)
        # FileMode permission bits for the device.
        self.newAttr(name="FileMode", attType=str, jsonName="fileMode", omitempty=True)
        # UID of the device.
        self.newAttr(name="UID", attType=int, jsonName="uid", omitempty=True)
        # Gid of the device.
        self.newAttr(name="GID", attType=int, jsonName="gid", omitempty=True)


class LinuxResources(Struct):
    # LinuxResources has container runtime resource constraints
     
    def __init__(
        self
    ):

        super().__init__()

        # Devices configures the device whitelist.
        self.newAttr(name="Devices", attType=[LinuxDeviceCgroup], jsonName="devices", omitempty=True)
        # Memory restriction configuration
        self.newAttr(name="Memory", attType=LinuxMemory, jsonName="memory", omitempty=True)
        # CPU resource restriction configuration
        self.newAttr(name="CPU", attType=LinuxCPU, jsonName="cpu", omitempty=True)
        # Task resource restriction configuration.
        self.newAttr(name="Pids", attType=LinuxPids, jsonName="pids", omitempty=True)
        # BlockIO restriction configuration
        self.newAttr(name="BlockIO", attType=LinuxBlockIO, jsonName="blockIO", omitempty=True)
        # Hugetlb limit (in bytes)
        self.newAttr(name="HugepageLimits", attType=[LinuxHugepageLimit], jsonName="hugepageLimits", omitempty=True)
        # Network restriction configuration
        self.newAttr(name="Network", attType=LinuxNetwork, jsonName="network", omitempty=True)
        # Rdma resource restriction configuration.
        # Limits are a set of key value pairs that define RDMA resource limits,
        # where the key is device name and value is resource limits.
        self.newAttr(name="Rdma", attType=dict, jsonName="rdma", omitempty=True)


class LinuxRdma(Struct):
    # LinuxRdma for Linux cgroup 'rdma' resource management (Linux 4.11)

    def __init__(
        self
    ):

        super().__init__()

        # Maximum number of HCA handles that can be opened. Default is "no limit".
        self.newAttr(name="HcaHandles", attType=int, jsonName="hcaHandles", omitempty=True)
        # Maximum number of HCA objects that can be created. Default is "no limit".
        self.newAttr(name="HcaObjects", attType=int, jsonName="hcaObjects", omitempty=True)


class LinuxNetwork(Struct):
    # LinuxNetwork identification and priority configuration
     
    def __init__(
        self
    ):

        super().__init__()

        # Set class identifier for container's network packets
        self.newAttr(name="ClassID", attType=int, jsonName="classID", omitempty=True)
        # Set priority of network traffic for container
        self.newAttr(name="Priorities", attType=[LinuxInterfacePriority], jsonName="priorities", omitempty=True)


class LinuxPids(Struct):
    # LinuxPids for Linux cgroup 'pids' resource management (Linux 4.3)
     
    def __init__(
        self
    ):

        super().__init__()

        # Maximum number of PIDs. Default is "no limit".
        self.newAttr(name="Limit", attType=int, jsonName="limit", required=True)


class LinuxCPU(Struct):
    # LinuxCPU for Linux cgroup 'cpu' resource management
     
    def __init__(
        self
    ):

        super().__init__()

        # CPU shares (relative weight (ratio) vs. other cgroups with cpu shares).
        self.newAttr(name="Shares", attType=int, jsonName="shares", omitempty=True)
        # CPU hardcap limit (in usecs). Allowed cpu time in a given period.
        self.newAttr(name="Quota", attType=int, jsonName="quota", omitempty=True)
        # CPU period to be used for hardcapping (in usecs).
        self.newAttr(name="Period", attType=int, jsonName="period", omitempty=True)
        # How much time realtime scheduling may use (in usecs).
        self.newAttr(name="RealtimeRuntime", attType=int, jsonName="realtimeRuntime", omitempty=True)
        # CPU period to be used for realtime scheduling (in usecs).
        self.newAttr(name="RealtimePeriod", attType=int, jsonName="realtimePeriod", omitempty=True)
        # CPUs to use within the cpuset. Default is to use any CPU available.
        self.newAttr(name="Cpus", attType=str, jsonName="cpus", omitempty=True)
        # List of memory nodes in the cpuset. Default is to use any available memory node.
        self.newAttr(name="Mems", attType=str, jsonName="mems", omitempty=True)


class LinuxMemory(Struct):
    # LinuxMemory for Linux cgroup 'memory' resource management
     
    def __init__(
        self
    ):

        super().__init__()

        # Memory limit (in bytes).
        self.newAttr(name="Limit", attType=int, jsonName="limit", omitempty=True)
        # Memory reservation or soft_limit (in bytes).
        self.newAttr(name="Reservation", attType=int, jsonName="reservation", omitempty=True)
        # Total memory limit (memory + swap).
        self.newAttr(name="Swap", attType=int, jsonName="swap", omitempty=True)
        # Kernel memory limit (in bytes).
        self.newAttr(name="Kernel", attType=int, jsonName="kernel", omitempty=True)
        # Kernel memory limit for tcp (in bytes)
        self.newAttr(name="KernelTCP", attType=int, jsonName="kernelTCP", omitempty=True)
        # How aggressive the kernel will swap memory pages.
        self.newAttr(name="Swappiness", attType=int, jsonName="swappiness", omitempty=True)
        # DisableOOMKiller disables the OOM killer for out of memory conditions
        self.newAttr(name="DisableOOMKiller", attType=bool, jsonName="disableOOMKiller", omitempty=True)
        # Enables hierarchical memory accounting
        self.newAttr(name="UseHierarchy", attType=bool, jsonName="useHierarchy", omitempty=True)


class LinuxBlockIO(Struct):
    # LinuxBlockIO for Linux cgroup 'blkio' resource management
     
    def __init__(
        self
    ):

        super().__init__()

        # Specifies per cgroup weight
        self.newAttr(name="Weight", attType=int, jsonName="weight", omitempty=True)
        # Specifies tasks' weight in the given cgroup while competing with the cgroup's child cgroups, CFQ scheduler only
        self.newAttr(name="LeafWeight", attType=int, jsonName="leafWeight", omitempty=True)
        # Weight per cgroup per device, can override BlkioWeight
        self.newAttr(name="WeightDevice", attType=[LinuxWeightDevice], jsonName="weightDevice", omitempty=True)
        # IO read rate limit per cgroup per device, bytes per second
        self.newAttr(name="ThrottleReadBpsDevice", attType=[LinuxThrottleDevice], jsonName="throttleReadBpsDevice", omitempty=True)
        # IO write rate limit per cgroup per device, bytes per second
        self.newAttr(name="ThrottleWriteBpsDevice", attType=[LinuxThrottleDevice], jsonName="throttleWriteBpsDevice", omitempty=True)
        # IO read rate limit per cgroup per device, IO per second
        self.newAttr(name="ThrottleReadIOPSDevice", attType=[LinuxThrottleDevice], jsonName="throttleReadIOPSDevice", omitempty=True)
        # IO write rate limit per cgroup per device, IO per second
        self.newAttr(name="ThrottleWriteIOPSDevice", attType=[LinuxThrottleDevice], jsonName="throttleWriteIOPSDevice", omitempty=True)


class LinuxThrottleDevice(Struct):
    # LinuxThrottleDevice struct holds a `major:minor rate_per_second` pair
     
    def __init__(
        self
    ):

        super().__init__()

        # Major is the device's major number.
        self.newAttr(name="Major", attType=int, jsonName="major", required=True)
        # Minor is the device's minor number.
        self.newAttr(name="Minor", attType=int, jsonName="minor", required=True)
        # Rate is the IO rate limit per cgroup per device
        self.newAttr(name="Rate", attType=int, jsonName="rate", required=True)


class LinuxWeightDevice(Struct):
    # LinuxWeightDevice struct holds a `major:minor weight` pair for weightDevice
     
    def __init__(
        self
    ):

        super().__init__()

        # Major is the device's major number.
        self.newAttr(name="Major", attType=int, jsonName="major", required=True)
        # Minor is the device's minor number.
        self.newAttr(name="Minor", attType=int, jsonName="minor", required=True)
        # Weight is the bandwidth rate for the device.
        self.newAttr(name="Weight", attType=int, jsonName="weight", omitempty=True)
        # LeafWeight is the bandwidth rate for the device while competing with the cgroup's child cgroups, CFQ scheduler only
        self.newAttr(name="LeafWeight", attType=int, jsonName="leafWeight", omitempty=True)


class LinuxInterfacePriority(Struct):
    # LinuxInterfacePriority for network interfaces

    def __init__(
        self
    ):

        super().__init__()

        # Name is the name of the network interface
        self.newAttr(name="Name", attType=str, jsonName="name", required=True)
        # Priority for the interface
        self.newAttr(name="Priority", attType=int, jsonName="priority", required=True)


class LinuxHugepageLimit(Struct):
    # LinuxHugepageLimit structure corresponds to limiting kernel hugepages

    def __init__(
        self
    ):

        super().__init__()

        # Pagesize is the hugepage size
        # Format: "<size><unit-prefix>B' (e.g. 64KB, 2MB, 1GB, etc.)
        self.newAttr(name="Pagesize", attType=str, jsonName="pageSize", required=True)
        # Limit is the limit of "hugepagesize" hugetlb usage
        self.newAttr(name="Limit", attType=int, jsonName="limit", required=True)


class POSIXRlimit(Struct):
    # POSIXRlimit type and restrictions

    def __init__(
        self
    ):

        super().__init__()

        # Type of the rlimit to set
        self.newAttr(name="Type", attType=str, jsonName="type", required=True)
        # Hard is the hard limit for the specified type
        self.newAttr(name="Hard", attType=int, jsonName="hard", required=True)
        # Soft is the soft limit for the specified type
        self.newAttr(name="Soft", attType=int, jsonName="soft", required=True)


class LinuxIDMapping(Struct):
    # LinuxIDMapping specifies UID/GID mappings

    def __init__(
        self
    ):

        super().__init__()

        # ContainerID is the starting UID/GID in the container
        self.newAttr(name="ContainerID", attType=int, jsonName="containerID", required=True)
        # HostID is the starting UID/GID on the host to be mapped to 'ContainerID'
        self.newAttr(name="HostID", attType=int, jsonName="hostID", required=True)
        # Size is the number of IDs to be mapped
        self.newAttr(name="Size", attType=int, jsonName="size", required=True)


class LinuxNamespace(Struct):
    # LinuxNamespace is the configuration for a Linux namespace

    def __init__(
        self
    ):

        super().__init__()

        # Type is the type of namespace
        regexp = "^[A-Za-z0-9]$"
        self.newAttr(
            name="Type",
            attType=str,
            jsonName="type",
            regexp=regexp,
            required=True,
        )
        # Path is a path to an existing namespace persisted on disk that can be joined
        # and is of the same type
        self.newAttr(name="Path", attType=str, jsonName="path", omitempty=True)


class Linux(Struct):
    # Linux contains platform-specific configuration for Linux based containers.

    def __init__(
        self
    ):

        super().__init__()

        # UIDMapping specifies user mappings for supporting user namespaces.
        self.newAttr(name="UIDMappings", attType=[LinuxIDMapping], jsonName="uidMappings", omitempty=True)
        # GIDMapping specifies group mappings for supporting user namespaces.
        self.newAttr(name="GIDMappings", attType=[LinuxIDMapping], jsonName="gidMappings", omitempty=True)
        # Sysctl are a set of key value pairs that are set for the container on start
        self.newAttr(name="Sysctl", attType=dict, jsonName="sysctl", omitempty=True)
        # Resources contain cgroup information for handling resource constraints
        # for the container
        self.newAttr(name="Resources", attType=LinuxResources, jsonName="resources", omitempty=True)
        # CgroupsPath specifies the path to cgroups that are created and/or joined by the container.
        # The path is expected to be relative to the cgroups mountpoint.
        # If resources are specified, the cgroups at CgroupsPath will be updated based on resources.
        self.newAttr(name="CgroupsPath", attType=str, jsonName="cgroupsPath", omitempty=True)
        # Namespaces contains the namespaces that are created and/or joined by the container
        self.newAttr(name="Namespaces", attType=[LinuxNamespace], jsonName="namespaces", omitempty=True)
        # Devices are a list of device nodes that are created for the container
        self.newAttr(name="Devices", attType=[LinuxDevice], jsonName="devices", omitempty=True)
        # Seccomp specifies the seccomp security settings for the container.
        self.newAttr(name="Seccomp", attType=LinuxSeccomp, jsonName="seccomp", omitempty=True)
        # RootfsPropagation is the rootfs mount propagation mode for the container.
        self.newAttr(name="RootfsPropagation", attType=str, jsonName="rootfsPropagation", omitempty=True)
        # MaskedPaths masks over the provided paths inside the container.
        self.newAttr(name="MaskedPaths", attType=[str], jsonName="maskedPaths", omitempty=True)
        # ReadonlyPaths sets the provided paths as RO inside the container.
        self.newAttr(name="ReadonlyPaths", attType=[str], jsonName="readonlyPaths", omitempty=True)
        # MountLabel specifies the selinux context for the mounts in the container.
        self.newAttr(name="MountLabel", attType=str, jsonName="mountLabel", omitempty=True)
        # IntelRdt contains Intel Resource Director Technology (RDT) information for
        # handling resource constraints (e.g., L3 cache, memory bandwidth) for the container
        self.newAttr(name="IntelRdt", attType=LinuxIntelRdt, jsonName="intelRdt", omitempty=True)
        # Personality contains configuration for the Linux personality syscall
        self.newAttr(name="Personality", attType=LinuxPersonality, jsonName="personality", omitempty=True)

class Hooks(Struct):
    # Hooks specifies a command that is run in the container at a particular event in the lifecycle of a container
    # Hooks for container setup and teardown

    def __init__(
        self
    ):

        super().__init__()

        # Prestart is Deprecated. Prestart is a list of hooks to be run before the container process is executed.
        # It is called in the Runtime Namespace
        self.newAttr(name="Prestart", attType=[Hook], jsonName="prestart", omitempty=True)
        # CreateRuntime is a list of hooks to be run after the container has been created but before pivot_root or any equivalent operation has been called
        # It is called in the Runtime Namespace
        self.newAttr(name="CreateRuntime", attType=[Hook], jsonName="createRuntime", omitempty=True)
        # CreateContainer is a list of hooks to be run after the container has been created but before pivot_root or any equivalent operation has been called
        # It is called in the Container Namespace
        self.newAttr(name="CreateContainer", attType=[Hook], jsonName="createContainer", omitempty=True)
        # StartContainer is a list of hooks to be run after the start operation is called but before the container process is started
        # It is called in the Container Namespace
        self.newAttr(name="StartContainer", attType=[Hook], jsonName="startContainer", omitempty=True)
        # Poststart is a list of hooks to be run after the container process is started.
        # It is called in the Runtime Namespace
        self.newAttr(name="Poststart", attType=[Hook], jsonName="poststart", omitempty=True)
        # Poststop is a list of hooks to be run after the container process exits.
        # It is called in the Runtime Namespace
        self.newAttr(name="Poststop", attType=[Hook], jsonName="poststop", omitempty=True)


class Hook(Struct):
    # Hook specifies a command that is run at a particular event in the lifecycle of a container

    def __init__(
        self
    ):

        super().__init__()

        self.newAttr(name="Path", attType=str, jsonName="path", required=True)
        self.newAttr(name="Args", attType=[str], jsonName="args", omitempty=True)
        self.newAttr(name="Env", attType=[str], jsonName="env", omitempty=True)
        self.newAttr(name="Timeout", attType=int, jsonName="timeout", omitempty=True)


class Mount(Struct):
    # Mount specifies a mount for a container.

    def __init__(
        self
    ):

        super().__init__()

        # Destination is the absolute path where the mount will be placed in the container.
        self.newAttr(name="Destination", attType=str, jsonName="destination", required=True)
        # Type specifies the mount kind.
        self.newAttr(name="Type", attType=str, jsonName="type", omitempty=True, platform=["linux,solaris"])
        # Source specifies the source path of the mount.
        self.newAttr(name="Source", attType=str, jsonName="source", omitempty=True)
        # Options are fstab style mount options.
        self.newAttr(name="Options", attType=[str], jsonName="options", omitempty=True)


class Root(Struct):
    # Root contains information about the container's root filesystem on the host.

    def __init__(
        self,
        path=None,
        readonly=None
    ):

        super().__init__()

        # Path is the absolute path to the container's root filesystem.
        self.newAttr(name="Path", attType=str, jsonName="path", required=True)
        
        # Readonly makes the root filesystem for the container readonly before the process is executed.
        self.newAttr(name="Readonly", attType=bool, jsonName="readonly", omitempty=True)

        self.add("Path", path)
        self.add("Readonly", readonly)


class User(Struct):
    # User specifies specific user (and group) information for the container process.

    def __init__(
        self,
        uid=None,
        gid=None,
        umask=None,
        additionalGids=None,
        username=None
    ):

        super().__init__()

        # UID is the user id.
        self.newAttr(name="UID", attType=int, jsonName="uid", platform=["linux,solaris"])

        # GID is the group id.
        self.newAttr(name="GID", attType=int, jsonName="gid", platform=["linux,solaris"])

        # Umask is the umask for the init process.
        self.newAttr(name="Umask", attType=int, jsonName="umask", omitempty=True, platform=["linux,solaris"])

        # Umask is the umask for the init process.
        self.newAttr(name="AdditionalGids", attType=[int], jsonName="additionalGids", omitempty=True, platform=["linux,solaris"])

        # Username is the user name.
        self.newAttr(name="Username", attType=str, jsonName="username", omitempty=True, platform=["windows"])

        self.add("UID", uid)
        self.add("GID", gid)
        self.add("Umask", umask)
        self.add("AdditionalGids", additionalGids)
        self.add("Username", username)


class Box(Struct):
    # Box specifies dimensions of a rectangle. Used for specifying the size of a console.

    def __init__(
        self,
        height=None,
        width=None
    ):

        super().__init__()

        # Height is the vertical dimension of a box.
        self.newAttr(name="Height", attType=int, jsonName="height", required=True)
        
        # Width is the horizontal dimension of a box.
        self.newAttr(name="Width", attType=int, jsonName="width", required=True)

        self.add("Height", height)
        self.add("Width", width)



class LinuxCapabilities(Struct):
    # LinuxCapabilities specifies the whitelist of capabilities that are kept for a process.
    # http://man7.org/linux/man-pages/man7/capabilities.7.html

    def __init__(
        self
    ):

        super().__init__()

        # Bounding is the set of capabilities checked by the kernel.
        self.add("Bounding", attType=[str], jsonName="bounding", omitempty=True, platform=["linux"])
        # Effective is the set of capabilities checked by the kernel.
        self.add("Effective", attType=[str], jsonName="effective", omitempty=True, platform=["linux"])
        # Inheritable is the capabilities preserved across execve.
        self.add("Inheritable", attType=[str], jsonName="inheritable", omitempty=True, platform=["linux"])
        # Permitted is the limiting superset for effective capabilities.
        self.add("Permitted", attType=[str], jsonName="permitted", omitempty=True, platform=["linux"])
        # Ambient is the ambient set of capabilities that are kept.
        self.add("Ambient", attType=[str], jsonName="ambient", omitempty=True, platform=["linux"])


class Process(Struct):
    # Process contains information to start a specific application inside the container.

    def __init__(
        self,
        terminal=None,
        consoleSize=None,
        user=None,
        args=None,
        commandLine=None,
        env=None,
        cwd=None,
        capabilities=None,
        rlimits=None,
        noNewPrivileges=None,
        apparmorProfile=None,
        oomScoreAdj=None,
        selinuxLabel=None
    ):

        super().__init__()

        # Terminal creates an interactive terminal for the container.
        self.newAttr(name="Terminal", attType=bool, jsonName="terminal", omitempty=True)
        
        # ConsoleSize specifies the size of the console.
        self.newAttr(name="ConsoleSize", attType=Box, jsonName="consoleSize", omitempty=True)
        
        # User specifies user information for the process.
        self.newAttr(name="User", attType=User, jsonName="user", required=True)
        
        # Args specifies the binary and arguments for the application to execute.
        self.newAttr(name="Args", attType=[str], jsonName="args", omitempty=True)
        
        # CommandLine specifies the full command line for the application to execute on Windows.
        self.newAttr(name="CommandLine", attType=str, jsonName="commandLine", omitempty=True, platform=["windows"])
        
        # Env populates the process environment for the process.
        self.newAttr(name="Env", attType=[str], jsonName="env", omitempty=True)
        
        # Cwd is the current working directory for the process and must be
        # relative to the container's root.
        self.newAttr(name="Cwd", attType=str, jsonName="cwd", required=True)
        
        # Capabilities are Linux capabilities that are kept for the process.
        self.newAttr(name="Capabilities", attType=LinuxCapabilities, jsonName="capabilities", omitempty=True, platform=["linux"])
        
        # Rlimits specifies rlimit options to apply to the process.
        self.newAttr(name="Rlimits", attType=[POSIXRlimit], jsonName="rlimits", omitempty=True, platform=["linux,solaris"])
        
        # NoNewPrivileges controls whether additional privileges could be gained by processes in the container.
        self.newAttr(name="NoNewPrivileges", attType=bool, jsonName="noNewPrivileges", omitempty=True, platform=["linux"])
        
        # ApparmorProfile specifies the apparmor profile for the container.
        self.newAttr(name="ApparmorProfile", attType=str, jsonName="apparmorProfile", omitempty=True, platform=["linux"])
        
        # Specify an oom_score_adj for the container.
        self.newAttr(name="OOMScoreAdj", attType=int, jsonName="oomScoreAdj", omitempty=True, platform=["linux"])
        
        # SelinuxLabel specifies the selinux context that the container process is run as.
        self.newAttr(name="SelinuxLabel", attType=str, jsonName="selinuxLabel", omitempty=True, platform=["linux"])
        
        self.add("Terminal", terminal)
        self.add("ConsoleSize", consoleSize)
        self.add("User", user)
        self.add("Args", args)
        self.add("CommandLine", commandLine)
        self.add("Env", env)
        self.add("Cwd", cwd)
        self.add("Capabilities", capabilities)
        self.add("Rlimits", rlimits)
        self.add("NoNewPrivileges", noNewPrivileges)
        self.add("ApparmorProfile", apparmorProfile)
        self.add("OOMScoreAdj", oomScoreAdj)
        self.add("SelinuxLabel", selinuxLabel)


class Platform(Struct):
    # Platform defines operating system and architecture

    def __init__(
        self,
        os=None,
        arch=None
    ):

        super().__init__()

        # OperatingSystem
        self.newAttr(name="OS", attType=str, jsonName="os", required=True)

        # Architecture
        self.newAttr(name="Architecture", attType=str, jsonName="arch", required=True)

        self.add("OS", os)
        self.add("Architecture", arch)


class Spec(Struct):
    # Spec is the base configuration for the container.

    def __init__(
        self,
        ociVersion=None,
        platform=None,
        process=None,
        root=None,
        hostname=None,
        mounts=None,
        hooks=None,
        annotations=None,
        linux=None,
        solaris=None,
        windows=None,
        vm=None
    ):

        super().__init__()

        # ociVersion of the Open Container Initiative Runtime Specification with which the bundle complies.
        self.newAttr(name="ociVersion", attType=str, jsonName="ociVersion", required=True)

        # Platform configures the container platform.
        self.newAttr(name="Platform", attType=Platform, jsonName="platform", required=True)

        # Process configures the container process.
        self.newAttr(name="Process", attType=Process, jsonName="process", omitempty=True)
        
        # Root configures the container's root filesystem.
        self.newAttr(name="Root", attType=Root, jsonName="root", omitempty=True)
        
        # Hostname configures the container's hostname.
        self.newAttr(name="Hostname", attType=str, jsonName="hostname", omitempty=True)
        
        # Mounts configures additional mounts (on top of Root).
        self.newAttr(name="Mounts", attType=[Mount], jsonName="mounts", omitempty=True)
        
        # Hooks configures callbacks for container lifecycle events.
        self.newAttr(name="Hooks", attType=Hooks, jsonName="hooks", omitempty=True, platform=["linux,solaris"])
        
        # Annotations contains arbitrary metadata for the container.
        self.newAttr(name="Annotations", attType=[str], jsonName="annotations", omitempty=True)
        
        # Linux is platform-specific configuration for Linux based containers.
        self.newAttr(name="Linux", attType=Linux, jsonName="linux", omitempty=True, platform=["linux"])
        
        # Solaris is platform-specific configuration for Solaris based containers.
        self.newAttr(name="Solaris", attType=Solaris, jsonName="solaris", omitempty=True, platform=["solaris"])
        
        # Windows is platform-specific configuration for Windows based containers.
        self.newAttr(name="Windows", attType=Windows, jsonName="windows", omitempty=True, platform=["windows"])
        
        # VM specifies configuration for virtual-machine-based containers.
        self.newAttr(name="VM", attType=VM, jsonName="vm", omitempty=True, platform=["vm"])

        self.add("ociVersion", ociVersion or SpecOCIVersion)
        self.add("Platform", platform)
        self.add("Process", process)
        self.add("Root", root)
        self.add("Hostname", hostname)
        self.add("Mounts", mounts)
        self.add("Hooks", hooks)
        self.add("Annotations", annotations)
        self.add("Linux", linux)
        self.add("Solaris", solaris)
        self.add("Windows", windows)
        self.add("VM", vm)

