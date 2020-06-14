from darwin_ml import DarwinStateSpace


class DarwinUnittestSetup(DarwinStateSpace):
    def __init__(self):
        super().__init__()
    

    def localized_test_setup(self):
        """
            # Setup Local Test
            ---

            Setups the test locally. All of the data is on Kevin's laptop. Data is already there with the appropiate data.
        """
        self.processor = Jamboree()
        self.asset = "80de790b2d024654b76de0e76a623bcf"
        self.time.head = setup_time()
        try:
            self.change_stepsize(days=1, hours=0, microseconds=0)
            self.change_lookback(days=20, microseconds=0)
            if self.price_count > 0 and self.feature_count == 0:
                self.technical.time.head = time.time()
                self.technical.reset()
                self.technical.time.head = setup_time()
        except Exception:
            pass