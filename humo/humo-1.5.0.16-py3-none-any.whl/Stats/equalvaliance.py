import numpy as np
from scipy import stats
import pingouin as pg

class Equalvaliance_test(object):
    def __init__(self,g1,g2):
        self.g1 = g1
        self.g2 = g2

    def equalvariance_value(self):
        df_g1 = len(self.g1) - 1
        df_g2 = len(self.g2) - 1
        if np.var(self.g1) > np.var(self.g2):
            f = np.var(self.g2) / np.var(self.g1)
        else:
            f = np.var(self.g1) / np.var(self.g2)
        F = stats.f.cdf(f,df_g1,df_g2)*2
        return F

    def is_equalvariance(self):
        F = self.equalvariance_value()
        print("Result of F test")
        print("=============================================")
        print("pvalue : {}".format(F))
        if F < 0.05:
            print("variance of group 1 and group 2 are equal")
        else:
            print("variance of group 1 and group 2 are not equal")
        print("==============================================")

    def dicision(self):
        F = self.equalvariance_value()
        if F < 0.05:
            return True
        else:
            return False

class Equalvaliance_test2(object):
    def __init__(self, data, repeat):
        self.data = data
        self.repeat = repeat

    def bartlett_pvalue(self):
        return stats.bartlett(*[self.data[col] for col in self.data.columns])[1]

    def bartlett_statics(self):
        return stats.bartlett(*[self.data[col] for col in self.data.columns])[0]

    def bartlett_values(self):
        return stats.bartlett(*[self.data[col] for col in self.data.columns])

    def check_equalvariance(self):
        if self.repeat == False:
            if self.bartlett_pvalue() >= 0.05:return True
            else:return False
        else:return pg.sphericity(self.data)[0]

    def sphericity_1factor(self):
        return pg.sphericity(self.data)[0]