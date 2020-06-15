from pandas import set_option,get_option


set_option('display.width',1000)
get_option('display.max_colwidth',1000)

class showResult(object):
    def __init__(self,data,statsname,paired,N,V=None):
        self.data = data
        self.statsname = statsname
        self.paired = paired
        self.N = N
        self.V = V

    def print_result(self):
        print("Normality : {}".format(self.N))
        if self.paired == False:
            print("Homogeneity of variance : {}".format(self.V))
        else:
            pass
        print(">>> {} was performed.".format(self.statsname))
        print("===================================================")
        print("Result of test")
        print("===================================================")
        print("statics : {}".format(self.data[0]))
        print("p values : {}".format(self.data[1]))

        if (self.data[1] < 0.05) & (self.paired == False):
            print("There was {} significant difference in the mean values.".format("a"))
        elif (self.data[1] >= 0.05)& (self.paired == False):
            print("There was {} significant difference in the mean values.".format("no"))
        elif (self.data[1] < 0.05) & (self.paired == True):
            print("There was {} significant difference in the difference in change.".format("a"))
        else:
            print("There was {} significant difference in the difference in change.".format("no"))


class StatsText(object):
    def __init__(self,factor,repeat,N,V):
        self.factor = factor
        self.repeat = repeat
        self.N = N
        self.V = V

    def result_of_analysis1(self):
        print("Result of analysis".center(50))
        print("======================================================================")
        print("Factor    : {}  Repeat          : {}".format(self.factor,self.repeat))
        print("Normarity : {}".format(self.N))
        print("Equal variance : {}".format(self.V))

    def result_of_analysis1_repeat(self):
        print("Result of analysis".center(50))
        print("======================================================================")
        print("Factor    : {}   Repeat          : {}".format(self.factor,self.repeat))
        print("Normarity : {}".format(self.N))
        print("Sphericity : {}".format(self.V))

    def result_of_analysis2(self,name,res):
        print(">>> {} was applied.".format(name))
        print("----------------------------------------------------------------------")
        print("")
        print("[{}]".format(name))
        print(res)

    def result_of_analysis3(self,name,significance,post_hock):
        if significance == True:
            print("Significant differences were observed between either group.")
            print(">>> {} test was applied.".format(name))
            print("----------------------------------------------------------------------")
            print("")
            print("[{} test]".format(name))
            print(post_hock)
            print("======================================================================")
        else:
            print("There was no significant difference.")
            print("======================================================================")


def print_res(factor,repeat,N,V,res,significance,post_hock):
    text = StatsText(factor,repeat,N,V)
    if repeat == False: # one factor ANOVA
        text.result_of_analysis1()
        if N == True:
            if V == True:
                text.result_of_analysis2("A one-way analysis of variance",res)
                text.result_of_analysis3("TukeyHSD",significance,post_hock)
            else:
                text.result_of_analysis2("A one-way analysis of variance with a modified Welch",res)
                text.result_of_analysis3("The Games-Howell test",significance,post_hock)

        else:
            text.result_of_analysis2("The Kruskal-Wallis test",res)
            text.result_of_analysis3("Mann-Whitney U test with p-value corrected by holm method",significance,post_hock)
    else: # one factor RM-ANOVA
        text.result_of_analysis1_repeat()
        if N == True:
            if V == True:
                text.result_of_analysis2("A one-way repeaed measure analysis of variance",res)
                text.result_of_analysis3("pairwise_ttests test with p-value corrected by holm method",significance,post_hock)
            else:
                text.result_of_analysis2("Analysis of variance using Greenhouse-Geisser ε correction",res)
                text.result_of_analysis3("pairwise_ttests test with p-value corrected by holm method",significance,post_hock)
        else:
            text.result_of_analysis2("The Friedman test",res)
            text.result_of_analysis3("Matched pair test of Wilcoxon test with p-value corrected by holm method",significance,post_hock)

