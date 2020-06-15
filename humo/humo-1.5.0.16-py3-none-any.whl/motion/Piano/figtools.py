import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas as pd

plt.rcParams['xtick.direction'] = 'in'
plt.rcParams["figure.facecolor"]="w"
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.major.width'] = 1.2
plt.rcParams['ytick.major.width'] = 1.2
plt.rcParams['axes.linewidth'] = 1.2
plt.rcParams['grid.linestyle']='--'
plt.rcParams['grid.linewidth'] = 0.5
plt.rcParams['font.size'] = 15
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False
plt.rcParams["axes.edgecolor"] = "grey"

colors = [cm.RdBu(0.85), cm.RdBu(0.7), cm.PiYG(0.7), cm.Spectral(0.38), cm.Spectral(0.25)]

label1 = ["near","mid","far"]
label2 = ["sub{}".format(i+1) for i in range(4) ]

def accuracy_of_tempi(sub,cond):
    """Summary line.
    Indicates the accuracy of keying tempo.
    Visualize the accuracy of keying tempo for each subject for each experimental condition.
    The left figure is for each subject, and the right figure is for each experimental condition.

    Parameters
    ----------
    sub : np.ndarray
        shape is (3,n,10).
        n is the number of subjects.

    cond : np.ndarray
        shape is (3,n).
        n is the number of subjects.

    Returns
    -------
    figure(1,2,1).
    Left  : each subjects.
    Right : each condition
    """
    subs = [sub.mean(2),sub.std(2,ddof=1)]
    conds = [cond.mean(1),cond.std(1,ddof=1)]
    x1,x2,h = np.linspace(1,6,4),np.linspace(1,2,3),0.3
    fig, axes = plt.subplots(1,2,figsize=(18,8),sharey=True,facecolor="w")
    # plotting each subject data
    for i in range(3):
        axes[0].bar(
            x1+i*h, subs[0][i],
            yerr = subs[1][i], ecolor="grey",
            width = h, label=label1[i],
            zorder=2, alpha=0.8
        )
        axes[0].set_title("Tempo accuracy between subjects",fontsize=20,color="grey")
        axes[0].set_ylabel("Time [Frame]",fontsize=15,color="grey")
        axes[0].set_xticks(x1+h)
        axes[0].set_xticklabels(label2,color="grey",fontsize=15)
        axes[0].set_yticklabels(np.arange(0,101,20),color="grey",fontsize=15)
        axes[0].legend(edgecolor="none")
        axes[0].yaxis.grid()

    # plotting each condition data
        axes[1].bar(
            i/2, conds[0][i],
            yerr = conds[1][i], ecolor="grey",
            width=h, color=colors[i+1]
        )
        axes[1].text(
            i/2+0.05, conds[0][i]+4,
            round(conds[0][i],1),
            color="grey",fontsize=15
        )
        axes[1].set_title("Tempo accuracy between conditions",fontsize=20,color="grey")
        axes[1].set_xticks([0,0.5,1.])
        axes[1].set_xticklabels(label1,fontsize=15,alpha=0.5)
        axes[1].set_yticklabels(np.arange(0,101,20),color="grey",fontsize=15)
        axes[1].yaxis.grid()

def tempi_histogram(hist_condition,subs):
    fig = plt.figure(figsize=(15,10),facecolor="w")
    for num,i in enumerate(np.arange(1,4)):
        ax = fig.add_subplot(2,3,i)
        ax.set_title("{} condition".format(["near","mid","far"][num]),fontsize=20)
        pd.Series(hist_condition[num]).plot("hist",color=colors[i])
        pd.Series(hist_condition[num]).plot("kde",secondary_y=True,color="k",alpha=0.6,ls="--")
        ax.yaxis.grid()
    for num, j in enumerate(np.arange(4,7)):
        ax = fig.add_subplot(2,3,j)
        for sub_num, k in enumerate(subs[num]):
            pd.Series(k).plot("kde",label="sub{}".format(sub_num+1),alpha=0.7,lw=3,zorder=3)
            ax.axvline(67,color="r",ls="--",alpha=0.5,zorder=0)
            ax.legend()
        ax.yaxis.grid()
    fig.tight_layout()
    fig.suptitle("Histgram of tempi",fontsize=20)
    plt.subplots_adjust(top=0.9)

