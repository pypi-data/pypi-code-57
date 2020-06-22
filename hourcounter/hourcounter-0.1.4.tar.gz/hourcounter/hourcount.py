import pandas as pd
from tqdm import tqdm

class HourCount:
    print("HourlyCount class is intiated you can use the functoins.")

    

    def hour_count(self,data,column_name):
            
            df = data
            column_name = column_name
            i=0
            j=1
            num = []
            count = []
            for i in tqdm(range(0,24)):
                num.append(i)
            for i in tqdm(range(len(num)-1)):
            
            
           
            
                if i < 9:

                   
                    hour_start = '0'+str(i)+":"+'00'+':'+"00"
                    
                    hour_end = '0'+str(j)+":"+'00'+':'+"00"
                    
                    count.append(len(df[(df[column_name]>=hour_start)&(df[column_name]<=hour_end)]))

                elif i==9:
                        hour_start = '0'+str(i)+":"+'00'+':'+"00"
                        hour_end = str(j)+":"+'00'+':'+"00"
                        
                        count.append(len(df[(df[column_name]>=hour_start)&(df[column_name]<=hour_end)]))


                else:
                    
                    hour_start = str(i)+":"+'00'+':'+"00"
                    
                    hour_end = str(j)+":"+'00'+':'+"00"
                    
                    count.append(len(df[(self.__df[column_name]>=hour_start)&(df[column_name]<=hour_end)]))

                i = j
                j = i+1
                
            hour = []
            for i in tqdm(range(len(count))):
                hour.append(i)
            hour_count = pd.DataFrame()
            hour_count['hour'] = hour
            hour_count['count'] = count
    
            return hour_count