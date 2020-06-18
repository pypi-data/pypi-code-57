from testcase.app.surface_mse_module import SurfaceMSE
from worker import App


class DrillingEfficiency(App):

    # override
    def get_modules(self):
        return [
            SurfaceMSE
        ]
