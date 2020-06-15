import numpy as np
import functools

#def getInterval_by_keymarker(func):
#    @functools.wraps(func)
#    def wrapper(*args, **kwargs):
#        key1, threshold1 = func(*args, **kwargs)
#        key1 = np.diff(np.where(key1 < threshold1, 1, 0))
#        key1_index = np.where(key1 == 1)[0]
#        sp, ep = key1_index[1:11], key1_index[2:12]
#        return sp, ep
#    return wrapper

def getInterval_by_keymarker(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key1, threshold1 = func(*args, **kwargs)
        a = np.diff(np.where(key1 > threshold1, 1, 0))
        hoge = np.where(a == -1)[0]
        if args[1] == 100:
            del_index = np.where(np.diff(hoge) < 31)[0] + 1
        else:
            del_index = np.where(np.diff(hoge) < 310)[0] + 1
        key1_index = np.delete(hoge,list(del_index))
        sp, ep = key1_index[1:11], key1_index[2:12]
        return sp, ep
    return wrapper

#def get_p2_point(func):
#    @functools.wraps(func)
#    def wrapper(*args, **kwargs):
#        key1, threshold1, sp, ep = func(*args, **kwargs)
#        key1 = [key1[start:end] for start, end in zip(sp, ep)]
#        key1_release = []
#        for i in key1:
#            i = np.diff(np.where(i < threshold1, 1, 0))
#            key1_release.append(np.where(i == -1)[0][0])
#        return np.array(key1_release)
#    return wrapper

def get_p2_point(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        com,sp,ep,p4 = func(*args, **kwargs)
        com = [com[start:end,2] for start, end in zip(sp, ep)]
        com_max = [i[:j].argmax() for i,j in zip(com,p4)]
        return np.array(com_max)
    return wrapper

def get_p4_point(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key2, threshold2, sp, ep = func(*args, **kwargs)
        key2 = [key2[start:end] for start, end in zip(sp,ep)]
        key2_start = []
        for i in key2:
            i = np.diff(np.where(i < threshold2, 1, 0))
            key2_start.append(np.where(i == 1)[0][0])
        return np.array(key2_start)
    return wrapper

#def get_p4_point(func):
#    @functools.wraps(func)
#    def wrapper(*args, **kwargs):
#        key2, threshold2 = func(*args, **kwargs)
#        a = np.diff(np.where(key2 > threshold2, 1, 0))
#        hoge = np.where(a == -1)[0]
#        del_index = np.where(np.diff(hoge) < 31)[0] + 1
#        key2_index = np.delete(hoge,list(del_index))
#        return np.array(key2_index[1:11])
#    return wrapper

def get_p5_point(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key2, threshold2, sp, ep = func(*args, **kwargs)
        key2 = [key2[start:end] for start, end in zip(sp,ep)]
        key2_bottom = []
        for i in key2:
            key2_bottom.append(i.argmin())
        return np.array(key2_bottom)
    return wrapper


def get_p6_point(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key2, threshold2, sp, ep = func(*args, **kwargs)
        key2 = [key2[start:end] for start, end in zip(sp,ep)]
        key2_end = []
        for i in key2:
            i = np.diff(np.where(i < threshold2, 1, 0))
            key2_end.append(np.where(i == -1)[0][0])
        return np.array(key2_end)
    return wrapper

#def get_p6_point(func):
#    @functools.wraps(func)
#    def wrapper(*args, **kwargs):
#        key2, threshold2 = func(*args, **kwargs)
#        a = np.diff(np.where(key2 > threshold2, 1, 0))
#        hoge = np.where(a == 1)[0]
#        del_index = np.where(np.diff(hoge) < 30)[0] + 1
#        key2_index = np.delete(hoge,list(del_index))
#        return np.array(key2_index[1:11])
#    return wrapper

def get_p3_point(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        marker, sp, ep, p4 = func(*args, **kwargs)
        marker = [marker[start:end] for start, end in zip(sp,ep)]
        p3_index = []
        for num, i in enumerate(marker):
            p3_index.append(i[:p4[num]].argmax())
        return np.array(p3_index)
    return wrapper

def get_p1_point(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key1, sp, ep = func(*args, **kwargs)
        key1 = [key1[start:end] for start, end in zip(sp,ep)]
        key1_index = [i.argmin() for i in key1]
        return np.array(key1_index)
    return wrapper



def getAnalysis_Interval_by_keymarker(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key1, key2, threshold1, threshold2 = func(*args, **kwargs)
        sps, eps = np.where(key1[:,2] > threshold1, 0, 1), np.where(key2[:,2] > threshold2, 0, 1)
        key1_stroke, key3_stroke = np.where(np.diff(sps) == 1)[0], np.where(np.diff(eps) == 1)[0]
        key1_release, key3_release = np.where(np.diff(sps) == -1)[0], np.where(np.diff(eps) == -1)[0]

        key1_release = np.array(key1_stroke)[1:11]
        key1_stroke = np.array(key3_release)[1:11]
        #key1_stroke = np.array(key1_stroke)[1:11]
        #key1_release = np.array(key1_release)[:10]

        analysis_section_start, analysis_section_end = [], []
        for i in range(10):
            analysis_section_start.append(key3_stroke[i+1] - key1_release[i])
            analysis_section_end.append(key3_release[i+1] - key1_release[i])
        analysis_section_start = np.array(analysis_section_start)
        analysis_section_end = np.array(analysis_section_end)

        if args[1] == 100:
            return analysis_section_start, analysis_section_end
        elif args[1] == 1000:
            return analysis_section_start*10, analysis_section_end*10
    return wrapper


def normalized_stroke_section(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        sp, ep, asp, esp = func(*args, **kwargs)
        length_trial = ep - sp
        normed_asp = (asp*100 / length_trial).astype("int")
        normed_esp = (esp*100 / length_trial).astype("int")
        if args[1] == 100:
            return normed_asp, normed_esp
        elif args[1] == 1000:
            return (normed_asp*10).astype("int"), (normed_esp*10).astype("int")
    return wrapper