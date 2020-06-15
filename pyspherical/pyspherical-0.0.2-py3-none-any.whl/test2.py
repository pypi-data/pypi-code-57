    >>> from pyspherical import spin_spherical_harmonic
    >>> from pyspherical import get_cache_details, set_cache_mem_limit, get_cached_dmat, clear_cached_dmat

    >>> lmax = 30
    
    # Running a function, such as spin_spherical_harmonic, will initialize the cached DeltaMatrix.
    >>> spin_spherical_harmonic(0, 1, 1, 0, 1.5, lmax=lmax)
    >>> print(get_cached_dmat().lmax)
    30
    
    >>> spin_spherical_harmonic(0, 1, 1, 0, 1.5, lmax= 2 * lmax)
    >>> print(get_cached_dmat().lmax)
    60
    # Running a function with a lower lmax will not reset this:
    
    >>> spin_spherical_harmonic(0, 1, 1, 0, 1.5, lmax=lmax // 2)
    >>> print(get_cached_dmat().lmax)
    60
    
    # It can be cleared, however:
    >>> clear_cached_dmat()
    >>> print(get_cached_dmat() is None)
    True
    
    # The size of the cached DeltaMatrix is set by lmin and lmax, which are set so the data array doesn't exceed a set memory limit.
    # By default, the limit is 500 MiB = 500 * 2**20
    >>> print(get_cache_details())
    {'cache_mem_limit': 524288000, 'maximum_el': 10238}
    
    # It can be set larger or smaller. e.g., to 30 MiB:
    >>> set_cache_mem_limit(30)
    >>> print(get_cache_details())
    {'cache_mem_limit': 31457280, 'maximum_el': 3964}
    
    # The maximum_el in the above is the maximum value of l that can be handled by a DeltaMatrix within the given limit.
    # For each l, an additional N_l = (l + 1) * (l + 2) // 2 floats are added to the DeltaMatrix. The maximum_el is simply the largest l
    # such that N_l * sizeof(float) <= cache_mem_limit. Anything higher cannot be calculated.
