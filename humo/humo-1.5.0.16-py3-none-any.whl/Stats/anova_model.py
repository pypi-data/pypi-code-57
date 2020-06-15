import itertools
import numpy as np
import pandas as pd
import pingouin as pg
from pingouin import welch_anova
from pingouin import pairwise_tukey
from pingouin import pairwise_gameshowell
from pingouin import kruskal
from pingouin import pairwise_ttests
from pingouin import friedman
from pingouin import mixed_anova
from scipy import stats


class oneway_anova_model(object):
    def __init__(self,data,repeat,normality,equalvariance):
        self.data = data
        self.repeat = repeat
        self.normality = normality
        self.equalvariance = equalvariance

    def factor(self):
        factor = []
        for col in list(self.data.columns):
            for _ in range(self.data.index.size):
                factor.append(col)
        return factor

    def score(self):
        return self.data.values.T.flatten()

    def sub_id(self):
        return [i + 1 for i in range(self.data.index.size)]*self.data.columns.size

    def DataFrame(self):
        if self.repeat == False:
            factor,score = self.factor(),self.score()
            return pd.DataFrame(
                {"factor":factor,
                "score":score}
                )
        else:
            sub_id,factor,score = self.sub_id(),self.factor(),self.score()
            return pd.DataFrame(
                {"sub_id":sub_id,
                "factor":factor,
                "score":score}
                )

    def analyse(self):
        if self.repeat == False: # one factor ANOVA
            if self.normality == True:
                if self.equalvariance == True:
                    res = pg.anova(
                        data=self.DataFrame(),
                        dv="score",
                        between="factor",
                        detailed=True
                        )
                    significance = True if res["p-unc"][0] < 0.05 else False
                    if significance == True:
                        post_hock = pairwise_tukey(
                            data=self.DataFrame(),
                            dv="score",
                            between="factor"
                            )
                        return res, significance, post_hock
                    else:
                        return res, significance, None
                else:
                    res = pg.welch_anova(
                        data=self.DataFrame(),
                        dv="score",
                        between="factor"
                        )
                    significance = True if res["p-unc"][0] < 0.05 else False
                    if significance == True:
                        post_hock = pairwise_gameshowell(
                            data=self.DataFrame(),
                            dv="score",
                            between="factor"
                            )
                        return res, significance, post_hock
                    else:
                        return res, significance, None
            else:
                res = kruskal(
                    data=self.DataFrame(),
                    dv="score",
                    between="factor"
                    )
                significance = True if res["p-unc"][0] < 0.05 else False
                if significance == True: # Mann-Whitney test
                        post_hock = pairwise_ttests(
                                    data=self.DataFrame(),
                                    dv="score",
                                    within="factor",
                                    parametric=False,
                                    padjust = "holm"
                                        )
                        return res, significance, post_hock
                else:
                    return res, significance, None
        else: # one factor RM-ANOVA
            if self.normality == True:
                if self.equalvariance == True:
                    res = pg.rm_anova(
                            data=self.DataFrame(),
                            dv="score",
                            within="factor",
                            subject="sub_id",
                            detailed=True
                            )
                    significance = True if res["p-unc"][0] < 0.05 else False
                    if significance == True:
                        post_hock  = pairwise_ttests(
                                                    data=self.DataFrame(),
                                                    dv="score",
                                                    between="factor"
                                                    )
                        return res, significance, post_hock
                    else:
                        return res, significance, None
                else: # Greenhouse-Geisser Analysis of variance with ε correction
                    res = pg.rm_anova(
                                data=self.DataFrame(),
                                dv="score",
                                within="factor",
                                subject="subject",
                                detailed=True,
                                correction=True
                                )
                    significance = True if res["p-GG-corr"][0] < 0.05 else False
                    if significance == True:
                        post_hock  = pairwise_ttests(
                                            data=self.DataFrame(),
                                            dv="score",
                                            between="factor"
                                            )
                        return res, significance,post_hock
                    else:
                        return res, significance,None
            else: # friedman test
                res = friedman(
                            data=self.DataFrame(),
                            dv="score",
                            within="factor",
                            subject="sub_id",
                            )
                significance == True if res["p-unc"] < 0.05 else False
                if significance == True: # Wilcoxon
                    post_hock = friedman(
                                    data=self.DataFrame(),
                                    dv="score",
                                    within="factor",
                                    subject="sub_id"
                                    )
                    return res, significance, post_hock
                else:
                    return res, significance, None

