import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)


#replace can be mm and none. mm= mode for categoric features and median for numeric features
#n_r= null ratio , s_r=skewness ratio , c_r=correalation ratio , n_f=number of features ,t_s= test size, n= remove outliers more than,cat_count= remove categoric columns more than cat_count
def main (train,test,target,Id,n_r=0.6,s_r=0.75,c_r=1,n_f="full",t_s=0.25,r_s=42,replace="mm",cat_count=100,n=2):
#-----------------------------------------------------------------------------------------------------------------------------------------------------
    dataset =  pd.concat(objs=[train, test], axis=0,sort=False).reset_index(drop=True)
#-----------------------------------------------------------------------------------------------------------------------------------------------------
    def check_skew(train,target):
        if train[target].skew()>=s_r :
            train[target]= np.log1p(train[target])

#-----------------------------------------------------------------------------------------------------------------------------------------------------
    def drop_na(dataset,target):
        dataset_isna=dataset.isna()
        dataset_isna_sum=dataset_isna.sum()
        dataset_isna_ratio=dataset_isna_sum/len(dataset)
        if target in dataset_isna_ratio:
            dataset_isna_ratio.drop(target,inplace=True)
            remove_columns=dataset_isna_ratio[dataset_isna_ratio>n_r]
        columns=pd.DataFrame(remove_columns)
        print("2-This Columns will be remove because of null ratio higher than %"+str(n_r*100)+": ")
        print(remove_columns)
        return columns
    drops=drop_na(dataset,target)
    dataset=dataset.drop(drops.index,axis=1)
#-----------------------------------------------------------------------------------------------------------------------------------------------------      
    def replace_null(dataset,replace):
        cat=dataset.select_dtypes("object")   
        fl=dataset.select_dtypes(["float64","int64"]).drop(target,axis=1)
        if replace =="mm":
            for column in cat:
                dataset[column].fillna(dataset[column].mode()[0], inplace=True)
            for column in fl:
                dataset[column].fillna(dataset[column].median(), inplace=True)
        if replace=="none":
            for column in cat:
                dataset[column].fillna("NA", inplace=True)
            for column in fl:
                dataset[column].fillna(0, inplace=True)
    
#-----------------------------------------------------------------------------------------------------------------------------------------------------      
    def detect_outliers(dataset,n,features):
        from collections import Counter
        outlier_indices = []
        # iterate over features(columns)
        for col in features:
            # 1st quartile (25%)
            Q1 = np.percentile(dataset[col], 25)
            # 3rd quartile (75%)
            Q3 = np.percentile(dataset[col],75)
            # Interquartile range (IQR)
            IQR = Q3 - Q1
            # outlier step
            outlier_step = 1.5 * IQR 
            # Determine a list of indices of outliers for feature col
            outlier_list_col = dataset[(dataset[col] < Q1 - outlier_step) | (dataset[col] > Q3 + outlier_step )].index
            # append the found outlier indices for col to the list of outlier indices 
            outlier_indices.extend(outlier_list_col)    
        # select observations containing more than 2 outliers
        outlier_indices = Counter(outlier_indices)        
        multiple_outliers = list( k for k, v in outlier_indices.items() if v > n )
        return multiple_outliers 
#-----------------------------------------------------------------------------------------------------------------------------------------------------
    def skew_features(dataset):
        from scipy.special import boxcox1p
        from scipy.stats import boxcox
        from scipy.stats import skew
        lam = 0.15
        #boxcox transform skewed numeric features:
        numeric_feats = dataset.dtypes[dataset.dtypes != "object"].index
        skewed_feats = dataset[numeric_feats].apply(lambda x: skew(x.dropna())) #compute skewness
        skewed_feats = skewed_feats[skewed_feats > s_r]
        skewed_feats = skewed_feats.index
        dataset[skewed_feats] = boxcox1p(dataset[skewed_feats],lam)


        
