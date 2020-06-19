import hashlib
import requests
import logging
import pickle
import gzip
from pathlib import Path
from urllib.parse import urlparse


class CRequests(requests.Session):
    def __init__(self, cacheFolder):
        """Constructor. Create cachefolder, if it doesn't exist already

        Args:
            cacheFolder (str): Folder where scaping cache content should be stored.
        """
        self.logger = logging.getLogger(__name__)  # Use our own logging instance
        self.logger.debug(f"CacheScrape is using {cacheFolder} as cache directory")

        self.cacheFolder = cacheFolder
        Path(cacheFolder).mkdir(parents=True, exist_ok=True)

        self.__lastReqWasCashed = False

        super().__init__()

    def __getCacheFileInfo(self, method, url, **kwargs):
        """From a provided method, URL and kwargs is generated a unique dir/filename with sha1
        The reason we need these 3 parameters is that the hash has to be unique according to the parameters
        passed to requests.Session.request.

        Args:
            method(str): GET, POST, DELETE etc.
            url (str): URL that should be converted into a filename
            kwargs: Arguments passed on from requests.Session.request


        Returns:
            dict:   filename: raw sha1 filename. (eg fe334fefa2323b3434)
                    filedir: directory of the file. (eg cachedir/www.google.com/fe)
                    filefullpath: full path to file. (eg cachedir/www.google.com/fe/334fefa2323b3434)
        """
        m = hashlib.sha1()  # Build a hash of 3 parameters
        m.update(method.encode())  # Method: POST/GET/DELETE...
        m.update(url.encode())  # URL
        m.update(repr(kwargs).encode())  # And also the kwargs

        hostname = urlparse(url).netloc.split(":")[0]  # Remove portinformation
        filename = m.digest().hex()
        filedir = self.cacheFolder + "/" + hostname + "/" + filename[:2]

        fileFullPath = filedir + "/" + filename

        return {"filedir": filedir, "filename": filename, "filefullpath": fileFullPath}

    def __writeCacheFile(self, url, requestObject, fileInfo):
        """Writes the raw webcontent to a cachefile that is derived from the URL.

        Args:
            url (str): URL url where that cache content comes from
            urlContent (requests.response): the raw content from the webpage
        """
        filefullpath = fileInfo["filefullpath"]
        filedir = fileInfo["filedir"]
        self.logger.info(f"Writing cachefile '{filefullpath}' with content of '{url}'")

        Path(filedir).mkdir(parents=True, exist_ok=True)  # Make sure there is a dir for the file
        with gzip.open(filefullpath, "wb") as fp:  # Save a gzip compressed pickle of response
            pickleData = pickle.dumps(requestObject)
            fp.write(pickleData)
        with open(f"{filefullpath}_url.txt", "w") as fp:  # Save metadata about the webcontent
            fp.write(url)

    def __readCacheFile(self, url, fileInfo):
        """Reads raw webcontent from a cachefile that is derived from the URL.

        Args:
            url (str): URL that should be read from disk

        Returns:
            requests.response: The raw data from the webpage, that is fetched from disk.
                                If nothing is on disk, None is returned
        """
        filename = fileInfo["filefullpath"]
        if Path(filename).is_file():
            self.logger.info(f"CACHE-HIT. '{url}' got cacheinfo in '{filename}'")
            with gzip.open(filename, "rb") as fp:  # Load a gzip compressed pickle of response
                pickleData = fp.read()
                requestObject = pickle.loads(pickleData)
                self.__lastReqWasCashed = True
        else:  # Cache file does not exist
            self.logger.info(f"CACHE-MISS. '{url}' not in cache.")
            requestObject = None
            self.__lastReqWasCashed = False
        return requestObject

    def request(self, method, url, forceRefresh=False, **kwargs):
        """Gets data from website if it's not in cache and returns it.
        If data is in cache the data is returned from here.
        If the url is invalid or unreadable, then None is returned

        Args:
            url (str): URL we want data from
            reqFunc(functionptr): A pointer to the function in requests-module to call
            forceRefresh (bool, optional): If set to True, the data is fetched again from the website.
                                            Defaults to False.
            **kwargs: kwargs to pass on the the requests function

        Returns:
            bytestring: The raw data from the website.
        """
        fileInfo = self.__getCacheFileInfo(method, url, **kwargs)

        self.logger.debug(f"{method} request for {url}")
        responseObject = None
        if not forceRefresh:  # If we are not overriding cache, we load file from cache
            responseObject = self.__readCacheFile(url, fileInfo)
        if (responseObject is None) or forceRefresh:
            # If no data in cachefile, or we are overriding, then get from web
            self.logger.info(f"Getting data directly from: {url}")
            responseObject = super().request(method, url, **kwargs)
            self.__writeCacheFile(url, responseObject, fileInfo)
        return responseObject

    @property
    def lastReqWasCashed(self):
        return self.__lastReqWasCashed
