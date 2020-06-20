# (c) 2012-2020 Dativa, all rights reserved
# -----------------------------------------
#  This code is licensed under MIT license (see license.txt for details)

"""
           __.
        .-".'                      .--.            _..._
      .' .'                     .'    `       .-""  __ ""-.
     /  /                     .'       : --..:__.-""  ""-. \
    :  :                     /         ;.d$$    sbp_.-""-:_:
    ;  :                    : ._       :P .-.   ,"TP
    :   `                    `  T--...-; : d$b  :d$b
     `   `.                   `  `..'    ; $ $  ;$ $
      `.   "-.                 ).        : T$P  :T$P
        `..---^..             /           `-'    `._`._
       .'        "-.       .-"                     T$$$b
      /             "-._.-"               ._        '^' ;
     :                                    `.`.         /
     ;                                -.   ``."-._.-'-'
    :                                 .'`   ` ` ` `
    ;  ;                             /:  `   ` ` . ;
   :   :                            ,  ;  `.  `.;  :
   ;    `        ;                     ;    "-._:  ;
  :      `.      :                     :         `/
  ;       /"-.    ;                    :
 :       /    "-. :                  : ;
 :     .'        T-;                 ; ;
 ;    :          ; ;                /  :
 ;    ;          : :              .'    ;
:    :            ;:         _..-"`     :
:     `           : ;       /      `     ;
;    . '.         '-;      /        ;    :
;  `  ; :           :     :         :    '-.
'.._L.:-'           :     ;    bug   ;    . `.
                     ;    :          :  `  ; :
                     :    '-..       '.._L.:-'
                      ;     , `.
                      :   `  ; :
                      '..__L.:-'
"""

from io import BytesIO
import re
import gzip

from newtools.optional_imports import boto3
from newtools.optional_imports import pandas as pd

from newtools.aws import S3Location

import logging

logger = logging.getLogger("newtools.doggo")


def _gzip_wrapped(func):
    def gzip_open(self, *args, **kwargs):
        if self.compression == 'gzip':
            f = func(self, *args, **kwargs)
            self._to_close.append(f)
            return gzip.open(f, self.mode)
        return func(self, *args, **kwargs)

    return gzip_open


class PandasDoggo:
    """Is a Panda a doggo?

    ░░░░░░░░▄██▄░░░░░░▄▄░░
    ░░░░░░░▐███▀░░░░░▄███▌
    ░░▄▀░░▄█▀▀░░░░░░░░▀██░
    ░█░░░██░░░░░░░░░░░░░░░
    █▌░░▐██░░▄██▌░░▄▄▄░░░▄
    ██░░▐██▄░▀█▀░░░▀██░░▐▌
    ██▄░▐███▄▄░░▄▄▄░▀▀░▄██
    ▐███▄██████▄░▀░▄█████▌
    ▐████████████▀▀██████░
    ░▐████▀██████░░█████░░
    ░░░▀▀▀░░█████▌░████▀░░
    ░░░░░░░░░▀▀███░▀▀▀░░░░
    """

    def __init__(self, boto_session=None):
        """

        @param boto_session: optional boto3 session to use for
        @type boto_session: boto3.Session
        """

        if boto_session:
            self.s3_client = boto_session.client('s3')
        else:
            self.s3_client = None

    @staticmethod
    def _extract_file_format(path):
        try:
            f = re.match(r'(?:.*/)?\w+\.(?P<ext>[^.]+)(?:\.[gz]+(?:ip)?)?$', path).group('ext')
        except AttributeError:
            raise ValueError(f'could not determine format of path: {path}, use file_format param to specify')

        if f not in ('csv', 'parquet', 'pq'):
            raise ValueError(f'detected format: {format} is not recognized file format for load')

        return f

    @staticmethod
    def _extract_compression(path):
        # extend for other compression

        if path.endswith('.gzip') or path.endswith('.gz'):
            return 'gzip'
        if path.endswith('.zip'):
            return 'zip'

    def load(self, path, file_format=None, compression=None, *args, **kwargs):
        """Load a file into a Pandas.DataFrame from local or s3 locations.

        @param path: path to the file to load, string or s3 location, local or s3
        @type path: str
        @param file_format: 'csv', 'parquet' currently supported
        @param compression: optional, 'gzip' or None
        @param args: args to pass to the panda to load the file
        @param kwargs: kwargs to pass to the panda to load the file eg columns=['subset', 'of', 'columns']
        @return: Pandas.DataFrame
        """

        file_format = file_format or self._extract_file_format(path)

        if file_format not in ('csv', 'parquet', 'pq'):
            raise ValueError(f'detected format:{format} is not recognized file format for load')

        if file_format == 'csv':
            return self.load_csv(path, compression=compression, *args, **kwargs)

        elif file_format in ('parquet', 'pq'):
            return self.load_parquet(path, compression=compression, *args, **kwargs)

    def load_csv(self, path, compression=None, *args, **kwargs):
        """alias for .load(path, format='csv')"""
        if 'chunksize' in kwargs:
            raise NotImplementedError("PandasDoggo does not support chunksize for loading data frames")

        compression = compression or self._extract_compression(path)
        fm = FileDoggo(path, mode='rb', client=self.s3_client, compression=compression)
        with fm as f:
            df = pd.read_csv(f, *args, **kwargs)

        return df

    def load_parquet(self, path, compression=None, *args, **kwargs):
        """alias for .load(path, format='csv')"""

        compression = compression or self._extract_compression(path)
        fm = FileDoggo(path, mode='rb', client=self.s3_client, compression=compression)
        with fm as f:
            df = pd.read_parquet(f, engine='pyarrow', *args, **kwargs)

        return df

    def save(self, df, path, file_format=None, compression=None, *args, **kwargs):
        """Save a file into a Pandas.DataFrame from local or s3 locations.

        @param df: Data frame
        @type df: Pandas.DataFrame
        @param path: path to save the file, string or s3 location, local or s3
        @type path: str
        @param file_format: 'csv', 'parquet' currently supported
        @param compression: optional, 'gzip' or None
        @param args: args to pass to the panda to save the file
        @param kwargs: kwargs to pass to the panda to load the file eg index=None
        """

        file_format = file_format or self._extract_file_format(path)

        if file_format == 'csv':
            return self.save_csv(df, path, compression, *args, **kwargs)

        elif file_format in ('parquet', 'pq'):
            return self.save_parquet(df, path, compression, *args, **kwargs)

    def save_csv(self, df, path, compression=None, *args, **kwargs):
        """Alias for .save(df, format='csv')"""
        compression = compression or self._extract_compression(path)
        fm = FileDoggo(path, mode='wb', client=self.s3_client, compression=compression)
        with fm as f:
            f.write(df.to_csv(None, *args, **kwargs).encode('utf-8'))

    def save_parquet(self, df, path, compression=None, *args, **kwargs):
        """Alias for .save(df, format='parquet')"""
        fm = FileDoggo(path, mode='wb', client=self.s3_client, compression=compression)
        with fm as f:
            df.to_parquet(f, *args, **kwargs)


