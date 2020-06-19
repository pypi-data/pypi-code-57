from pathlib import Path
script_location = Path(__file__).absolute().parent
map_loc = script_location / "map2g.txt"


import pickle, pandas as pd


with open(map_loc, 'r', encoding = 'utf-8') as data:
    data = [word for line in data for word in line.split()]


temp = ""
map_2g = {}
k = 0
for i in range(len(data)):
  if data[i] == "=":
    temp = data[i-2] + " " + data [i - 1]
    map_2g [temp] = data[i+1]

def mapping_2g(sentence):
    sentence = sentence.split()
    add = ""
    final_sentence = ""
    it = 0
    ln = len(sentence)
    while it<ln-1:
        add = sentence[it] + " "+ sentence [it + 1]
    
        if add in map_2g.keys():
            final_sentence = final_sentence + " " + map_2g[add] + " " +sentence[it]
        else:
            final_sentence = final_sentence + " " + sentence [it]
        it = it + 1

    final_sentence = final_sentence + " " + sentence[ln - 1]
    return final_sentence.lstrip()


def word_freq(data, keyword):
    freq_factor = 10
    list_freq = []
    for d in data:
        d_split = d.split()
        count = 0
        for s in d_split:
            if s == keyword:
                count+=1
        list_freq.append(count/freq_factor)
    return list_freq

def transform(data, fit_dataframe):
    data = mapping_2g(data)
    print(data)
    target_keys = fit_dataframe.columns
    df = {}
    for tk in target_keys:
        df[tk] = word_freq([data], tk)
    df = pd.DataFrame(df)
    #return df
    df = pd.DataFrame(df.values*fit_dataframe.values, index = fit_dataframe.index)
    #return df
    df = pd.DataFrame(df.sum(axis = 1, skipna = True), columns=["sum"])
    #return df

    get_max = df.loc[df['sum'].idxmax()]

    if(type(get_max) == pd.core.series.Series):
        return get_max.name, data
    else:
        return list(get_max.index, data)
    