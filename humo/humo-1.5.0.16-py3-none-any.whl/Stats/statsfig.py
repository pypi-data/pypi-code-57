import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import math
from scipy import stats



class figure_two_group(object):
    def __init__(self,g1,g2):
        self.g1 = g1
        self.g2 = g2

    def histgram(self):
        x1 = np.linspace(self.g1.min()-20, self.g1.max()+20, num=200)
        x2 = np.linspace(self.g2.min()-20, self.g2.max()+20, num=200)
        kde_model1 = gaussian_kde(self.g1)
        kde_model2 = gaussian_kde(self.g2)
        y1 = kde_model1(x1)
        y2 = kde_model2(x2)

        bin1 = int(np.ceil(np.log2(self.g1.size) + 1)) # Sturges' formula
        bin2 = int(np.ceil(np.log2(self.g2.size) + 1)) # Sturges' formula

        plt.title("Histgram",fontsize=15)
        plt.hist(self.g1,bins=bin1,alpha=0.5)
        plt.hist(self.g2,bins=bin2,alpha=0.5)
        plt.ylabel("Frequency",fontsize=15)
        plt.twinx()
        plt.plot(x1,y1,label="g1")
        plt.plot(x2,y2,label="g2")
        plt.ylabel("Density",fontsize=15)
        plt.legend()

    def QQplot(self,label):
        if label == "g1":
            g = self.g1
        else:
            g = self.g2
        a,b = stats.probplot(g, dist="norm", plot=plt)
        plt.title("Probability Plot : {}".format(label),fontsize=15)

    def unpaired_normality_plot(self,p):
        g1,g2 = self.g1, self.g2
        plt.bar([1,2],
                [g1.mean(),g2.mean()],
                yerr = [g1.std()*2/np.sqrt(g1.size), g2.std()*2/np.sqrt(g2.size)],
                width=0.5,
                align="center",
                capsize=5,
                ecolor="k",
                zorder=6,
                edgecolor="k",
                linewidth=1.5
                )
        plt.xticks([1,2],["g1","g2"],fontsize=15)
        g1_ = g1.mean() + g1.std()*6 / np.sqrt(g1.size)
        g2_ = g2.mean() + g2.std()*6 / np.sqrt(g2.size)
        y_ = g1_ if g1_ > g2_ else g2_
        plt.plot([1,2],[y_,y_],color="k")
        if p < 0.01:
            plt.text(1.5,y_*1.05,"**",fontsize=20)
        elif 0.05 > p >= 0.01:
            plt.text(1.5,y_*1.05,"*",fontsize=20)
        else:
            plt.text(1.5,y_*1.05,"n.s",fontsize=15)
        plt.ylim(0,y_*1.2)
        plt.grid(alpha=0.5,color="gray")

    def unpaired_non_normality_plot(self,p):
        plt.boxplot([self.g1,self.g2],
                    patch_artist=True,  # 細かい設定をできるようにする
                    widths=0.5,  # boxの幅の設定
                    medianprops=dict(color='black', linewidth=1),  # 中央値の線の設定
                    whiskerprops=dict(color='black', linewidth=1),  # ヒゲの線の設定
                    capprops=dict(color='black', linewidth=1),  # ヒゲの先端の線の設定
                    flierprops=dict(markeredgecolor='black', markeredgewidth=1)  # 外れ値の設定
                    )
        plt.xticks([1,2],["g1","g2"],fontsize=15)
        g1_ = self.g1.mean() + self.g1.std()*2
        g2_ = self.g2.mean() + self.g2.std()*2
        y_ = g1_ if g1_ > g2_ else g2_
        plt.plot([1,2],[y_*1.05,y_*1.05],color="k")
        if p < 0.01:
            plt.text(1.5,y_*1.1,"**",fontsize=20)
        elif 0.05 > p >= 0.01:
            plt.text(1.5,y_*1.1,"*",fontsize=20)
        else:
            plt.text(1.5,y_*1.1,"n.s",fontsize=15)
        plt.ylim(0,y_*1.2)
        plt.grid(alpha=0.5,color="gray")

    def paired_plot(self):
        plt.plot(np.array([self.g1,self.g2]),color="b",marker="o",alpha=0.5)
        plt.xticks([0,1],["g1","g2"],fontsize=15)
        plt.grid()

    def paired_plot_ave(self,p):
        g1,g2 = self.g1, self.g2
        plt.errorbar([0,1], [g1.mean(),g2.mean()], yerr=[g1.mean()*2/np.sqrt(g1.size),g2.mean()*2/np.sqrt(g2.size)], marker='o', capthick=1, capsize=10, lw=1)
        plt.xticks([0,1],["g1","g2"],fontsize=15)
        g1_ = g1.mean() + g1.std()*2
        g2_ = g2.mean() + g2.std()*2
        y_ = g1_ if g1_ > g2_ else g2_
        plt.plot([0,1],[y_*1.1,y_*1.1],color="k")
        if p < 0.01:
            plt.text(0.5,y_*1.2,"**",fontsize=20)
        elif 0.05 > p >= 0.01:
            plt.text(0.5,y_*1.2,"*",fontsize=20)
        else:
            plt.text(0.5,y_*1.2,"n.s",fontsize=15)
        plt.ylim(0,y_*1.3)
        plt.grid()

    def basic_statics(self):
        import pandas as pd
        g2_ = pd.Series(self.g2)
        g1_ = pd.Series(self.g1)
        for i,num in zip(g2_.describe().index,np.linspace(0.7,0.1,8)):
            plt.text(0.15,num,i,fontsize=15)
        for i,num in zip(g1_.describe().values,np.linspace(0.7,0.1,8)):
            plt.text(0.35,num,round(i,2),fontsize=15)
        for i,num in zip(g2_.describe().values,np.linspace(0.7,0.1,8)):
            plt.text(0.55,num,round(i,2),fontsize=15)

        plt.text(0.36,0.89,"g1",fontsize=15)
        plt.text(0.56,0.89,"g2",fontsize=15)
        plt.title("Basic statistics",fontsize=15)
        plt.xticks([])
        plt.yticks([])