def print_res2(res,significance,post_hock1,post_hock2,factor,repeat,N,V,res2,significance2,post_hock3):
    print("Result of twoway anova")
    print("=================================================================================")
    print(res)
    if significance[-1] == True:
        print("---------------------------------------------------------------------------------")
        print("An interaction was observed.")
        print("a oneway anova was performed as a subtest.")
        print("")
        print("↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓    ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓    ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓")
        print("")
        print_res(factor,repeat,N,V,res2,significance2,post_hock3)
        print("")
        if (significance[0] == False) & (significance[1] == False):
            print("The main effect was not observed.")
        else:
            print("↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓    ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓    ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓")
            print("")
            print("Since some main effect was observed, the simple main effect was tested.")
            print("[Supplementary data - TukeyHSD test]")
            if (significance[0] == True) & (significance[1] == True):
                print(">>> facotr1")
                print(post_hock1)
                print("--------------------------------------------------------------------------")
                print(">>> facotr2")
                print(post_hock2)
            elif (significance[0] == True) & (significance[1] == False):
                print(">>> facotr1 only")
                print(post_hock1)
            elif (significance[0] == False) & (significance[1] == True):
                print(">>> facotr2 only")
                print(post_hock2)
    else:
        print("")
        if (significance[0] == False) & (significance[1] == False):
            print("There were no significant differences.")
        else:
            print("↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓    ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓    ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓")
            print("")
            print("Since some main effect was observed, the simple main effect was tested.")
            print("[TukeyHSD test]")
            if (significance[0] == True) & (significance[1] == True):
                print(">>> facotr1")
                print(post_hock1)
                print("--------------------------------------------------------------------------")
                print(">>> facotr2")
                print(post_hock2)
            elif (significance[0] == True) & (significance[1] == False):
                print(">>> facotr1 only")
                print(post_hock1)
            elif (significance[0] == False) & (significance[1] == True):
                print(">>> facotr2 only")
                print(post_hock2)

def print_res3(split_anova,sphericity, significance, post_hoc1, post_hoc2, post_hoc3,post_hoc4):
    print("Result of split designed anova : sphericity is {}".format(sphericity))
    print("="*121)
    print(split_anova)
    if significance[2] == True:
        print('"The interaction" was observed.')
        print("")
        print("↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓                   "*3)
        print("↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓                   "*3)
        print("")
        print("[Rsult of post hoc test]")
        for key in post_hoc3.keys():
            print("[factor1 (Paired level) >>> {}]".format(key))
            print("-"*86)
            print(post_hoc3[key])
            print("")
        print("")
        for key in post_hoc4.keys():
            print("[factor2 (Unpaired level)>>> {}]".format(key))
            print("-"*86)
            print(post_hoc4[key])
            print("")
        print("="*121)
    else:
        print("There was no interaction.")
        print("")
        print("↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓                   "*3)
        print("↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓                   "*3)
        print("")
        print("[Rsult of post hoc test]")
        print("[factor1]")
        print("-"*86)
        print(post_hoc1)
        print("[factor2]")
        print("-"*86)
        print(post_hoc2)
        print("="*121)

def print_res4(RManova, sphericity, significance, post_hoc1, post_hoc2,res2, significance2,post_hock2,N,V):
    print("Result of twoway repeated measure anova : sphericity is {}".format(sphericity))
    print("="*121)
    print(RManova)
    if significance[2] == True:
        print('"The interaction" was observed.')
        print("")
        print("↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓                   "*3)
        print("↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓                   "*3)
        print("")
        print("[Rsult of oneway repeated measure anova]")
        print_res("one",True,N,V,res2,significance2,post_hock2)
    else:
        print("There was no interaction.")
        if (significance[0] == True) & (significance[1] == True):
            print("The main effect was recognized in factor1 and factor2.")
            print("")
            print("↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓                   "*3)
            print("↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓                   "*3)
            print("")
            print("[Rsult of post hoc test]")
            print("[factor1]")
            print("-"*86)
            print(post_hoc1)
            print("[factor2]")
            print("-"*86)
            print(post_hoc2)
            print("="*121)
        elif (significance[0] == True) & (significance[1] == False):
            print("The main effect was recognized in factor1 only.")
            print("")
            print("↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓                   "*3)
            print("↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓                   "*3)
            print("")
            print("[Rsult of post hoc test]")
            print("[factor1 only]")
            print("-"*86)
            print(post_hoc1)
        elif (significance[0] == False) & (significance[1] == True):
            print("The main effect was recognized in factor2 only.")
            print("")
            print("↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓                   "*3)
            print("↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓                   "*3)
            print("")
            print("[Rsult of post hoc test]")
            print("[factor2 only]")
            print("-"*86)
            print(post_hoc2)
        else:
            print("There was no significant difference.")