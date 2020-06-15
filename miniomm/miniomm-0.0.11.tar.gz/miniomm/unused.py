
def remove_barostat(system):
    """Remove MonteCarloBarostat if present"""
    fs = system.getForces()
    for i, f in enumerate(fs):
        if type(f) == simtk.openmm.openmm.MonteCarloBarostat or \
           type(f) == simtk.openmm.openmm.MonteCarloAnisotropicBarostat:
            system.removeForce(i)
            return