class twoway_anova_model(object):
    def __init__(self,data,repeat,split,normality=None,equalvariance=None):
        self.data = data
        self.repeat = repeat
        self.split = split
        self.normality = normality
        self.equalvariance = equalvariance

    def factor(self):
        if (self.split == False) & (self.repeat == False): # twoway anova
            index_counts = []
            for i in self.data.index.unique():
                index_counts.append(list(self.data.index).count(i))

            factor1 = [] # >>> horizontal data columns
            for i in index_counts:
                factor1.append(list(self.data.columns)*i)
            factor1 = list(itertools.chain.from_iterable(factor1))

            factor2 = [] # >>> vertical data index
            for i, j in zip(self.data.index.unique(), index_counts):
                factor2.append([i]*(j * self.data.columns.size))
            factor2 = list(itertools.chain.from_iterable(factor2))

            return factor1, factor2

        elif (self.split == True) & (self.repeat == True): # split anova
            index_counts = []
            for i in self.data.index.unique():
                index_counts.append(list(self.data.index).count(i))

            factor1 = []
            for i in index_counts:
                factor1.append(list(self.data.columns)*i)
            factor1 = list(itertools.chain.from_iterable(factor1))

            factor2 = []
            for i, j in zip(self.data.index.unique(), index_counts):
                factor2.append([i]*(j * self.data.columns.size))
            factor2 = list(itertools.chain.from_iterable(factor2))
            return factor1, factor2
        else: # twoway repeated measure anova
            index_counts = []
            for i in self.data.index.unique():
                index_counts.append(list(self.data.index).count(i))

            factor1 = []
            for i in index_counts:
                factor1.append(list(self.data.columns)*i)
            factor1 = list(itertools.chain.from_iterable(factor1))

            factor2 = []
            for i,j in zip(self.data.index.unique(), index_counts):
                factor2.append([i]*(j * self.data.columns.size))
            factor2 = list(itertools.chain.from_iterable(factor2))
            return factor1, factor2



    def sub_id(self):
        index_counts = []
        for i in self.data.index.unique():
            index_counts.append(list(self.data.index).count(i))

        sub_id = []
        for i in index_counts:
            for j in np.arange(i):
                for _ in np.arange(self.data.columns.size):
                    sub_id.append(j+1)
        sub_id = np.array(sub_id)
        return sub_id

    def sub_id2(self):
        NumofSub = int(len(self.data) / len(self.data.index.unique()))
        sub_id = []
        for i in range(NumofSub):
            sub_id.append([i+1] * len(self.data.columns))
        sub_id = list(itertools.chain.from_iterable(sub_id)) * len(self.data.index.unique())
        return sub_id

    def sub_id3(self): # for split anova
        index_counts = []
        for i in self.data.index.unique():
            index_counts.append(list(self.data.index).count(i))

        sub_id = []
        for i in range(len(self.data)):
            sub_id.append([i+1] * self.data.columns.size)
        sub_id = list(itertools.chain.from_iterable(sub_id))
        return sub_id


    def score(self):
        return self.data.values.flatten()

    def DataFrame(self):
        if (self.repeat == False) & (self.split == False): # twoway anova
            factor1, factor2 = self.factor()
            score = self.score()
            return pd.DataFrame(
                {
                    "factor1":factor1,
                    "factor2":factor2,
                    "score":score
                }
            )
        elif (self.repeat == True) & (self.split == True): # split anova
            factor1, factor2 = self.factor()
            score = self.score()
            sub_id = self.sub_id3()
            return pd.DataFrame(
                {
                    "factor1":factor1,
                    "factor2":factor2,
                    "score":score,
                    "sub_id":sub_id
                }
            )

        else:
            factor1, factor2 = self.factor()
            score = self.score()
            sub_id = self.sub_id2()
            return pd.DataFrame(
                {
                    "factor1":factor1,
                    "factor2":factor2,
                    "score":score,
                    "sub_id":sub_id
                }
            )

    #def DataFrame2(self):
    #    if self.repeat == False:
    #        factor, values = [], []
    #        for col in self.data.columns:
    #            for index in self.data.index.unique():
    #                value = self.data[col][index].values
    #                factor.append(["{} × {}".format(col,index)]*value.size)
    #                values.append(value)
    #        factor = list(itertools.chain.from_iterable(factor))
    #        values = np.array(values).flatten().T
