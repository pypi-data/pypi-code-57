#!/usr/bin/env python
class utilidades():
    def __init__(self):
        pass
    def count_zero(self, a):
        return len(a.flat) - np.count_nonzero(a)

    def uncompress(self, bytess):
        file_like_object = io.BytesIO(bytess.read())
        zf = zipfile.ZipFile(file_like_object)
        json_file = json.load(zf.open(zf.namelist()[0]))
        return json_file

    def dk(self, d,k=0):
        return list(d.values())[k]

    def pdump(self, var, path):
        with open(path,'wb') as p:
            pickle.dump(var,p)

    def pload(self, path):
        with open(path,'rb') as p:
            var=pickle.load(p)
        return var

    def point2comma(self, s):
        if isinstance(s,Number):
            return s
        if type(s) == str or type(s) == object:
            match = re.match("^\s*-*[0-9]*[\.\,]*[0-9]+\s*",re.sub(",",".",s,count=1))[0]
            if match:
                number = match
                return float(number)

    def display_all(self, df):
        with pd.option_context("display.max_rows", 1000, "display.max_columns", 1000):
            display(df)
            
    def unlist(self, dfiles):
        dfiles2 = {}
        for i in dfiles:
            if len(dfiles[i]) == 1:
                dfiles2[i] = dfiles[i][0]
        return dfiles2

    def logar(self, *args, sep='-', width=30):
        sep_string = sep*width
        print(sep_string)
        print(*args)
        print(sep_string)
        
    def jload(self, json_file):
        with open(json_file,'rt') as j:
            return json.load(j)   
    def jdump(self, json_object, json_destiny):
        with open(json_destiny,'wt') as j:
            json.dump(json_object, j) 
            
    def cplists(self, l1,l2):
        return [i for i in l1 if i not in l2], [i for i in l2 if i not in l1]
