
from subprocess import call, TimeoutExpired, Popen
import urllib.request
import os
from os.path import dirname
import glob
import shutil
import argparse

from concurrent.futures import ThreadPoolExecutor

from pathlib import Path

def install(path, url, package_path):
    #package_path = os.path.dirname(os.path.realpath(__file__))
    full_path = package_path + "/" + path
    if os.path.exists(full_path):
        return
    os.mkdir(full_path)
    try:
        name, hdrs = urllib.request.urlretrieve(url)
    except IOError as e:
        print("Can't retrieve %s: %s" % (url, e))
        return
    call(["unzip", name, "-d", full_path])

def install_jd_cli(package_path):
    install("tools/jd-cli",
            "https://github.com/kwart/jd-cmd/releases/download/jd-cmd-1.0.1.Final/jd-cli-1.0.1.Final-dist.zip",
            package_path)

def install_dex_tools(package_path):
    install("tools/dex-tools",
            "https://github.com/pxb1988/dex2jar/files/1867564/dex-tools-2.1-SNAPSHOT.zip",
            package_path)

def setup(package_path):
    #package_path = os.path.dirname(os.path.realpath(__file__))
    if not os.path.exists(package_path + "/tools"):
        os.mkdir(package_path + "/tools")
    install_dex_tools(package_path)
    install_jd_cli(package_path)

def jar2java(jar, dir):
    package_path = os.path.dirname(os.path.realpath(__file__))
    call(["unzip", jar, "-d", "%s/jar" % (os.path.dirname(jar))])
    path_jar = '%s/jar' %  (os.path.dirname(jar))
    
    executor = ThreadPoolExecutor(max_workers=8)
    
    owd = os.getcwd()
    os.chdir(path_jar)
    for path in Path('.').rglob('*.class'):
        if "$" in path.name:
            continue
        filename = "../../src/" + str(path.with_suffix('.java'))
        #print(filename)
        Path(os.path.dirname(filename)).mkdir(parents=True, exist_ok=True)
        executor.submit(Class2Java, filename, package_path, path)
    executor.shutdown(wait=True)
    os.chdir(owd)
    return 0

def Class2Java(filename, package_path, path):
    file = open(filename, "w")
    print(filename)
    try:
        p = Popen(["java", "-jar", package_path + "/java/Class2Java.jar", path],
                stdout=file)
        p.communicate(timeout=5)
    except TimeoutExpired:
        p.kill()
        p.communicate()
    finally:
        file.flush()
        file.close()



def decompile(apk, dir):
    package_path = os.path.dirname(os.path.realpath(__file__))
    if not os.path.exists(dir):
        Path(dir).mkdir(parents=True, exist_ok=True)
    #basename = os.path.basename(apk)
    call(["apktool", "-f", "d", apk, "-o", "%s/apktools/" % (dir)])
    call(["unzip", apk, "-d", "%s/zip" % (dir)])
    call([glob.glob(package_path + "/tools/dex-tools/*/d2j-dex2jar.sh")[0],
        "%s/zip/classes.dex"\
        % (dir), "-o", "%s/zip/apk.jar" % (dir)])
    return jar2java("%s/zip/apk.jar" % (dir), "%s/src/" % (dir))
    #try:
    #    p = Popen(["java", "-jar", package_path + "/tools/jd-cli/jd-cli.jar", "-od", "%s/%s/src/" % (dir, basename) ,"-sr",
    #    "%s/%s/zip/apk.jar" % (dir, basename)], shell=False) 
    #    p.communicate(timeout=30)
    #except TimeoutExpired:
    #    p.kill()
    #    p.communicate()
    #    p.wait()
    #    print("Maybe the decompilation is imcomplete")
    #    return p.pid
    #return 0

def main():
    parser = argparse.ArgumentParser(description='apk2java convert apk to java')
    parser.add_argument('apk', type=str, help='path to apk')
    parser.add_argument('dir', type=str, help='path to decompile')

    args = parser.parse_args()

    return decompile(args.apk, args.dir)

