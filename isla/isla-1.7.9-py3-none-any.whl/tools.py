import numpy as np


def sched_build(
    prof_dy, prof_wk=np.zeros(7), prof_yr=np.zeros(12), base_yr=2020
):
    """Builds a schedule for the sched() calculation.

    Parameters
    ----------
    prof_dy : ndarray
        Daily maintenance schedule in hourly resolution. Use 0 for times
        when maintenance is ongoing and 1 when no maintenance is done.
    prof_wk : ndarray
        Weekly maintenance schedule in daily resolution, Days marked 0 will
        adopt the daily maintenance schedule. Should be marked 1 elsewhere.
        First day of the week is Monday.
    prof_yr : ndarray
        Yearly maintenance schedule in monthly resolution. Months marked 0
        will adopt the weekly and daily maintenance schedule. Should be
        marked 1 elsewhere.
    base_yr : ndarray
        Year to base schedule generation on (for aligning weeks and months)

    Returns
    -------
    sched_arr : ndarray
        Yearly maintenance schedule in hourly resolution

    """
    # invert notation: 0 - no maintenance, 1 - maintenance
    sc_dy_hr = 1-prof_dy
    sc_wk_dy = 1-prof_wk
    sc_yr_mo = 1-prof_yr

    # get weekly profile in hourly resolution
    sc_wk_hr = np.tile(sc_dy_hr, 7)*np.repeat(sc_wk_dy, 24)

    # extend monthly profile into hourly resolution
    day_mo = np.cumsum([0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
    sc_yr_hr_a = np.zeros(8760)
    for i in range(12):
        i1 = 24*day_mo[i]
        i2 = 24*day_mo[i+1]
        sc_yr_hr_a[i1:i2] = sc_yr_mo[i]

    # find starting day of the year (zeller's rule)
    ls = (base_yr-1) % 100  # last 2 digits of year
    fs = (base_yr-1)//100  # first 2 digits of year
    dy = (29+ls//4+fs//4+ls-2*fs) % 7  # zeller's rule
    dy_adj = (dy+6) % 7  # adjust so that mon -> 0, sun -> 6

    # extend weekly profile to year length
    sc_yr_hr_b = np.append(
        sc_wk_hr[dy_adj*24:],
        np.tile(sc_wk_hr, 53)
    )[:8760]

    # get yearly profile in hourly resolution
    prof_out = 1-sc_yr_hr_a*sc_yr_hr_b

    return prof_out


def ld_build(ld_data):
    """Extracts the load profile.

    Parameters
    ----------
    ld_data : ndarray
        Array with monthly and daily average load.

    Returns
    -------
    ld_prof : ndarray
        Annual load profile [kW] with hourly resolution.

    """
    # initialize
    day_mo = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    ld_prof = np.array([])

    # assemble load profile
    for i in range(12):
        ld_prof = np.append(
            ld_prof,
            np.tile(ld_data[i, :], day_mo[i])
        )

    return ld_prof
