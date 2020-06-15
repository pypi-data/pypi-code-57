import os
import setuptools
import sys
import platform, shutil
from setuptools import find_packages, setup, Extension
from setuptools.command.build_ext import build_ext as build_ext_orig
from setuptools.command.install_lib import install_lib as install_lib_orig
from subprocess import check_output
from shutil import copyfile
from distutils.sysconfig import get_python_lib;
#https://stackoverflow.com/questions/42585210/extending-setuptools-extension-to-use-cmake-in-setup-py
class CMakeExtension(Extension):
    def __init__(self, name, sources=[]):
        Extension.__init__(self,name = name, sources = sources)

def get_hepmc3_version():
  line = '#define HEPMC3_VERSION_CODE 3002000'
  current=os.getcwd()
  with open(current+'/include/HepMC3/Version.h') as f:
    line = next((l for l in f if 'HEPMC3_VERSION_CODE' in l and '#define ' in l), None)
  number=int(line.split(' ')[2]) 
  return str(int(number/1000000))+'.'+str(int((number%1000000)/1000))+'.'+str((number%1000))

def get_library_location():
 ps=platform.system()
 bits=platform.architecture()[0]
 if  ps == 'Solaris':
  return "lib"
 if  ps == 'FreeBSD':
  return "lib"
 if  ps == 'Linux':
  if bits=='64bit':
   return "lib64"
  if bits=='32bit':
   return "lib"
 if  ps == 'Darwin':
  return "lib"
 if  ps == 'Windows':
  return "lib"
 return "lib"
 
def get_hepmc3_libraries():
 lib=get_library_location()
 ps=platform.system()
 if  ps == 'Darwin':
  return [( lib, ['outputs/'+lib+'/libHepMC3.dylib',  'outputs/'+lib+'/libHepMC3search.dylib','outputs/'+lib+'/libHepMC3-static.a','outputs/'+lib+'/libHepMC3search-static.a'])]
 if  ps == 'Windows':
  return [( lib, ['outputs/lib/HepMC3.dll', 'outputs/'+lib+'/HepMC3search.dll', 'outputs/'+lib+'/HepMC3search-static.lib', 'outputs/'+lib+'/HepMC3-static.lib'])]
 return [( lib, ['outputs/'+lib+'/libHepMC3.so', 'outputs/'+lib+'/libHepMC3.so.3','outputs/'+lib+'/libHepMC3search.so','outputs/'+lib+'/libHepMC3search.so.4'])]

class  hm3_install_lib(install_lib_orig):
      def run(self):
        cwd=os.path.abspath(os.getcwd())
        v=sys.version_info
        versionstring=str(v[0])+"."+str(v[1])+"."+str(v[2])
        shutil.copytree(os.path.join(cwd,"python",versionstring,"pyHepMC3"),os.path.join(cwd,self.build_dir,"pyHepMC3"))
        print(install_lib_orig.get_outputs(self)) 
        print(self.install_dir) 
        print(self.build_dir) 
        install_lib_orig.run(self)

class hm3_build_ext(build_ext_orig):
    def get_ctest_exe(self):
      return "ctest"
    def get_cmake_exe(self):
        vg='0'
        cmakeg_exe=""
        outg = check_output(["cmake", "--version"])
        outgsplit=outg.split()
        if len(outgsplit)>2: 
           vg=outgsplit[2]
           if int(vg[0])>=3: 
            cmakeg_exe="cmake"
        if (cmakeg_exe!=""): return cmakeg_exe

        v3='0'
        cmake3_exe=""
        out3 = check_output(["cmake3", "--version"])
        out3split=out3.split()
        if len(out3split)>2:
         v3=out3split[2]
         if int(v3[0])==3: 
           cmake3_exe="cmake3"
        if (cmake3_exe!=""): return cmake3_exe
        return "foo "
    def get_cmake_python_flags(self):
        pv=sys.version_info
        return '-DHEPMC3_PYTHON_VERSIONS='+str(pv[0])+'.'+str(pv[1])

        
    def run(self):
        for ext in self.extensions:
            self.build_cmake(ext)
