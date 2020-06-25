import ctypes

# my_dll = ctypes.cdll.LoadLibrary("Example.dll")
#
# # The following "restype" method specification is needed to make
# # Python understand what type is returned by the function.
# my_dll.AddNumbers.restype = ctypes.c_double
#
# p = my_dll.AddNumbers(ctypes.c_double(1.0), ctypes.c_double(2.0))
#

dll_filename = r'd:\OSGeo4W64-20200614\bin\talosdll.dll'
my_dll = ctypes.cdll.LoadLibrary(dll_filename)

# The following "restype" method specification is needed to make
# Python understand what type is returned by the function.
# my_dll.AddNumbers.restype = ctypes.c_double

p = my_dll.GS_ReturnInt()




print("The result was:", p)


