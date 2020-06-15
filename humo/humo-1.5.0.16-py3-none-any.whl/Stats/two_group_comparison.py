from scipy import stats
import numpy as np
import matplotlib.pyplot as plt

from .normality import Normality_test
from .equalvaliance import Equalvaliance_test
from .statsresult import showResult
from .statsfig import figure_two_group

class two_group_comparison(object):
    def __init__(self,data1,data2,paired):
        self.g1 = data1
        self.g2 = data2
        self.paired = paired

    def run_test(self):
        if self.paired == False: #対応のないt検定
            N = Normality_test(self.g1,self.g2)
            V = Equalvaliance_test(self.g1,self.g2)
            if (N.dicision() == True) & (V.dicision() == True): # student t test
                result = stats.ttest_ind(self.g1,self.g2,equal_var=True)
                showResult(result,
                            "student's t test [parametric]",
                            self.paired,
                            N.dicision(),
                            V.dicision()).print_result()
            elif (N.dicision() == True) & (V.dicision() == False): # welch t test
                result = stats.ttest_ind(self.g1,self.g2,equal_var=False)
                showResult(result,
                            "Welch's t test [parametric]",
                            self.paired,
                            N.dicision(),
                            V.dicision()).print_result()
            elif ((N.dicision() == False) & (V.dicision() == False)) or N.dicision() == False: # mannwhitney U test
                result = stats.mannwhitneyu(self.g1,self.g2,alternative="two-sided")
                showResult(result,
                            "MannWhitney U test [non parametric]",
                            self.paired,
                            N.dicision(),
                            V.dicision()).print_result()
        elif self.paired == True:
            N = Normality_test(self.g1,self.g2)
            if N.dicision() == True:
                result = stats.ttest_rel(self.g1,self.g2)
                showResult(result,
                            "paired t test [parametric]",
                            self.paired,
                            N.dicision()).print_result()
            elif N.dicision() == False:
                result = stats.wilcoxon(self.g1,self.g2,correction=True)
                showResult(result,
                            "Wilcoxon signed rank test [non parametric]",
                            self.paired,
                            N.dicision()).print_result()
    def dashboard(self):
        fig = figure_two_group(self.g1,self.g2)
        if self.paired == False:
            plt.figure(figsize=(15,10),facecolor="w")
            plt.subplot(2,3,1)
            fig.histgram()
            plt.subplot(2,3,2)
            fig.QQplot("g1")
            plt.subplot(2,3,3)
            fig.QQplot("g2")
            plt.subplot(2,3,4)
            N = Normality_test(self.g1,self.g2).dicision()
            V = Equalvaliance_test(self.g1,self.g2).dicision()
            if (N == True) & (V == True):
                p = stats.ttest_ind(self.g1,self.g2,equal_var=True)[1]
                fig.unpaired_normality_plot(p)
            elif (N == True) & (V == False):
                p = stats.ttest_ind(self.g1,self.g2,equal_var=False)[1]
                fig.unpaired_non_normality_plot(p)
            elif ((N == False) & (V == False)) or N == False:
                p = stats.mannwhitneyu(self.g1,self.g2,alternative="two-sided")[1]
                fig.unpaired_non_normality_plot(p)
            plt.subplot(2,3,5)
            fig.basic_statics()

            plt.tight_layout()
            plt.suptitle("Statistical analysis dashboard between two groups",fontsize=30)
            plt.subplots_adjust(top=0.9)

        elif self.paired == True:
            plt.figure(figsize=(15,10),facecolor="w")
            plt.subplot(2,3,1)
            fig.histgram()
            plt.subplot(2,3,2)
            fig.QQplot("g1")
            plt.subplot(2,3,3)
            fig.QQplot("g2")
            plt.subplot(2,3,4)
            fig.paired_plot()
            plt.subplot(2,3,5)
            p = stats.ttest_rel(self.g1,self.g2)[1]
            fig.paired_plot_ave(p)
            plt.subplot(2,3,6)
            fig.basic_statics()

            plt.tight_layout()
            plt.suptitle("Statistical analysis dashboard between two groups",fontsize=30)
            plt.subplots_adjust(top=0.9)
