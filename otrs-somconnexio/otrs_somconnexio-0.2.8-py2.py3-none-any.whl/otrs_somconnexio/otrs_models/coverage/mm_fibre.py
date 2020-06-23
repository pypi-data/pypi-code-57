from otrs_somconnexio.otrs_models.coverage.coverage import Coverage


class MMFibreCoverage(Coverage):
    VALUES = [
        "CoberturaMM",
        "NoFibra",
        "NoRevisat",
        "fibraIndirecta",
    ]
