"""
(c) Dativa 2012-2020, all rights reserved

This code is licensed under MIT license (see license.txt for details)

Classes to cache query results locally or on S3

Saves with a unique hash to guarantee the same result and long as the queries are deterministic and
the underlying data has not changed.

"""

import json
import datetime
import logging
import os
import gzip as gz
import re
import shutil
import hashlib

from newtools.aws import S3Location
from newtools.optional_imports import SqlClient, AthenaClient
from newtools.doggo import DoggoLock, DoggoFileSystem

logger = logging.getLogger("dativa.attribution.cached_query")

# Set S3fsMixin for backwards compatibility
S3fsMixin = DoggoFileSystem


class BaseCachedClass:
    validation_mode = False

    def __init__(self, cache_path):
        self.cache_path = cache_path
        self.dfs = DoggoFileSystem()

    def _exists(self, path):
        """
        Checks whether a path exists locally or on S3

        :param path: the path to check
        :return: True if the path exists
        """
        if self.validation_mode:
            return True
        else:
            return self.dfs.exists(path)

    @staticmethod
    def _get_file_hash(files):
        """
        Returns a hash based on the file contents

        :param files: a list the file to hash
        :return: an MD5 hex digest
        """

        hasher = hashlib.md5()
        for file in files:
            with open(file, 'rb') as afile:
                buf = afile.read()
                hasher.update(buf)
        return hasher.hexdigest()

    @staticmethod
    def _get_dict_hash(*my_dicts):
        """
        Returns a hash based on a dictionary

        :param my_dicts: the dictionary/ies to hash
        :return: an MD5 hex digest
        """

        return hashlib.md5("".join([json.dumps(d, sort_keys=True) for d in my_dicts if d is not None])
                           .encode('utf-8')).hexdigest()

    def get_cache_path(self, prefix, files_to_hash, data_hash="", suffix=""):
        """
        Returns the location to cache the output to

        :param prefix: the name of the file
        :param files_to_hash: the name of the file to hash in the output name
        :param data_hash: an additional hash to add to the string
        :param suffix: a suffix to add to the end
        :return: the full path to cache to
        """

        data_hash = [] if data_hash == "" else [data_hash]

        hash_list = [prefix, self._get_file_hash(files_to_hash)] + data_hash

        file = "_".join(hash_list) + ".csv" + suffix

        if self.cache_path.startswith("s3://"):

            return S3Location(self.cache_path).join(file)

        else:
            return os.path.join(self.cache_path, file)


