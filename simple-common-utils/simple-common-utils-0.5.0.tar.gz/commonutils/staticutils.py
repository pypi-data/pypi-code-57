from collections.abc import Iterable
from copy import deepcopy
from decimal import Decimal, ROUND_HALF_UP
from functools import cmp_to_key
from math import floor, log10
from platform import system
from re import split
from sys import float_info

class StaticUtils:
   __SYSTEM = system()
   
   @staticmethod
   def findKeyInDictionary(dictionary, key):
      result = []
      keyChain = []
      
      def find(d):
         for k, v in d.items():
            if k == key:
               result.append(tuple(keyChain.copy()))
            
            if isinstance(v, dict):
               keyChain.append(k)
               find(v)
               keyChain.pop()
            
            elif isinstance(v, list):
               for index, element in enumerate(v):
                  if isinstance(element, dict):
                     keyChain.append(index)
                     find(element)
                     keyChain.pop()
      
      find(dictionary)
      
      return tuple(result)
   
   @staticmethod
   def getIntersection(line1, line2):
      a1 = (line1[0][1] - line1[1][1]) / (line1[0][0] - line1[1][0])
      b1 = line1[0][1] - (a1 * line1[0][0])

      a2 = (line2[0][1] - line2[1][1]) / (line2[0][0] - line2[1][0])
      b2 = line2[0][1] - (a2 * line2[0][0])
      
      if abs(a1 - a2) < float_info.epsilon:
         raise ValueError()
      
      x = (b2 - b1) / (a1 - a2)
      y = a1 * x + b1
      
      return StaticUtils.round((x, y))
   
   @staticmethod
   def getOrSetIfAbsent(obj, key, default):
      return StaticUtils.setIfAbsentAndGet(obj, key, default)
   
   @staticmethod
   def getPlaces(value):
      return [StaticUtils.getPlaces(number) for number in value] if StaticUtils.isIterable(value) else 0 if not value else floor(log10(abs(value))) + 1
   
   @staticmethod
   def indexDictionary(dictionary, keys):
      d = dictionary
      
      for key in keys:
         d = d[key]
      
      return d
   
   @staticmethod
   def isLinux():
      return StaticUtils.__SYSTEM == "Linux"
   
   @staticmethod
   def isIterable(obj, ignore = (str,)):
      return not isinstance(obj, ignore) and isinstance(obj, Iterable)
   
   @staticmethod
   def isWindows():
      return StaticUtils.__SYSTEM == "Windows"
   
   @staticmethod
   def mergeJson(a, b, overwrite = False):
      c = deepcopy(a)
      
      for key, value in b.items():
         splitKey = split("[\[\]]", key)
         l = len(splitKey)
         
         if l == 1:
            if (key not in c) or overwrite:
               c[key] = value
            
            else:
               invalidType = type(c[key]) if not isinstance(c[key], dict) else type(value) if not isinstance(value, dict) else None
               
               if invalidType:
                  raise ValueError(f"'{key}' exists in both JSONs but is a '{invalidType}' in one of them")
               
               c[key] = mergeJson(c[key], b[key])
         
         elif l == 3 and not len(splitKey[2]):
            c[splitKey[0]][int(splitKey[1])] = value
         
         else:
            raise ValueError(f"Something terrible happened: {key}, {splitKey}")
      
      return c
   
   @staticmethod
   def round(value):
      result = None
      
      if StaticUtils.isIterable(value):
         result = [StaticUtils.round(val) for val in value]
         
         if isinstance(value, tuple):
            result = tuple(result)
      
      else:
         if value.__class__.__module__ == "numpy":
            value = value.item()
         
         result = int(Decimal(value).to_integral_value(ROUND_HALF_UP))
      
      return result
   
   @staticmethod
   def setSafely(obj, index, value):
      try:
         obj[index] = value
      
      except IndexError:
         obj.extend([None] * (index - len(obj)))
         obj.append(value)
   
   @staticmethod
   def setIfAbsentAndGet(obj, key, default):
      result = default
      
      try:
         result = obj[key]
      
      except KeyError:
         obj[key] = default
      
      except IndexError:
         StaticUtils.setSafely(obj, key, default)
      
      return result
   
   @staticmethod
   def sortStringsAsIntegers(iterable, separator = "."):
      def makeIntTuple(s):
         s = s.split(separator)
         
         if not s[-1]:
            s[-1] = '0'
         
         return tuple(map(int, s))
      
      return tuple(map(lambda t: separator.join(map(str, t)), sorted(map(makeIntTuple, iterable), key = cmp_to_key(lambda t1, t2: -1 if t1 < t2 else 1 if t1 > t2 else 0))))
