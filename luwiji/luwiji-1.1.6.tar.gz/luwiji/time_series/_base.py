import os
from IPython.display import Image

import matplotlib.pyplot as plt
from ipywidgets import interact
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima_process import ArmaProcess


class BaseDemoTimeSeries:
    def __init__(self):
        pass

    @staticmethod
    def _plot(sample):
        plt.figure(figsize=(15, 10))
        plt.subplot(211)
        plt.plot(sample, "b-")

        ax1 = plt.subplot(223)
        plot_acf(sample, lags=50, ax=ax1, title="ACF", color="b", alpha=None);

        ax2 = plt.subplot(224)
        plot_pacf(sample, lags=50, ax=ax2, title="PACF", color="r", alpha=None);

    def AR1_simulation(self):
        def _simul(alpha1=0.6):
            sample = ArmaProcess([1, -alpha1], [1]).generate_sample(250)
            self._plot(sample)

        interact(_simul, alpha1=(-1, 1, 0.1))

    def AR2_simulation(self):
        def _simul(alpha1=0.2, alpha2=0.3):
            sample = ArmaProcess([1, -alpha1, -alpha2], [1]).generate_sample(250)
            self._plot(sample)

        interact(_simul, alpha1=(-1, 1, 0.1), alpha2=(-1, 1, 0.1))

    def MA1_simulation(self):
        def _simul(theta1=0.6):
            sample = ArmaProcess([1], [1, theta1]).generate_sample(250)
            self._plot(sample)

        interact(_simul, theta1=(-1, 1, 0.1))

    def MA2_simulation(self):
        def _simul(theta1=0.6, theta2=0.6):
            sample = ArmaProcess([1], [1, theta1, theta2]).generate_sample(250)
            self._plot(sample)

        interact(_simul, theta1=(-1, 1, 0.1), theta2=(-1, 1, 0.1))

    def AR3MA2_simulation(self):
        def _simul(alpha1=0.2, alpha2=0.3, alpha3=0.4, theta1=0.6, theta2=0.6):
            sample = ArmaProcess([1, -alpha1, -alpha2, -alpha3], [1, theta1, theta2]).generate_sample(250)
            self._plot(sample)

        interact(_simul, alpha1=(-1, 1, 0.1), alpha2=(-1, 1, 0.1), alpha3=(-1, 1, 0.1), theta1=(-1, 1, 0.1), theta2=(-1, 1, 0.1))


class BaseIllustrationTimeSeries:
    def __init__(self):
        here = os.path.dirname(__file__)
        self.ets_model = Image(f"{here}/assets/ets_model.png", width=800)
