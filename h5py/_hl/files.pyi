from typing import Final

from .group import Group

mpi: Final[bool]

def register_driver(name, set_fapl):  # -> None:
    """Register a custom driver.

    Parameters
    ----------
    name : str
        The name of the driver.
    set_fapl : callable[PropFAID, **kwargs] -> NoneType
        The function to set the fapl to use your custom driver.
    """
    ...

def unregister_driver(name):  # -> None:
    """Unregister a custom driver.

    Parameters
    ----------
    name : str
        The name of the driver.
    """
    ...

def registered_drivers():  # -> frozenset[str]:
    """Return a frozenset of the names of all of the registered drivers."""
    ...

def make_fapl(
    driver,
    libver,
    rdcc_nslots,
    rdcc_nbytes,
    rdcc_w0,
    locking,
    page_buf_size,
    min_meta_keep,
    min_raw_keep,
    alignment_threshold,
    alignment_interval,
    meta_block_size,
    **kwds,
):
    """Set up a file access property list"""
    ...

def make_fcpl(track_order=..., fs_strategy=..., fs_persist=..., fs_threshold=..., fs_page_size=...):  # -> None:
    """Set up a file creation property list"""
    ...

def make_fid(name, mode, userblock_size, fapl, fcpl=..., swmr=...):
    """Get a new FileID by opening or creating a file.
    Also validates mode argument."""
    ...