def KP_MP_ratio(nKP,nMP):
    fig,ax = plt.subplots(figsize=(10,10),facecolor="w")
    ax.set_xticks([0,1,2])
    ax.set_xticklabels(["near","mid","far"],fontsize=25,color="grey")
    ax.set_yticks(np.arange(0,101,20))
    ax.set_yticklabels(np.arange(0,101,20),color="grey",fontsize=20)
    ax.bar(np.arange(3),nKP,width=0.7,alpha=0.5,label="keying phase")
    for num,i in enumerate(nKP):
        ax.text(num-0.15, 15, "{}%".format(round(i)),fontsize=20,color="grey")
    ax.bar(np.arange(3),nMP,bottom=nKP,width=0.7,alpha=0.5,label="moving phase")
    for num, i in enumerate(nMP):
        ax.text(num-0.15, 60, "{}%".format(round(i)),fontsize=20,color='grey')
    ax.legend(bbox_to_anchor=(1, 0.95),fontsize=15)
    ax.set_title("Percentage of keying time and movement time",fontsize=30,color="grey")
    ax.yaxis.grid()

def KP_MP_ratio2(nKPs,nMPs):
    width,h = 0.3,0.4
    fig, ax = plt.subplots(figsize=(8,8),facecolor="w")
    for i in range(3):
        ax.bar(np.arange(1,8,2)+h*i,nKPs[i],width=width,color="#1f77b4",alpha=[0.8,0.6,0.4][i])
        ax.bar(np.arange(1,8,2)+h*i,nMPs[i],width=width,alpha=[0.8,0.6,0.4][i],bottom=nKPs[i],color="#ff7f0e")
    ax.set_xticks(np.arange(1,8,2)+h)
    ax.set_xticklabels(["sub1","sub2","sub3","sub4"],fontsize=20,color="grey")
    ax.legend(["keying phase","moving phase"],bbox_to_anchor=(1, 0.95),fontsize=15)
    ax.set_title("Comparison of keying and moving phase for each subject",fontsize=20,color="grey")
    ax.set_yticks(np.arange(0,101,20))
    ax.set_yticklabels(np.arange(0,101,20),color="grey",fontsize=15)
    ax.yaxis.grid()

def speed_of_handCOM(SOH,SOH_max):
    fig, ax = plt.subplots(1,2,figsize=(20,9),facecolor="w")
    for i in range(3):
        ax[0].plot(SOH.mean(1)[i],color=colors[i+1],lw=5)
        ax[0].text(1020,SOH.mean(1)[i][-1],["near","mid","far"][i],fontsize=25,color=colors[i+1])
    ax[0].set_title("The speed of hand COM",color="grey",fontsize=25)
    ax[0].set_xticks(np.arange(0,1001,100))
    ax[0].set_xticklabels(np.arange(0,101,10),color="grey",fontsize=15)
    ax[0].set_xlabel("Time [%]",color="grey",fontsize=20)
    ax[0].set_yticks(np.arange(0,8,1))
    ax[0].set_yticklabels(np.arange(0,8,1),color="grey",fontsize=15)
    ax[0].set_ylabel("Speed [mm/sec]",color="grey",fontsize=20)
    ax[0].yaxis.grid()

    for i in range(3):
        ax[1].bar(i,SOH_max.mean(1)[i],yerr=SOH_max.std(1,ddof=1)[i],
        color=colors[i+1],ecolor="grey"
        )
        ax[1].text(i,SOH_max.mean(1)[i]+0.8,round(SOH_max.mean(1)[i],2),color="grey",fontsize=20)
        ax[1].set_yticks(np.arange(0,9))
        ax[1].set_yticklabels(np.arange(0,9),color="grey",fontsize=15)
        ax[1].set_ylabel("Speed [mm/sec",fontsize=20,color="grey")
        ax[1].set_xticks(np.arange(3))
        ax[1].set_xticklabels(["near","mid","far"],fontsize=20,color="grey")
    ax[1].set_title("The max speed of hand COM",fontsize=25,color="grey")
    ax[1].yaxis.grid()