class FileDoggo:
    """Fetch!

           ____,'`-,
      _,--'   ,/::.;
   ,-'       ,/::,' `---.___        ___,_
   |       ,:';:/        ;'"`;"`--./ ,-^.;--.
   |:     ,:';,'         '         `.   ;`   `-.
    `:.,:::/;/ -:.                   `  | `     `-.
     `:::,'//__.;  ,;  ,  ,  :.`-.   :. |  ;       :.
      `,',';/O)^. :'  ;  :   '__` `  :::`.       .:' )
      |,'  |`__,: ;      ;  '/O)`.   :::`;       ' ,'
           |`--''            `__,' , ::::(       ,'
           `    ,            `--' ,: :::,'`   ,-'
            | ,;         ,    ,::'  ,:::   |,'
            |,:        .(          ,:::|   `
            ::'_   _   ::         ,::/:|
           ,',' `-' `   `.      ,:::/,:|
          | : _  _   |   '     ,::,' :::
          | ` O`'O  ,',   ,    :,'   ;::
           ` `-'`--',:' ,' , ,,'      ::
            ``:.:.__   ',-','        ::'
    -hrr-      `--.__, ,::.         ::'
                   |:  ::::.       ::'
                   |:  ::::::    ,::'
    """

    _connection = None

    def __init__(self, path, mode='rb', is_s3=None, client=None, compression=None):
        """
        @param path: path to file to connect to
        @type path: str or S3Location
        @param mode: opening mode for file, note s3 only allows 'rb' or 'wb'
        @param is_s3: force Doggo to treat path as an S3Location
        @type is_s3: bool
        @param client: optional `boto3.Session().Client('s3')` instance to use for s3 operations
        @param compression: None or 'gzip'.
        """

        self.buffer = BytesIO()
        self.mode = mode

        self.is_s3 = is_s3 or path.startswith('s3://')
        if self.is_s3:
            # allows you to specify s3 for paths that don't begin with s3:// for whatever reason you might want
            self.path = S3Location(path)
        else:
            self.path = path

        self._client = client
        if compression in [None, 'gzip']:
            self.compression = compression
        else:
            raise NotImplementedError(f"Compression {compression} is not supported in FileDoggo")
        self._to_close = []

    @property
    def connection(self):
        if not self._connection:
            self._connection = self._connect()
        return self._connection

    @property
    def client(self):
        if not self._client:
            self._client = boto3.Session().client('s3')
        return self._client

    def close(self):

        if self._connection:
            for c in [self._connection] + self._to_close:
                if not c.closed:
                    c.close()

    def __enter__(self):
        return self.connection

    def __exit__(self, etype, value, traceback):
        # ¯\_(ツ)_/¯
        if self.is_s3 and 'w' in self.mode:
            self._write_s3()

        self.close()

    @_gzip_wrapped
    def _connect(self):

        if self.is_s3:
            if self.mode == 'rb':
                return self._read_s3()
            elif self.mode == 'wb':
                # check s3 exists? meh, writing to a buffer is so fast i think the overhead isn't worth
                return self.buffer  # write to this buffer and we'll upload later
            else:
                raise ValueError(f'mode {self.mode} is not supported')

        else:

            return open(self.path, self.mode)

    def _read_s3(self):

        self.client.download_fileobj(Bucket=self.path.bucket, Key=self.path.key, Fileobj=self.buffer)
        self.buffer.seek(0)
        return self.buffer

    def _write_s3(self):

        if self.compression == 'gzip':
            self.connection.close()  # flushes writing to gzip

        self.buffer.seek(0)
        self.client.upload_fileobj(Bucket=self.path.bucket, Key=self.path.key, Fileobj=self.buffer)