class File(Group):
    """
    Represents an HDF5 file.
    """
    @property
    def attrs(self):  # -> AttributeManager:
        """Attributes attached to this object"""
        ...

    @property
    def filename(self):  # -> str:
        """File name on disk"""
        ...

    @property
    def driver(self):  # -> str:
        """Low-level HDF5 file driver used to open file"""
        ...

    @property
    def mode(self):  # -> Literal['r+', 'r']:
        """Python mode used to open file"""
        ...

    @property
    def libver(self):  # -> tuple[str, ...]:
        """File format version bounds (2-tuple: low, high)"""
        ...

    @property
    def userblock_size(self):
        """User block size (in bytes)"""
        ...

    @property
    def meta_block_size(self):
        """Meta block size (in bytes)"""
        ...

    if mpi:
        @property
        def atomic(self):
            """Set/get MPI-IO atomic mode"""
            ...

        @atomic.setter
        def atomic(self, value):  # -> None:
            ...

    @property
    def swmr_mode(self):  # -> bool:
        """Controls single-writer multiple-reader mode"""
        ...

    @swmr_mode.setter
    def swmr_mode(self, value):  # -> None:
        ...
    def __init__(
        self,
        name,
        mode=...,
        driver=...,
        libver=...,
        userblock_size=...,
        swmr=...,
        rdcc_nslots=...,
        rdcc_nbytes=...,
        rdcc_w0=...,
        track_order=...,
        fs_strategy=...,
        fs_persist=...,
        fs_threshold=...,
        fs_page_size=...,
        page_buf_size=...,
        min_meta_keep=...,
        min_raw_keep=...,
        locking=...,
        alignment_threshold=...,
        alignment_interval=...,
        meta_block_size=...,
        **kwds,
    ) -> None:
        """Create a new file object.

        See the h5py user guide for a detailed explanation of the options.

        name
            Name of the file on disk, or file-like object.  Note: for files
            created with the 'core' driver, HDF5 still requires this be
            non-empty.
        mode
            r        Readonly, file must exist (default)
            r+       Read/write, file must exist
            w        Create file, truncate if exists
            w- or x  Create file, fail if exists
            a        Read/write if exists, create otherwise
        driver
            Name of the driver to use.  Legal values are None (default,
            recommended), 'core', 'sec2', 'direct', 'stdio', 'mpio', 'ros3'.
        libver
            Library version bounds.  Supported values: 'earliest', 'v108',
            'v110', 'v112'  and 'latest'.
        userblock_size
            Desired size of user block.  Only allowed when creating a new
            file (mode w, w- or x).
        swmr
            Open the file in SWMR read mode. Only used when mode = 'r'.
        rdcc_nbytes
            Total size of the dataset chunk cache in bytes. The default size
            is 1024**2 (1 MiB) per dataset. Applies to all datasets unless individually changed.
        rdcc_w0
            The chunk preemption policy for all datasets.  This must be
            between 0 and 1 inclusive and indicates the weighting according to
            which chunks which have been fully read or written are penalized
            when determining which chunks to flush from cache.  A value of 0
            means fully read or written chunks are treated no differently than
            other chunks (the preemption is strictly LRU) while a value of 1
            means fully read or written chunks are always preempted before
            other chunks.  If your application only reads or writes data once,
            this can be safely set to 1.  Otherwise, this should be set lower
            depending on how often you re-read or re-write the same data.  The
            default value is 0.75. Applies to all datasets unless individually changed.
        rdcc_nslots
            The number of chunk slots in the raw data chunk cache for this
            file. Increasing this value reduces the number of cache collisions,
            but slightly increases the memory used. Due to the hashing
            strategy, this value should ideally be a prime number. As a rule of
            thumb, this value should be at least 10 times the number of chunks
            that can fit in rdcc_nbytes bytes. For maximum performance, this
            value should be set approximately 100 times that number of
            chunks. The default value is 521. Applies to all datasets unless individually changed.
        track_order
            Track dataset/group/attribute creation order under root group
            if True. If None use global default h5.get_config().track_order.
        fs_strategy
            The file space handling strategy to be used.  Only allowed when
            creating a new file (mode w, w- or x).  Defined as:
            "fsm"        FSM, Aggregators, VFD
            "page"       Paged FSM, VFD
            "aggregate"  Aggregators, VFD
            "none"       VFD
            If None use HDF5 defaults.
        fs_page_size
            File space page size in bytes. Only used when fs_strategy="page". If
            None use the HDF5 default (4096 bytes).
        fs_persist
            A boolean value to indicate whether free space should be persistent
            or not.  Only allowed when creating a new file.  The default value
            is False.
        fs_threshold
            The smallest free-space section size that the free space manager
            will track.  Only allowed when creating a new file.  The default
            value is 1.
        page_buf_size
            Page buffer size in bytes. Only allowed for HDF5 files created with
            fs_strategy="page". Must be a power of two value and greater or
            equal than the file space page size when creating the file. It is
            not used by default.
        min_meta_keep
            Minimum percentage of metadata to keep in the page buffer before
            allowing pages containing metadata to be evicted. Applicable only if
            page_buf_size is set. Default value is zero.
        min_raw_keep
            Minimum percentage of raw data to keep in the page buffer before
            allowing pages containing raw data to be evicted. Applicable only if
            page_buf_size is set. Default value is zero.
        locking
            The file locking behavior. Defined as:

            - False (or "false") --  Disable file locking
            - True (or "true")   --  Enable file locking
            - "best-effort"      --  Enable file locking but ignore some errors
            - None               --  Use HDF5 defaults

            .. warning::

                The HDF5_USE_FILE_LOCKING environment variable can override
                this parameter.

            Only available with HDF5 >= 1.12.1 or 1.10.x >= 1.10.7.

        alignment_threshold
            Together with ``alignment_interval``, this property ensures that
            any file object greater than or equal in size to the alignment
            threshold (in bytes) will be aligned on an address which is a
            multiple of alignment interval.

        alignment_interval
            This property should be used in conjunction with
            ``alignment_threshold``. See the description above. For more
            details, see
            https://portal.hdfgroup.org/display/HDF5/H5P_SET_ALIGNMENT

        meta_block_size
            Set the current minimum size, in bytes, of new metadata block allocations.
            See https://portal.hdfgroup.org/display/HDF5/H5P_SET_META_BLOCK_SIZE

        Additional keywords
            Passed on to the selected file driver.
        """
        ...

    def close(self):  # -> None:
        """Close the file.  All open objects become invalid"""
        ...

    def flush(self):  # -> None:
        """Tell the HDF5 library to flush its buffers."""
        ...

    def __enter__(self):  # -> Self:
        ...
    def __exit__(self, *args):  # -> None:
        ...
    def __repr__(self):  # -> str:
        ...
