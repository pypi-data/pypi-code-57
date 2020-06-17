import os
import tempfile
import click
from aos.managers.misc import aos_error
from aos.managers import metadata
from aos.managers.constant import PYURLPKG

if PYURLPKG == 'urlgrabbder':
    from urlgrabber.grabber import URLGrabber
    from urlgrabber.grabber import URLGrabError
elif PYURLPKG == 'requests':
    import requests

class RepoError(Exception):
    pass

class Repo():
    def __init__(self, repourl, cachedir):
        self.repoMDFile = "repodata/repomd.xml"
        self.url = repourl
        self.cachedir = cachedir

    def getFile(self, url, relative, localfile):
        """ Download files from yum repo """
        result = ''
        remote = url + '/' + relative
        dest_dir = os.path.dirname(localfile)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        if PYURLPKG == 'urlgrabber':
            ug = URLGrabber(reget='simple')
            try:
                result = ug.urlgrab(remote, localfile, reget=None)
            except URLGrabError as e:
                if os.path.exists(localfile):
                    os.unlink(localfile)
                raise RepoError("Error downloading file %s: %s" % (localfile, e))
        elif PYURLPKG == 'requests':
            try:
                r = requests.get(remote)
                if r.status_code == 200:
                    with open(localfile, 'wb') as f:
                        f.write(r.content)
                    result = localfile
            except Exception as e:
                if os.path.exists(localfile):
                    os.unlink(localfile)
                raise RepoError("Error downloading file %s: %s" % (localfile, e))
        else:
            aos_error("The url package %s is not supported!" % PYURLPKG)

        return result

    def getCompInfoFile(self):
        """ Download component_info_publish.db as localfile """
        comp_info_f = "component_info_publish.db"
        localfile = os.path.join(self.cachedir, comp_info_f)

        # Remove the old existing file
        if os.path.exists(localfile):
            os.unlink(localfile)

        # Download a new file from server
        try:
            result = self.getFile(self.url, comp_info_f, localfile)
        except RepoError as e:
            pass

        return localfile

    def getRepoFile(self):
        """ Download repomd.xml as localfile """
        repomd_xml = self.repoMDFile
        localfile = os.path.join(self.cachedir, repomd_xml)

        try:
            tfname = tempfile.mktemp(prefix='repomd', suffix="tmp.xml",
                                     dir=os.path.dirname(localfile))
            result = self.getFile(self.url, repomd_xml, localfile)
        except Exception as e:
            if os.path.exists(localfile):
                os.unlink(tfname)
            raise RepoError("Error downloading file %s: %s" % (localfile, e))

        try:
            os.rename(result, localfile)
        except:
            os.unlink(tfname)
            raise RepoError("Error renaming file %s to %s" % (result, localfile))

        return localfile

    def getMDFile(self, mdtype):
        """ Download metadata files: primary, filelists, other """
        repomd_xml = os.path.join(self.cachedir, self.repoMDFile)
        if not os.path.exists(repomd_xml):
            raise RepoError("No such file: %s" % repomd_xml)

        repomd = metadata.RepoMD(repomd_xml)
        data = repomd.getData(mdtype)

        (r_base, remote) = data.location
        localfile = os.path.join(self.cachedir, remote)
        try:
            result = self.getFile(self.url, remote, localfile)
        except RepoError as e:
            pass

        return localfile

    def getPackage(self, package):
        """ Download rpm packages """
        remote = package
        localfile = os.path.join(self.cachedir, package)
        try:
            result = self.getFile(self.url, remote, localfile)
        except RepoError as e:
            pass

        return localfile
