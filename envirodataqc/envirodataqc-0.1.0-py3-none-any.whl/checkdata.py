'''
Functions for checking data:

Function input should generally be a dataframe with the following columns
index - datetime
data - database values for measurement with title of measurement.
flags - column, initially all zeros for flags

Functions should be called in the following order: gapcheck, checkvals, checkbehavior

Flags
- 0: Good
- 1: Suspicious
- 2: Bad
'''

import pandas as pd
import numpy as np
#from scipy import stats

#------------ General data check algorithms -----------#

#Assess data for gaps
def gapcheck(data):
    '''
    #A function to assess the datetimeindex of data
    Input should be a pandas df with columns: <data name>, flags
    Output: Various gap statistics
        - freq - Most frequent gap (likely sampling frequency)
        - hists - List of gap frequencies [30 - 45m, 45 - 1hr, 1 - 2hr, > 2hr]
        - tot - Total of gaps > 1 hr
    '''
    #Remove bad data values from analysis
    data = data[data['flags'] != 2].copy()

    #Calculate gaps between points in minutes
    timediff = np.diff(data.index)
    timediff = timediff.astype(float)/(60*(10**9)) #60 x 10^9 to convert from nanosec

    #Run statistics on gaps
    #Find the most frequent gap
    freq = stats.mode(timediff)[0][0]  #Outputs array. Want first val

    #Count binned gaps - index at the end forces just use of first returned value.
    hists = stats.binned_statistic(timediff,timediff,'count',bins=[40,45,60,120,1000])[0]

    #Find total of gaps over 1hr
    tot = round(timediff[timediff > 60].sum()/60,1)

    return freq, tot, hists

#Data range checks
def checkvals(data):
    '''
    A function for assessing how reasonable
    a given measured value is.
    Types: air_temp, humidity, air_pressure, 
           wind_speed, gust, rain rate, solar radiation (incoming)
    Input should be a pandas df with columns: <data name>, flags
    '''
    #Copy data to avoid warning
    data = data.copy()
    
    #Define reasonable ranges of values
    temprange = [-40,50] #C
    rhrange = [3,103]
    bprange = [700,1050] #mb
    windsp = [0,40] #m/s
    windgust = [0,60]
    rainrt = [0,24] #in/hr
    swrange = [0,1500] #Incoming solar in W/m2
    rangevals = {'air_temp':temprange,'humidity':rhrange,'air_pressure':bprange,
                 'wind_speed':windsp,'wind_gust':windgust,'rain_rate':rainrt,
                 'solarrad_sw':swrange}

    #Define suspicious ranges
    rainsusp = [6,24] #in/hr
    swsusp = [1362,1500] #W/m2
    suspvals = {'rain_rate':rainsusp,'solarrad_sw':swsusp}

    #Determine type
    mtype = data.columns[0] #Should be the column title of data values

    #Flag out of range values as '2' (bad)
    minval = rangevals[mtype][0]
    maxval = rangevals[mtype][1]
    data.loc[(data[mtype]<minval) | (data[mtype]>maxval),'flags'] = 2

    #Flag certain measurement ranges as suspicious
    if mtype in suspvals.keys():
        minval = suspvals[mtype][0]
        maxval = suspvals[mtype][1]
        data.loc[(data[mtype]>=minval) & (data[mtype]<=maxval),'flags'] = 1


    return data

#Evaluate behavior
def checkbehavior(data):
    '''
    A function for evaluating the behavior of 
    a measurement: flatlining, jumps
    *Only works for air_temp, humidity, air_pressure, wind_speed (not gust),
        SW solar radiation.
    '''
    #Copy data to avoid warning
    data = data.copy()
    
    #Define maximum plausible jumps
    airjump = 1.4 #C/min
    rhjump = 4.4 #%pts/min
    bpjump = 1 #mb/min
    wsjump = 6 #m/s per min
    swjump = 160 #W/m^2 per min
    maxjump = {'air_temp':airjump,'humidity':rhjump,'air_pressure':bpjump,
               'wind_speed':wsjump,'solarrad_sw':swjump}

    #Define maximum plausible flatlining (minutes)
    airflat = 15 
    rhflat = 15
    bpflat = 45
    wsflat = 60
    swflat = 840
    maxflat = {'air_temp':airflat,'humidity':rhflat,'air_pressure':bpflat,
               'wind_speed':wsflat,'solarrad_sw':swflat}

    #Extract measurement type
    mtype = data.columns[0] #Should be the column title of data values
    
    #Extract bad points from dataset
    bdpts = data[data.flags == 2]
    data = data[data.flags != 2]

    #Calculate absolute slope between input data points
    vdiff = np.absolute(np.diff(data[mtype].values))
    #Calculate time differences in minutes
    timediff = np.diff(data.index)
    timediff = timediff.astype(float)/(60*(10**9)) #60 x 10^9 to convert from nanosec
    dataslopes = vdiff/timediff

    #Flag points based on jumps. Also identify flatlined sections
    oldslopeflat = False #Keeps track of start of flatlined data
    sindex = 0
    counter = 0 #Keep track of index
    for slope in dataslopes:
        
        if (slope!=0) and (oldslopeflat):
            #Signifies the end of a section of flat data
            eindex = counter
            #Check amount of time flat
            flattime = (data.index[eindex] - data.index[sindex]).seconds/60 #Time in minutes
            #If exceeds maximum time flag all points
            if flattime > maxflat[mtype]:
                data.iloc[sindex:eindex+1,1]=1
            oldslopeflat = False

        if (slope==0) and (not oldslopeflat):
            #Signifies the start of a flat section
            sindex = counter
            oldslopeflat = True
        
        #Slope exceeds limits
        if abs(slope) > maxjump[mtype]:
            #Flag points adjacent as suspicious
            data.iloc[counter,1] = 1
            data.iloc[counter+1,1] = 1

        counter = counter+1

    #Put bad points back in dataset
    if not bdpts.empty:
        data = data.append(bdpts)
        data.sort_index(inplace=True)

    return data