class oneway_design(object):
    def __init__(self, data, repeat):
        self.data = data
        self.repeat = repeat

    def histgram(self): # >>> OK
        x = [self.data[col].values for col in self.data.columns]
        x_ = [np.linspace(i.min() - 20, i.max() + 20, num = 200) for i in x]
        kde_models = [gaussian_kde(i) for i in x]
        y = [model(i) for model, i in zip(kde_models, x_)]

        bins = [int(np.ceil(np.log2(i.size) + 1)) for i in x]

        plt.title("Histgramu", fontsize=15)
        for num, values in enumerate(x):
            plt.hist(values, bins=bins[num],alpha=0.5)
        plt.ylabel("Frequency",fontsize=15)
        plt.twinx()
        for i, j, level in zip(x_, y, self.data.columns):
            plt.plot(i,j,label=level)
        plt.ylabel("Density",fontsize=15)
        plt.legend()

    def anova_boxplot(self):
        values = [self.data[col] for col in self.data.columns]
        x = np.arange(1,len(values)+1)
        plt.title("Paired plot",fontsize=15)
        plt.boxplot(
            values,
            patch_artist=True,  # 細かい設定をできるようにする
            widths=0.5,  # boxの幅の設定
            medianprops=dict(color='black', linewidth=1),  # 中央値の線の設定
            whiskerprops=dict(color='black', linewidth=1),  # ヒゲの線の設定
            capprops=dict(color='black', linewidth=1),  # ヒゲの先端の線の設定
            flierprops=dict(markeredgecolor='black', markeredgewidth=1)
        )
        plt.xticks(x,self.data.columns,fontsize=15)
        plt.ylabel("Score",fontsize=15)
        if self.repeat == True:
            for i in np.arange(len(self.data)):
                plt.errorbar(
                    x,
                    self.data.iloc[i,:].values,
                    zorder=5,
                    color="g",
                    alpha=0.8,
                    fmt="o",
                    markeredgecolor = "k")
                plt.plot(x,self.data.iloc[i,:].values,color="g")
        else:
            pass

    def anova_plot(self):
        x = np.arange(1,len(self.data.columns) + 1)
        ave = self.data.mean().values
        se = self.data.std(ddof=1)*2 / np.sqrt(len(self.data))
        plt.title("mean ± 2SE",fontsize=15)
        plt.xticks(x,self.data.columns,fontsize=15)
        plt.ylabel("Score",fontsize=15)
        if self.repeat == True:
            plt.errorbar(
                    x,
                    ave,
                    yerr = se,
                    fmt = "o",
                    ms = 8,
                    markeredgecolor = "k",
                    ecolor = "k",
                    capsize = 5
                    )
            plt.plot(x,ave)
            plt.grid()
        else:
            plt.bar(
                x,
                ave,
                yerr = se,
                linewidth = 2,
                width = 0.7,
                capsize = 10
            )
            plt.xticks(x,self.data.columns,fontsize=15)
            plt.grid()

