# ---------------------------------------------------------- class: Measurement ---------------------------------------------------------- #

class Measurement:

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        func_name: str,
        total_duration: float,
        times_ran: int
    ):
        self.func_name = func_name
        self.total_duration = total_duration
        self.times_ran = times_ran
    

    # ------------------------------------------------------ Public properties ------------------------------------------------------- #

    @property
    def avg_duration(self) -> float:
        return self.total_duration / float(self.times_ran)


# ---------------------------------------------------------------------------------------------------------------------------------------- #