#------------ Wind specific algorithms -----------------#
def windspchk(datasp):
    '''
    Evaluate speeds for internal consistency
    - Calculate daily average and maximum wind speed
    - Assesses ratio of max/ave winds
    Input - Dataframe of wind speed values, flags
    '''
    #Output dataframe
    daydata = pd.DataFrame()
    
    #Resample to daily values and calculate
    daydata['avgwinds'] = datasp.resample('1D').apply(dataAvg) #Returns a series
    daydata['maxwinds'] = datasp.wind_speed.resample('1D').max()

    #Ratio
    daydata['max_avg'] = daydata.avgwinds/daydata.maxwinds

    #Flag data where avg/max ratio < 0.1
    daydata.dropna(inplace=True) #Drop any nans associated with endpoints
    counter = 0
    for day in daydata.index:
        if daydata.max_avg[counter]<0.1:
            #Flag all point associated with a given day
            datasp.loc[day.to_pydatetime():,'flags']=1 #Colon needed for datetime...see help
        counter = counter+1

    return datasp, daydata

def winddirchk(datasp,datadir):
    '''
    Evaluate direction data
    Assess flatlining in context of windspeed.
    Flatlining associated with wind > 0 is suspicious.
    '''
    #Set bad speed values to np.nan
    datasp[datasp['flags'] == 2] = np.nan
    
    #Extract flags to avoid data warning
    myflags = datadir.flags.values

    #Calculate slope between input data points
    #Ignore time, every point should be different when wind > 0
    slopes = np.diff(datadir.wind_direction.values)

    #Assess slopes and flag
    counter = 1 #Keep track of index
    for slope in slopes:
        if slope == 0:
            index1 = counter - 1
            index2 = counter
            speed1 = datasp.wind_speed[index1]
            speed2 = datasp.wind_speed[index2]
            spflag1 = datasp.flags[index1]
            spflag2 = datasp.flags[index2]
            #Flag points associated with 0 slope if speed != 0
            if (speed1!=0)and(speed2!=0):
                myflags[index1] = 1
                myflags[index2] = 1
            #Flag points associated with 0 slope if speed is suspect
            if(spflag1==1)and(spflag2==1):
                myflags[index1] = 1
                myflags[index2] = 1
        counter = counter + 1

    #Set flags again
    datadir.flags = myflags

    return datadir

#------------ Data averaging function ------------------#
def dataAvg(data):
    '''
    Outputs average
    - Uses trapezoidal numerical integration
    - Input pandas df <index>, <measurement>, flags
    '''
    #Remove bad values from dataset
    data = data[data['flags'] != 2]

    #Exit if no data
    if len(data)<2:
        return np.nan
    
    #Isolate measurement column
    mvar = data.columns[0]

    #Find total number of minutes in dataset
    totmin = ((data.index[-1] - data.index[0]).total_seconds())/60

    #Trapezoidal integration - index is in nanoseconds, so need to convert to seconds
    dAvg = np.trapz(data[mvar].values,(data.index.astype(np.int64)/10**9)/60)

    #Divide integral by timeframe
    dAvg = dAvg/totmin

    return dAvg





#-------------- Testing ----------------#
if __name__ == "__main__":
    #Load some test data
    csvfile = '../data/quiktest.csv'
    csvdata = pd.read_csv(csvfile,index_col=0,parse_dates=True)

    #Extract data
    Tdata = csvdata.copy()
    Tdata['flags'] = 0

    #Run data checks
    Tdata = checkvals(Tdata)