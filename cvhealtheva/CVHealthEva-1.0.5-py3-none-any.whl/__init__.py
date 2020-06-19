from .kernels import *
from urllib.request import urlopen
def preprocess(X_test):
  mean_sd = mean_sd = pd.read_table('https://raw.githubusercontent.com/VVictorChen/CVHealthEva/master/data/MEAN_SD.csv',sep=',',encoding='utf_8_sig')
  fea1 =mean_sd.feature.tolist()
  fea2 = X_test.columns.values.tolist()
  fea = [val for val in fea2 if val in fea1]
  X_test = X_test.loc[:,fea]
  newdata = X_test
  for i in X_test.columns.values.tolist():
    m = mean_sd.Mean[mean_sd.feature==i]
    s = mean_sd.SD[mean_sd.feature==i]
    v = np.array(X_test.loc[:,i])
    m = float(m)
    s = float(s)  
    newdata.loc[:,i]  =  (v - m) / s
  return(newdata)

def cvdage(X_test):
    return(cvdage_inner(X_test))

def main_cvdscore(X_test):
  loaded_model = pickle.load(urlopen("https://github.com/VVictorChen/CVHealthEva/blob/master/data/XGB.pickle.dat?raw=true"))
  Traindata = pd.read_table('https://raw.githubusercontent.com/VVictorChen/CVHealthEva/master/data/traindata_age.csv',sep=',',encoding='utf_8_sig')
  scores = loaded_model.predict_proba(X_test)
  df = pd.DataFrame({'y_pred': scores[:,1],'Age':X_test.Age})
  RRS = RRScore(df,Traindata)
  df = pd.DataFrame({'ARS': scores[:,1],'RRS':RRS})
  return(df)
