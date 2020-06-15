from scipy import stats
import numpy as np

class Normality_test(object):
    def __init__(self,g1,g2):
        self.g1 = g1
        self.g2 = g2

    def is_normality(self):
        g1 = stats.shapiro(self.g1)
        g2 = stats.shapiro(self.g2)
        print("Results of shapiro's test")
        print("===========group1===========")
        print("W : {}".format(g1[0]))
        print("pvalues : {}".format(g1[1]))
        if g1[1] > 0.05:
            print("group 1 indicates normality.")
        else:
            print("group 1 dose not indicates normality.")
        print("============================")
        print("")
        print("===========group2===========")
        print("W : {}".format(g2[0]))
        print("pvalues : {}".format(g2[1]))
        if g2[1] > 0.05:
            print("group 2 indicates normality.")
        else:
            print("group 2 dose not indicates normality.")
        print("============================")

    def shapiro_pvalue(self):
        return stats.shapiro(self.g1)[1], stats.shapiro(self.g2)[1]

    def shapiro_statics(self):
        return stats.shapiro(self.g1)[0], stats.shapiro(self.g2)[0]

    def shapiro(self):
        return stats.shapiro(self.g1), stats.shapiro(self.g2)

    def dicision(self):
        a,b = self.shapiro_pvalue()
        if (a > 0.05) & (b > 0.05):
            return True
        else:
            return False

class Normality_test2(object):
    def __init__(self,data):
        self.data = data

    def shapiro_pvalues(self):
        levels = [self.data[col] for col in self.data.columns]
        p_values = [stats.shapiro(i)[1] for i in levels]
        return np.array(p_values)

    def shapiro_statics(self):
        levels = [self.data[col] for col in self.data.columns]
        p_values = [stats.shapiro(i)[0] for i in levels]
        return np.array(p_values)

    def shapiro_values(self):
        levels = [self.data[col] for col in self.data.columns]
        p_values = [stats.shapiro(i) for i in levels]
        return np.array(p_values)

    def check_normality(self):
        """
        Check the normality of each level.
        Returns
            - True if normality can be assumed at all levels
            - False if no normality can be assumed.
        """
        if False in self.shapiro_pvalues() >= 0.05:return False
        else:return True