class BaseCachedQuery(BaseCachedClass):
    _archive_path = None

    wait_period = 30
    time_out_seconds = 1800
    maximum_age = 3600

    def __init__(self, params=None, cache_path="", sql_archive_path=None, sql_paths=None, gzip=True):
        """
        Cached query class

        :param params: a dictionary of parameters passed to each query
        :param cache_path: the path locally or on S3 to cache query results
        :param sql_archive_path: the path locally or on S3 to store archive SQL queries
        :param sql_paths: a list of paths to search for SQL queries
        :param gzip: if set, then results will be compression
        """
        super().__init__(cache_path)

        self._gzip = gzip
        self._args = self._validate_args(params)

        self._sql_paths = ['sql', os.path.join(os.path.split(__file__)[0], 'sql')]
        if sql_paths is not None:
            self._sql_paths = self._sql_paths + sql_paths

        self._archive_path = sql_archive_path

    def _validate_args(self, args):
        """
        Validated passed parameters and creates the arguments

        :param args: a dictionary of parameters
        """
        if args is not None:
            # create the S3 credentials
            try:
                args["s3_credentials"] = "aws_access_key_id={0};aws_secret_access_key={1}".format(
                    args["aws_access_key_id"],
                    args["aws_secret_access_key"])
            except KeyError:
                pass

            # now log out all the parameters
            self._log_parameters(args)

            return args
        else:
            return dict()

    def archive_path(self, file_path):
        """
        Calculates the archive path for the SQL queries

        :param: the path of the SQL files

        :return: the location to save the archived SQL file
        """
        if self._archive_path is None:
            return None
        else:
            return os.path.join(self._archive_path, os.path.split(file_path)[1])

    def get_sql_file(self, file):
        """
        Search SQL paths for the named query

        :param file: the SQL file to get
        :return: a full path to the SQL file
        """
        for p in self._sql_paths:
            f = os.path.join(p, file)
            if os.path.exists(f):
                return f

        raise ValueError("SQL file {0} not found in {1}".format(
            file,
            ",".join(self._sql_paths)
        ))

    @staticmethod
    def _clean_dict(d):
        """
        Removes any secret terms from a dictionary, for logging

        :param d: the dictionary to search
        :return: a clean dictionary
        """
        block_words = ["secret", "password", "credentials"]
        clean = {}
        for param in d:
            if any(x.lower() in param.lower() for x in block_words):
                clean[param] = "*" * len(d[param])
            else:
                clean[param] = d[param]

        return clean

    def _log_parameters(self, params):
        """
        Logs SQL parameters excluding any secret terms

        :param params: a dict of parameters
        """
        if params is not None:
            clean = self._clean_dict(params)
            for param in clean:
                logger.info("{0} = {1}".format(param, clean[param]))

    @staticmethod
    def __format_list(the_listl):

        if len(the_listl) == 1:
            the_listl = the_listl + ["There is really no chance that this will be a match in the database"]

        return tuple(the_listl)

    def clear_cache(self,
                    sql_file,
                    output_prefix,
                    params=None,
                    replacement_dict=None):
        """
        Clears the cache of the specified SQL file

        :param sql_file: the SQL file to delete the cachec
        :param output_prefix: the output path to use for the cache
        :param params: the parameters to use in the cache
        :param replacement_dict: and replacement to be made in the query's text
        :return:
        """
        # set the path
        path = self.get_cache_path(
            prefix=output_prefix,
            files_to_hash=[self.get_sql_file(sql_file)],
            data_hash=self._get_dict_hash(params, replacement_dict),
            suffix=".gz" if self._gzip else "")

        with DoggoLock(path,
                       wait_period=self.wait_period,
                       time_out_seconds=self.time_out_seconds,
                       maximum_age=self.maximum_age):
            if self._exists(path):
                self.dfs.rm(path)

    @staticmethod
    def _validate_sql(sql_file):
        """
        Implemented by the child class and raise an exception if it's not valid

        :param sql_file: the SQL file to validate
        """
        pass

    def get_results(self,
                    sql_file,
                    output_prefix,
                    params=None,
                    replacement_dict=None):
        """
        Runs the specified SQL file

        :param sql_file: the SQL file to run
        :param output_prefix: the output path to use for this query
        :param params: the parameters to use in the query
        :param replacement_dict: and replacement to be made in the query's text
        :return:
        """

        # get a set of query parameters, with passed arguments taking precedence
        query_parameters = dict(self._args)
        if params is not None:
            query_parameters.update(params)

        # Format lists
        for arg in query_parameters:
            if type(query_parameters[arg]) == list:
                query_parameters[arg] = self.__format_list(query_parameters[arg])

        # set the path
        file_path = self.get_sql_file(sql_file)
        self._validate_sql(file_path)

        output_file = self.get_cache_path(
            prefix=output_prefix,
            files_to_hash=[file_path],
            data_hash=self._get_dict_hash(params, replacement_dict),
            suffix=".gz" if self._gzip else "")

        self._log_parameters(params)

        if not self._exists(output_file):
            # Get the file file lock
            with DoggoLock(output_file,
                           wait_period=self.wait_period,
                           time_out_seconds=self.time_out_seconds,
                           maximum_age=self.maximum_age):
                # Check to see if it exists...
                if not self._exists(output_file):
                    # clean up any S3 files with the same prefix
                    for file in self.dfs.glob(output_file + "**"):
                        self.dfs.rm(file)

                    logger.info("Executing query to {0}".format(output_file))
                    self._execute_query(query_file=file_path,
                                        output_file=output_file,
                                        query_parameters=query_parameters,
                                        replacement_dict={} if replacement_dict is None else replacement_dict)

                    # In the S3 case, redshift files are saved with a prefix and need to be renamed
                    if output_file.startswith("s3://"):
                        if not self.dfs.exists(output_file):
                            files = self.dfs.glob(output_file + "**")
                            if len(files) == 0:
                                raise ValueError("No file returned by the query. Does it contain an UNLOAD command?")
                            elif len(files) > 1:
                                raise ValueError(
                                    "More than one file produced by query. Is PARALLEL OFF set in your UNLOAD command?")
                            else:
                                self.dfs.mv(files[0], output_file)

        logger.info("Loading query from {0}".format(output_file))
        return output_file

    def _execute_query(self, **params):
        # Implemented by child
        raise NotImplementedError("BaseCachedClass cannot execute queries")


