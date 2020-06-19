import pickle
import scipy.stats as st
import pandas as pd
import numpy as np
def cvdage_inner(X_test):
  fea = ["Body mass index","Mean platelet volume","Coefficient of variation of red blood cell distribution width","Composite inflammatory index",
            "Serum glucose","Hemoglobin A1c","High density lipoprotein","Low density lipoprotein",
            "Total cholesterol","Triglyceride","Serum uric acid",
            "Estimated glomerular filtration rate","Total bilirubin",
            "Heart rate","Pulse wave velocity","Ankle-brachial pressure index","Systolic blood pressure",
            "Diastolic blood pressure","Drinking","Smoking","Urine protein","Lipid-lowering drug","Antihypertensive drug","Antidiabetic drug"]
  train = X_test.loc[:,fea]
  agev = pd.read_table('https://raw.githubusercontent.com/VVictorChen/CVHealthEva/master/data/AGEV.csv',sep=',',encoding='gbk')  
  n1 = train
  for i in n1.columns.values.tolist():
    site = n1.columns.get_loc(i)
    obs = (n1.iloc[:,site] - agev.q[site])*(agev.k[site]/(agev.s[site]**2))
    n1.iloc[:,site]  =  obs
  ba_obs = 24
  ba_en = n1.apply(lambda x: x.sum(),axis=1)
  ba_ed = 0.01164164
  ba_eo = ba_en/ba_ed
  ba_e = ba_eo
  s_ba2 = 145.612
  ba_en = np.array(ba_en)
  C_age = np.array(X_test.Age)
  bioage = (ba_en + (C_age/s_ba2)) / (ba_ed + (1/s_ba2))
  return(bioage)


def qtrans(y):
  y = pd.Series(y.reshape((-1,)))
  y_rank = y.rank(method='first')
  y_rank = y_rank.astype('int64') - 1
  value = np.arange(1,(len(y)+1))  -0.5
  value = value / len(y)
  z = st.norm.ppf(value)
  z = z[y_rank]
  return z
def relative_risk_inner(x,traindata):
  y = np.append(traindata,x)
  z = qtrans(y)
  z = z[-1]
  result = st.norm.cdf(z)#........
  return(result)    
def RRScore(df,Traindata,mean=56.086,sd=12.063):
  Result=[]
  for a in range(df.shape[0]):
    x = df.y_pred[a]
    value = df.Age[a]
    value = value*sd+mean
    value = float(value)
    if(value<50):
      traindata=Traindata.y_pred[Traindata.Age<50]
    if(value<60 and value>=50):
      traindata=Traindata.y_pred[(Traindata.Age<60) & (Traindata.Age>=50)]
    if(value<70 and value>=60):
      traindata=Traindata.y_pred[(Traindata.Age<70) & (Traindata.Age>=60)]
    if(value<80 and value>=70):
      traindata=Traindata.y_pred[(Traindata.Age<80) & (Traindata.Age>=70)]
    if(value>=80):
      traindata=Traindata.y_pred[Traindata.Age>=80]
    Result.append(relative_risk_inner(x,traindata))
  return(Result)
