from otrs_somconnexio.otrs_models.coverage.coverage import Coverage


class VdfFibreCoverage(Coverage):
    VALUES = [
        "FibraCoaxial",
        "FibraVdf",
        "NEBAFTTH",
        "NoFibraVdf",
        "NoRevisat"
    ]