class CachedPep249Query(BaseCachedQuery):
    """
    A CachedQuery class compatible with PEP249 classes
    """
    __sql = None

    def __init__(self, pep_249_obj, params=None, cache_path="", sql_archive_path=None, sql_paths=None, gzip=True):
        super().__init__(params, cache_path, sql_archive_path, sql_paths, gzip)

        self._sql = SqlClient(pep_249_obj,
                              logger=logger,
                              logging_level=logging.INFO)

    @staticmethod
    def _validate_sql(sql_file):
        """
        Checks for unescape % signs in the SQL file which doesn't work for Parameters

        Raise an exception if it's not valid

        :param sql_file: the SQL file to validate
        """
        with open(sql_file, 'rt') as f:
            sql = f.read()
            # check for unescaped %
            if re.search("%[^%]", sql):
                raise ValueError("SQL file {0} contains unescaped % signs that will not run".format(sql_file))

    def _execute_query(self,
                       query_file,
                       output_file,
                       query_parameters,
                       replacement_dict):
        """
        Executes the query

        :param query_file: the query to run
        :param output_file: the location to store the output
        :param query_parameters: the full set of query parameters to use
        :param replacement_dict: any items to replace directly in the SQL code
        :return:
        """

        if '{s3_path' in open(query_file).read():
            # many of our queries include an UNLOAD to S3 path statement and require s3_path
            query_parameters["s3_path"] = output_file

            self._sql.execute_query(query=query_file,
                                    parameters=query_parameters,
                                    replace=replacement_dict,
                                    archive_query=self.archive_path(query_file))
        else:
            # otherwise run and save directly to CSV
            self._sql.execute_query_to_csv(query=query_file,
                                           csvfile=output_file,
                                           parameters=query_parameters,
                                           replace=replacement_dict,
                                           archive_query=self.archive_path(query_file))


class CachedAthenaQuery(BaseCachedQuery):
    """
    A CachedQuery class for AWS Athena

    """
    __ac = None

    @property
    def _ac(self):
        """

        :return: the AthenaClient class to use
        """
        if self.__ac is None:
            self.__ac = AthenaClient(region=self._args.get('aws_region', 'us-east-1'),
                                     db=self._args['athena_db'],
                                     workgroup=self._args.get('workgroup', None))

        return self.__ac

    def _archive_query(self, logged_query, parameters, file):
        """
        Logs the query to the archive location

        :param logged_query: the text of the query
        :param parameters: the parameters to apply
        :param file: the archive file path
        """
        with self.dfs.open(file, 'wb') as f:  # FileDoggo does not support "wt" for S3 files
            f.write('-- Ran query on: {:%Y-%m-%d %H:%M:%S}\n'.format(datetime.datetime.now()).encode('UTF-8'))
            f.write('-- Parameters: {0}\n'.format(self._clean_dict(parameters)).encode('UTF-8'))
            f.write((logged_query + ';\n').encode('UTF-8'))

    def _execute_query(self,
                       query_file,
                       output_file,
                       query_parameters,
                       replacement_dict):
        """
        Executes the query

        :param query_file: the query to run
        :param output_file: the location to store the output
        :param query_parameters: the full set of query parameters to use
        :param replacement_dict: any items to replace directly in the SQL code
        :return:
        """

        # run the query to unload them
        with open(query_file) as f:
            actual_query = f.read()

            # Apply any replacements
            for key in replacement_dict:
                actual_query = actual_query.replace(key, replacement_dict[key])

            # Apply the parameters
            actual_query = actual_query.format(
                **query_parameters)

        # Save an archive copy of the query
        archive_query_path = self.archive_path(query_file)
        if archive_query_path is not None:
            self._archive_query(actual_query, query_parameters, archive_query_path)

        # Now now the query on Athena
        res = self._ac.add_query(
            sql=actual_query,
            name="unload {}".format(output_file),
            output_location=self.cache_path)
        self._ac.wait_for_completion()

        actual_file = S3Location(self.cache_path).join(res.id + '.csv')

        # gzip the output
        if self._gzip:
            gz_file = output_file
            with self.dfs.open(actual_file, 'rb') as f_in:
                with self.dfs.open(gz_file, 'wb') as f_out:
                    with gz.open(f_out, 'wb') as gz_out:
                        shutil.copyfileobj(f_in, gz_out)

        # delete the metadata file
        self.dfs.rm(actual_file)
        self.dfs.rm(actual_file + '.metadata')