#------------------------------------------calling functions--------------------------------------------------------------------------------------
    check_skew(dataset,"Survived")
    drop_na(dataset,target)
    replace_null(dataset,replace)
    features=dataset.select_dtypes(["float64","int64"]).drop([target,Id],axis=1)
    detect_outliers(dataset,n,features)
    Outliers_to_drop = detect_outliers(dataset,n,features)
    dataset = dataset.drop(Outliers_to_drop, axis = 0).reset_index(drop=True)
    skew_features(dataset)
    cat=dataset.select_dtypes("object")
    del_col=[]
    for c in cat.columns:
        if len(cat[c].value_counts())>=cat_count:
            del_col.append(c)
    cat=cat.drop(del_col,axis=1)
    dataset=pd.get_dummies(dataset,columns=cat.columns)
#------------------------------------------train test split--------------------------------------------------------------------------------------    
    train=dataset[dataset[target].notnull()]
    test=dataset[dataset[target].isna()]
    
    if n_f=="full":
        k=train.shape[1]
    else:
        k=n_f
    corrmat=abs(dataset.corr())
    cols = corrmat.nlargest(k, target)[target].index
    train_x=train[cols].drop(target,axis=1)
    train_y=train[target]
    X_test=test[cols].drop(target,axis=1)
    
    from sklearn.model_selection import train_test_split
    X_train, X_val, y_train, y_val = train_test_split(train_x, train_y, test_size=t_s, random_state=r_s)
#------------------------------------------all models--------------------------------------------------------------------------------------     
    from sklearn.metrics import confusion_matrix  
    from sklearn.metrics import mean_squared_error,mean_absolute_error
    from sklearn.ensemble import GradientBoostingClassifier,RandomForestClassifier,AdaBoostClassifier,ExtraTreesClassifier
    from lightgbm import LGBMClassifier
    from catboost import CatBoostClassifier
    from xgboost import XGBClassifier
    from sklearn.neural_network import MLPClassifier
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.svm import SVC
    from sklearn.gaussian_process import GaussianProcessClassifier
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.naive_bayes import GaussianNB
    from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
    from sklearn.linear_model import LogisticRegression

    my_models= [ 
               GradientBoostingClassifier(random_state=r_s),
               RandomForestClassifier(random_state=r_s),
               AdaBoostClassifier(random_state=r_s),
               ExtraTreesClassifier(random_state=r_s),
               LGBMClassifier(random_state=r_s), 
               CatBoostClassifier(logging_level='Silent',random_state=r_s), 
               XGBClassifier(random_state=r_s),
               MLPClassifier(random_state=r_s),
               KNeighborsClassifier(),
               SVC(random_state=r_s),
               GaussianProcessClassifier(random_state=r_s),
               DecisionTreeClassifier(random_state=r_s),
               GaussianNB(),
               QuadraticDiscriminantAnalysis(),
               LogisticRegression(random_state=r_s)
               ]
    
    
    scores_val=[]
    scores_train=[]
    MAE=[]
    MSE=[]
    RMSE=[]
    
  
    
    for model in my_models:
        scores_val.append(model.fit(X_train,y_train).score(X_val,y_val))
        scores_train.append(model.fit(X_train,y_train).score(X_train,y_train))
        y_pred=model.predict(X_val)
        MAE.append(mean_absolute_error(y_val,y_pred))
        MSE.append(mean_squared_error(y_val,y_pred))
        RMSE.append(np.sqrt(mean_squared_error(y_val,y_pred)))
        
    results=zip(scores_val,scores_train,MAE,MSE,RMSE)
    results=list(results)
    results_score_val=[item[0] for item in results]
    results_score_train=[item[1] for item in results]
    results_MAE=[item[2] for item in results]
    results_MSE=[item[3] for item in results]
    results_RMSE=[item[4] for item in results]
    df_results=pd.DataFrame({"Algorithm":my_models,"Training Score":results_score_train,"Validation Score":results_score_val,"MAE":results_MAE,"MSE":results_MSE,"RMSE":results_RMSE})
    best_models=df_results.sort_values(by="Validation Score",ascending=False)
    best_model=best_models.iloc[0]
    print(best_model)
    best_model_name=best_models.iloc[0][0]
    print(best_model_name)
    best_model_learn=best_model_name.fit(X_train,y_train)
    y_pred_best=best_model_learn.predict(X_val)
    cm=confusion_matrix(y_val,y_pred_best.round())
    print("Confussion Matrix: ")
    print(cm)





