#        build_ext_orig.run(self)

    def build_cmake(self, ext):
        build_temp=os.getcwd()
        cwd=os.path.abspath(os.getcwd())
        cmake_exe=self.get_cmake_exe()
        ctest_exe=self.get_ctest_exe()
        cmake_args = [
         'CMakeLists.txt',
         '-DHEPMC3_BUILD_EXAMPLES:BOOL=OFF',
         '-DHEPMC3_INSTALL_INTERFACES:BOOL=OFF',
         '-DHEPMC3_ENABLE_SEARCH:BOOL=ON',
         '-DHEPMC3_BUILD_DOCS:BOOL=OFF',
         '-DHEPMC3_ENABLE_PYTHON:BOOL=ON',
         '-DHEPMC3_ENABLE_ROOTIO:BOOL=OFF',
         '-DCMAKE_BUILD_TYPE=Release', 
         '-DHEPMC3_ENABLE_TEST:BOOL=ON',
         self.get_cmake_python_flags()]
        ps=platform.system()
        bits=platform.architecture()[0]
        if  ps == 'Linux':
          if bits=='64bit':
            cmake_args.append ('-DLIB_SUFFIX=64')
            cmake_args.append ('-DCMAKE_INSTALL_LIBDIR=lib64')
        if ps == 'Windows':
          #FIXME: detect arch
          cmake_args.append ('-Thost=x64')
          cmake_args.append ('-A')
          cmake_args.append ('x64')
        self.spawn([cmake_exe, str(cwd)] + cmake_args)

        if not self.dry_run:
            build_args = [  ]
            self.spawn([cmake_exe, '--build', '.'] + build_args)
            ctest_args = []
            v=sys.version_info
            if  ps == 'Windows':
             ctest_args.append('-C')
             ctest_args.append('Debug')
            #Travis Windows bug?
            if ps != 'Darwin' and  not ( ps == 'Windows' and v[0]==3 and v[1] == 8 ):
             self.spawn([ctest_exe,  '.','--output-on-failure']+ctest_args)
        os.chdir(str(cwd))
def local_find_packages():
  os.mkdir('pyHepMC3')
  return ['pyHepMC3']


setuptools.setup(
     name='HepMC3',  
     version=get_hepmc3_version(),
     author="HepMC3 Developers",
     author_email="hepmc-dev@cern.ch",
     description="HepMC3 library and Python bindings for HepMC3",
     long_description="Official python bindings for the HepMC3 library. Please visit https://hepmc.web.cern.ch/hepmc/ and  https://gitlab.cern.ch/hepmc/HepMC3 for more documentation",
     long_description_content_type="text/markdown",
     url="https://gitlab.cern.ch/hepmc/HepMC3",
     license = "GPLv3",
     platforms=['any'],
     include_package_data = True,
     packages=local_find_packages(),
     data_files=get_hepmc3_libraries()+[
     ('bin',                ['outputs/bin/HepMC3-config']),       
     ('share/HepMC3/cmake', [
     'outputs/share/HepMC3/cmake/HepMC3Config-version.cmake',
     'outputs/share/HepMC3/cmake/HepMC3Config.cmake']),       
     ('include/HepMC3',[
     'include/HepMC3/ReaderPlugin.h','include/HepMC3/WriterPlugin.h',
     'include/HepMC3/WriterAsciiHepMC2.h','include/HepMC3/WriterHEPEVT.h','include/HepMC3/Units.h',
     'include/HepMC3/HEPEVT_Wrapper.h','include/HepMC3/GenCrossSection.h','include/HepMC3/GenRunInfo.h',
     'include/HepMC3/WriterAscii.h','include/HepMC3/Setup.h',
     'include/HepMC3/GenVertex.h','include/HepMC3/FourVector.h','include/HepMC3/PrintStreams.h',
     'include/HepMC3/GenEvent.h','include/HepMC3/ReaderHEPEVT.h','include/HepMC3/Print.h',
     'include/HepMC3/LHEF.h','include/HepMC3/GenParticle_fwd.h',
     'include/HepMC3/Reader.h','include/HepMC3/GenPdfInfo_fwd.h','include/HepMC3/GenParticle.h',
     'include/HepMC3/GenCrossSection_fwd.h','include/HepMC3/LHEFAttributes.h',
     'include/HepMC3/AssociatedParticle.h','include/HepMC3/ReaderLHEF.h','include/HepMC3/GenPdfInfo.h',
     'include/HepMC3/HepMC3.h','include/HepMC3/Errors.h',
     'include/HepMC3/GenHeavyIon.h','include/HepMC3/Writer.h','include/HepMC3/ReaderFactory.h',
     'include/HepMC3/ReaderAsciiHepMC2.h',
     'include/HepMC3/Version.h','include/HepMC3/Attribute.h','include/HepMC3/GenHeavyIon_fwd.h',
     'include/HepMC3/ReaderAscii.h',
     'include/HepMC3/GenVertex_fwd.h','search/include/HepMC3/Filter.h',
     'search/include/HepMC3/Relatives.h', 'search/include/HepMC3/AttributeFeature.h',
     'search/include/HepMC3/FilterAttribute.h', 'search/include/HepMC3/Feature.h',
     'search/include/HepMC3/Selector.h'
      ]),
     ('include/HepMC3/Data',[
     'include/HepMC3/Data/GenEventData.h',
     'include/HepMC3/Data/GenParticleData.h',
     'include/HepMC3/Data/GenVertexData.h',
     'include/HepMC3/Data/GenRunInfoData.h'])
                  ],
     classifiers=[
         "Programming Language :: Python ",
         "Operating System :: OS Independent",
     ],
     ext_modules=[CMakeExtension('pyHepMC3')],
      cmdclass={
        'build_ext': hm3_build_ext,  'install_lib': hm3_install_lib
    }
 )
