from .anova_model import oneway_anova_model
from .anova_model import twoway_anova_model
from .equalvaliance import Equalvaliance_test2
from .normality import Normality_test2
from .statsresult import print_res,print_res2,print_res3,print_res4
from .statsfig import oneway_design
import matplotlib.pyplot as plt


class multi_group_comparison(object):
    def __init__(self,data,factor,repeat,split=None):
        self.data = data
        self.repeat = repeat
        self.factor = factor
        self.split = split

    def run_test(self):
        if self.factor == "one": # one factor analysis
            N = Normality_test2(self.data).check_normality()
            V = Equalvaliance_test2(self.data,self.repeat).check_equalvariance()
            model = oneway_anova_model(self.data,self.repeat,N,V)
            res, significance,post_hock = model.analyse()
            print_res(self.factor,self.repeat,N,V,res,significance,post_hock)
        elif self.factor == "two": # two factor analysis
            if (self.repeat == False) & (self.split == False): # twoway anova
                model = twoway_anova_model(self.data, self.repeat, self.split)
                res, significance, post_hock1, post_hock2, mdata = model.analyse()
                N = Normality_test2(mdata).check_normality()
                V = Equalvaliance_test2(mdata,self.repeat).check_equalvariance()
                res2, significance2,post_hock3 = oneway_anova_model(mdata,self.repeat,N,V).analyse()
                print_res2(res,significance,post_hock1,post_hock2,"one",self.repeat,N,V,res2,significance2,post_hock3)
            elif (self.repeat == True) & (self.split == True):
                model = twoway_anova_model(self.data, self.repeat, self.split)
                res = model.analyse()
                print_res3(*res)
            elif (self.repeat == True) & (self.split == False):
                model = twoway_anova_model(self.data, self.repeat, self.split)
                RManova, sphericity, significance, post_hoc1, post_hoc2, mdata = model.analyse()
                N = Normality_test2(mdata).check_normality()
                V = Equalvaliance_test2(mdata,self.repeat).check_equalvariance()
                model2 = oneway_anova_model(mdata,self.repeat,N,V)
                res2, significance2,post_hock2 = model2.analyse()
                print_res4(RManova, sphericity, significance, post_hoc1, post_hoc2,res2, significance2,post_hock2,N,V)



    def dashboard(self):
        fig = oneway_design(self.data, self.repeat)
        plt.figure(figsize=(15,5),dpi=120)
        plt.subplot(1,3,1)
        fig.histgram()
        plt.subplot(1,3,2)
        fig.anova_boxplot()
        plt.subplot(1,3,3)
        fig.anova_plot()
        plt.tight_layout()
        plt.suptitle("Dashboard : oneway anova design(1)",fontsize=25)
        plt.subplots_adjust(top=0.85)