#
    #        return pd.DataFrame(
    #            {
    #                "factor":factor,
    #                "score":values
    #            })
    #    else:
    #        pass

    def DataFrame2(self):
        values, cols = [], []
        for col in self.data.columns:
            for index in self.data.index.unique():
                cols.append("{} × {}".format(col, index))
                values.append(self.data[col][index].values)
        values = np.array(values).T
        return pd.DataFrame(values,columns=cols)

    def DataFrame3(self):
        dataframe = dict()
        for col in self.data.columns:
            for index in self.data.index.unique():
                dataframe[col + " & " + index] = self.data.loc[index][col].values
        return pd.DataFrame(dataframe)


    def check_sphericity(self):
        f1,f2 = dict(), dict()
        for i in self.DataFrame().set_index("factor1").index.unique():
            f1[i] = self.DataFrame().set_index("factor1").loc[i]["score"].values
        for i in self.DataFrame().set_index("factor2").index.unique():
            f2[i] = self.DataFrame().set_index("factor2").loc[i]["score"].values
        f1, f2 = pd.DataFrame(f1), pd.DataFrame(f2)
        return True if (pg.sphericity(f1)[0] == True) & (pg.sphericity(f2)[0] == True) else False

    def analyse(self):
        if (self.repeat == False) & (self.split == False):
            res = pg.anova(
                data=self.DataFrame(),
                dv="score",
                between=["factor1","factor2"],
                detailed=True
            )
            significance = res["p-unc"][0:-1].values < 0.05
            post_hock1 = pairwise_tukey(
                                data = self.DataFrame(),
                                dv = "score",
                                between = "factor1"
                                )
            post_hock2 = pairwise_tukey(
                                data = self.DataFrame(),
                                dv = "score",
                                between = "factor2"
            )
            mdata = self.DataFrame2()
            #onewayanova = mdata.anova(
            #                dv = "score",
            #                between = "factor",
            #                detailed = True
            #)
            #post_hock3 = pairwise_tukey(
            #                data = mdata,
            #                dv = "score",
            #                between = "factor"
            #)
            return res, significance, post_hock1, post_hock2, mdata


        elif (self.repeat == True) & (self.split == True):
            split_anova = mixed_anova(
                                dv="score",
                                between = "factor2",
                                within = "factor1",
                                subject = "sub_id",
                                data = self.DataFrame(),
                                correction = True
            )
            try:
                sphericity = split_anova["sphericity"][1]
                sphericity = True
                significance = split_anova["p-GG-corr"] < 0.05
            except:
                sphericity = False
                significance = split_anova["p-unc"] < 0.05
            if len(self.DataFrame()["factor1"].unique()) == 2:
                a,b = self.DataFrame()["factor1"].unique()
                a,b = self.DataFrame().set_index(["factor1"]).loc[a]["score"].values,self.DataFrame().set_index(["factor1"]).loc[b]["score"].values
                post_hoc1 = pg.ttest(a,b,paired=True)
            else:
                post_hoc1 = pairwise_tukey(
                    data = self.DataFrame(),
                    dv = "score",
                    between = "factor1"
                    )

            if len(self.DataFrame()["factor2"].unique()) == 2:
                a,b = self.DataFrame()["factor2"].unique()
                a,b = self.DataFrame().set_index(["factor2"]).loc[a]["score"].values,self.DataFrame().set_index(["factor2"]).loc[b]["score"].values
                post_hoc2 = pg.ttest(a,b,paired=False)
            else:
                post_hoc2 = pairwise_tukey(
                    data = self.DataFrame(),
                    dv = "score",
                    between = "factor2"
                    )

            # if interaction is True
            post_hoc3 = dict()
            for i in self.DataFrame()["factor2"].unique():
                if self.DataFrame()["factor1"].unique().size != 2:
                    post_hoc3[str(i) + " : Wilcoxon's test"] = self.DataFrame().set_index(["factor2"]).loc[i].pairwise_ttests(dv="score",between="factor1",padjust="holm")
                else:
                    a,b = self.DataFrame()["factor1"].unique()
                    a,b = self.DataFrame().set_index(["factor1"]).loc[a]["score"].values,self.DataFrame().set_index(["factor1"]).loc[b]["score"].values
                    if (stats.shapiro(a)[1] >= 0.05) & (stats.shapiro(a)[1] >= 0.05):
                        if stats.bartlett(a,b)[1] >= 0.05:
                            # student's ttest
                            post_hoc3["{} : student's ttest".format(i)] = pg.ttest(a,b,paired=True,correction=True)
                        else:
                            # welch's ttest
                            post_hoc3["{} : Welch's ttest".format(i)] = pg.ttest(a,b,paired=True,correction=False)
                    else:
                        # mwu ttest
                        post_hoc3["{} : Wilcoxon's test".format(i)] = pg.wilcoxon(a,b)

            post_hoc4 = dict()
            for i in self.DataFrame()["factor1"].unique():
                if self.DataFrame()["factor2"].unique().size != 2:
                    post_hoc4[i + " : TukeyHSD test"] = self.DataFrame().set_index(["factor1"]).loc[i].pairwise_tukey(dv="score",between="factor2")
                else:
                    a,b = self.DataFrame()["factor2"].unique()
                    a,b = self.DataFrame().set_index(["factor2"]).loc[a]["score"].values,self.DataFrame().set_index(["factor2"]).loc[b]["score"].values
                    if (stats.shapiro(a)[1] >= 0.05) & (stats.shapiro(a)[1] >= 0.05):
                        if stats.bartlett(a,b)[1] >= 0.05:
                            # student's ttest
                            post_hoc4["{} : student's ttest".format(i)] = pg.ttest(a,b,paired=False,correction=True)
                        else:
                            # welch's ttest
                            post_hoc4["{} : Welch's ttest".format(i)] = pg.ttest(a,b,paired=False,correction=False)
                    else:
                        # mwu ttest
                        post_hoc4["{} : mwu test".format(i)] = pg.mwu(a,b)
            return split_anova, sphericity, significance, post_hoc1, post_hoc2,post_hoc3, post_hoc4

        elif (self.repeat == True) & (self.split == False):
            RManova = pg.rm_anova(
                data = self.DataFrame(),
                dv = "score",
                within = ["factor1","factor2"],
                subject = "sub_id",
                detailed = True
            )
            sphericity = self.check_sphericity()
            if sphericity == True:
                significance = RManova["p-unc"] < 0.05
            else:
                significance = RManova["p-GG-corr"] < 0.05
            if len(self.DataFrame()["factor1"].unique()) != 2:
                post_hoc1 = pairwise_tukey(
                                data = self.DataFrame(),
                                dv = "score",
                                between = "factor1"
                )
            else:
                a,b = self.DataFrame()["factor1"].unique()
                a,b = self.DataFrame().set_index("factor1").loc[a]["score"].values,self.DataFrame().set_index("factor1").loc[b]["score"].values
                post_hoc1 = pg.ttest(a,b,paired=True)
            if len(self.DataFrame()["factor2"].unique()) != 2:
                post_hoc2 = pairwise_tukey(
                                data = self.DataFrame(),
                                dv = "score",
                                between = "factor2"
                )
            else:
                a,b = self.DataFrame()["factor2"].unique()
                a,b = self.DataFrame().set_index("factor2").loc[a]["score"].values,self.DataFrame().set_index("factor2").loc[b]["score"].values
                post_hoc2 = pg.ttest(a,b,paired=True)
            return RManova, sphericity, significance, post_hoc1, post_hoc2, self.DataFrame3()





        else:
            print("Your experimental condition is an experimental condition with repetition({}) and division({}).".format(self.repeat,self.split))
            print("Unfortunately, the experimental conditions are not supported.")

