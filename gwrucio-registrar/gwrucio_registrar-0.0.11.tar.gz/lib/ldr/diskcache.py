#!/usr/bin/python
# Taken from https://git.ligo.org/computing/ligo-data-replicator/-/tree/master/python-ldrv1-master/ldrv1
from __future__ import absolute_import
from __future__ import print_function
from ligo.segments import *
from ligo.segments.utils import segmentlist_range
from os.path import split, exists, join
from time import time
from re import compile, match, search
from stat import ST_MTIME
from time import sleep

import mimetypes
import gzip
import os
from six.moves import range
from six.moves import zip

# the known ascii dump versions
VERSION_SINGLE = 0x00ff
VERSION_MULTI = 0x0101
# we want the preceding 0's for the magic string (hex strips them)
VERSION_SINGLE_STR = "0x00ff"
VERSION_MULTI_STR = "0x0101"        

TOO_MANY_FILES = 1e6

def diskcache_expand(d):
    """return  list of strings described by d, where 
        d is dict with keys
    {"directory", "frame_type", "site", "dur", "ext", "segmentlist"}
    """
    for dc_seg in d["segmentlist"]:
        for gps in range(dc_seg[0], dc_seg[1], d['dur']):
            lfn = '-'.join(
                [d["site"], d["frame_type"], str(gps), str(d["dur"])]
            ) + d["ext"]
            yield '/'.join([d["directory"], lfn])

class DiskCacheBase(list):
    '''DiskCache is a list of dictionaries with a key constraint:
    ('directory', 'frame_type', 'site', 'dur', 'ext')

    It is populated using information in the diskcache_file and
    optionally filter_list and regexp. Regexp may be a string or a
    compiled regular expression and is applied directly to the
    diskcache ascii dump.

    diskcache parses the frame filename.  It requires that
    'site-frame_type-gps_start-dur.extension' convention is followed

    Note that 'extension' does include the dot.  Within the ascii file
    dump, the extension _also_ includes the dot.
    '''
    
    def __init__(self, version, filter_list=[], extension=None,
                 regexp='', minimum_gps=None, maximum_gps=None, 
                 prune=True, update_file_count=True):

        # extension and parse depend on the version. We assume
        # self._extension is set to something. Set self._parse
        # depending on the version.
        self.version = version
        self._extension = None
        if version == VERSION_SINGLE:
            if extension is None:
                self.extension = ".gwf"
            else:
                if match('\.', extension):
                    self.extension = extension
                else:
                    self.extension = '.' + extension
            self._parse_ = self._parse_0x00ff
        elif version == VERSION_MULTI:
            self._parse_ = self._parse_0x0101
        else:
            raise NotImplementedError("Unknown version %x" % hex(version))

        # some details about modifying content of the diskcache
        # iterator contents
        self.prune = bool(prune)
        self.update_file_count = bool(update_file_count)

        self.filter_list = filter_list
        self.regexp = compile(regexp)
        self.minimum_gps = minimum_gps
        # Please do not alter maximum_gps to behave like
        # maximum_gps+1. See comments below.
        self.maximum_gps = maximum_gps 

        # 'read' time: (approximate) mtime of file when file last read
        # setting this should precede actual reading of the file; use
        # to test staleness of internal data
        self.refresh()

    @property
    def extension(self):
        return self._extension

    @extension.setter
    def extension(self, val):
        if self.version == VERSION_SINGLE:
            self._extension = val
        else: 
            raise ValueError("Cannot set extension with the current version")
        for d in self:
            d['ext'] = val

    def __contains__(self, item):
        '''
        item should be path of frame file

        allow for syntax 

        if <path> in <diskcache instance>:
            ...
        '''
        try:
            directory, basename = split(item)
            site, frame_type, gps_start, durext = basename.split('-')
            durstr, ext = durext.split('.')
            _ext = "." + ext
            dur = int(durstr)
            gps_start = int(gps_start)
            return bool([
                d for d in self if
                d['directory'] == directory and
                d['ext'] == _ext and
                d['site'] == site and
                d['frame_type'] == frame_type and
                d['dur'] == dur and
                segment(gps_start, gps_start + dur) in d['segmentlist']])
        except:
            return False

    def _parse_(self, line):
        raise NotImplementedError("parse is not implemented")
        
    def _parse_0x0101(self, line):
        '''
        return line from diskcache converted to a dictionary
        '''
        header, mod_time, file_count, segment_bdry = line.strip().split(' ', 3)
        directory, site, frame_type, ext, number1, duration = header.split(',')

        tmp = [int(s) for s in segment_bdry[1:-1].split()]
        segment_bdry = list(zip(tmp[:-1:2], tmp[1::2]))

        ret = {
            "directory": directory,
            "site": site,
            "frame_type": frame_type,
            "number1": int(number1),
            "dur": int(duration),
            "mod_time": int(mod_time),
            "file_count": int(file_count),
            "ext": ext
            }
        ret['segmentlist'] = segmentlist([segment(s) for s in segment_bdry])

        return ret

    def _parse_0x00ff(self, line):
        '''
        return line from diskcache converted to a dictionary
        '''
        header, mod_time, file_count, segment_bdry = line.strip().split(' ', 3)
        directory, site, frame_type, number1, duration = header.split(',')

        tmp = [int(s) for s in segment_bdry[1:-1].split()]
        segment_bdry = list(zip(tmp[:-1:2], tmp[1::2]))

        ret = {
            "directory": directory,
            "site": site,
            "frame_type": frame_type,
            "number1": int(number1),
            "dur": int(duration),
            "mod_time": int(mod_time),
            "file_count": int(file_count),
            "ext": self.extension
            }
        ret['segmentlist'] = segmentlist([segment(s) for s in segment_bdry])

        return ret

    def expand(self):
        """return iterator that yields a string contained in self.

        full list of iterator is the expanded list of all files
        indexed by the entire diskcache
        """
        for entry in self:
            for i in diskcache_expand(entry):
                yield i

    def dict_keys(self):
        return list(self[0].keys())

    def dict_values(self):
        raise NotImplementedError("Method 'values' is not implemented")

    def segmentlist(self):
        '''return coalesced segmentlist from diskcache file'''
        return sum([d['segmentlist'] for d in self], segmentlist())

    def load(self, dc_iter, filter_list=None):
        '''
        dc_iter is iterator where each entry is a line from the
        diskcache

        return list of dicts with keys ('directory', 'dur', 'site', 'frame_type')
        '''
        content = [self._parse_(l) for l in dc_iter if 
                   not match('#', l) and search(self.regexp, l)]

        keys = [(d['directory'], d['dur'], d['site'], d['frame_type'], d['ext'])
                for d in content]
        
        # integrity check
        if len(keys) != len(set(keys)):
            msg ='Nonunique key in diskcache'
            raise ValueError(msg)

        def _filter_list(d, filter_list=None):
            '''
            return True if each in filter_list applied to d is True
            where d is result of _parse_(LINE)
            
            return False immediately if any filter returns False
            '''
            if filter_list is None:
                filter_list = self.filter_list

            for f in filter_list:
                if not f(d): return False
            return True

        ret = [d for d in content if _filter_list(d)]

        # NB: this is startingly tricky to do correctly, gotchas keep
        # appearing in practice
        #
        # first work on the start point, then work on end point
        #
        # find segment that contains s_0, build the 'gpsstart' times
        # in appropriate order associated with that segment, and
        # choose the first gpsstart time that intersects self_sl
        if self.minimum_gps is not None:
            s_0 = self.minimum_gps
            for d in ret:
                if s_0 in d['segmentlist']:
                    dc_seg = [s for s in d['segmentlist'] if s_0 in s][0]
                    sl_range_args = (dc_seg[0], dc_seg[1], d['dur'])
                    for seg in segmentlist_range(*sl_range_args):
                        if s_0 in seg:
                            d['segmentlist'] &= segmentlist([segment([seg[0], PosInfinity])])
                            break
                else:
                    # this last is needed when s_0 is larger than one
                    # segment, but smaller than the next segment
                    d['segmentlist'] &= segmentlist([segment(s_0, PosInfinity)])

        # Please do not alter maximum_gps to behave like max_gps+1.
        # 
        # When specifying gps-min and gps-max, a user is identifying a
        # set of frames and not a time window. It is possible, quite
        # likely, in fact, that the available frames will not
        # terminate at either boundary gps-min or gps-max.  Rather
        # than suggest through the API that one is including frames
        # with times between the points (gps-min, gps-max), it is more
        # natural to specify "seconds of interest", i.e. frames
        # intersecting (gps-min, gps-min+1) and (gps-max, gps-max+1).
        # Any frame that intersects these seconds of interest will be
        # included.  
        if self.maximum_gps is not None:
            e_0 = self.maximum_gps
            for d in ret:
                if e_0 in d['segmentlist']:
                    dc_seg = [s for s in d['segmentlist'] if e_0 in s][0]

                    # if e_0 is starting point of segment, we're done!
                    if e_0 == dc_seg[0]:
                        d['segmentlist'] &= segmentlist([segment([NegInfinity, e_0])])
                        continue

                    sl_range_args = (dc_seg[0], dc_seg[1], d['dur'])
                    for seg in list(segmentlist_range(*sl_range_args))[::-1]:
                        if e_0 in seg:
                            d['segmentlist'] &= segmentlist([segment([NegInfinity, seg[-1]])])
                            break
                else:
                    # this is needed when e_0 is larger than one
                    # segment, but smaller than the next segment
                    d['segmentlist'] &= segmentlist([segment(NegInfinity, e_0)])
        if self.prune:
            ret= [d for d in ret if d["segmentlist"]]
        if self.update_file_count:
            for d in ret:
                  d["file_count"] = sum((s[1]-s[0])/d["dur"] for s in d["segmentlist"])
        return ret

    def refresh(self, *args, **kwargs):
        raise NotImplementedError('refresh  not implemented')


class DiskCacheFile(DiskCacheBase):
    def __init__(self, diskcache_file, sleepfun=sleep, **kwargs):
        '''
        diskcache_file is path to a diskcache file
        
        each item in filter_list must be a boolean-valued function
        accepting a dictionary whose keys are in self.dict_keys(). For
        example:
        
          filter_list = [lambda x: x['site'] == 'foo', ]

        Only lines matching regexp will be included in the search.
        '''
        self.diskcache_file = diskcache_file

        # inspect the first line of diskcache file to set the file
        # version
        ftype = mimetypes.guess_type(self.diskcache_file)
        self.open = open
        if "gzip" in ftype: self.open = gzip.open

        with self.open(self.diskcache_file) as fh: l = next(fh)

        if VERSION_MULTI_STR in l: version = VERSION_MULTI
        else: version = VERSION_SINGLE

        # read time
        self.rtime = 0

        # customize what to do when sleeping
        self.sleepfun = sleepfun

        super(DiskCacheFile, self).__init__(version, **kwargs)

    def mtime(self):
        return self.__stat__()[ST_MTIME]

    def __stat__(self):
        return os.stat(self.diskcache_file)

    def force_refresh(self, *args, **kwargs):
        '''reread the diskcache file'''
        self.rtime = self.mtime()
        with self.open(self.diskcache_file, 'r') as fh:
            # initialize the *list*, not the base class
            super(DiskCacheBase, self).__init__(self.load(fh, *args, **kwargs))
        
    def refresh(self, max_tries=5, sleeptime=5):
        """
        Refresh the diskcache from file if the file has been
        modified since the last read.

        It can happen that the diskcache file is not available for
        calls to stat or reading. This occurs when a separate process
        is writing a new diskcache file and is a fairly brief state.
        """
        err = ''
        # if you leave the end of this for loop, that is an error
        for ntries in range(max_tries):
            try:
                if self.rtime < self.mtime():
                    self.force_refresh()
                return
            except (IOError, OSError) as e:
                print(("Diskcache read failed (attempt %d of %d)"%(ntries,
                    max_tries)))
                print(("Sleeping for %d s"%sleeptime))
                self.sleepfun(sleeptime)
                sleeptime *= 2
                err = str(e)
        
        msg = 'Problem reading %s: %s' % (self.diskcache_file, err)
        return msg


class DiskCacheIter(DiskCacheBase):
    """
    _iter should be an iterator whose elements are valid diskcacheAPI
    strings
    """
    def __init__(self, iterator, *args, **kwargs):
        self.iterator = iterator
        super(DiskCacheIter, self).__init__(*args, **kwargs)

    def refresh(self, *args, **kwargs):
        '''reread the diskcache iterator. This is only useful if the
        instance's iterator is updated (you must do this manually).'''
        # initialize the *list*, not the base class
        super(DiskCacheBase, self).__init__(self.load(self.iterator, *args, **kwargs))


class DiskCacheIterSingleType(DiskCacheIter):
    """
    thin wrapper of the DiskCacheIter base class
    """
    def __init__(self, iterator, *args, **kwargs):
        super(DiskCacheIterSingleType, self).__init__(
            iterator, VERSION_SINGLE, *args, **kwargs)


if __name__ == "__main__":
    from optparse import OptionParser

    CMD_LIST=["verify", "expand", "raw"]
    
    usage = "usage: %prog FILE_LIST [options]"
    description = "Find data using diskcache"
    version = "%prog 0.1"
    
    parser = OptionParser(usage, version=version, description=description)
    
    # yes, the interval is intended to be the open interval. The interior of the 
    # intervals in question needs to be nonempty.

    parser.add_option("-m", "--gps-min", help="[default: None] Smallest second "
                      "of interest.  Frames intersecting the open interval "
                      "(GPS_MIN,GPS_MIN+1) are included.",
                      default=None, type="int")
    # NOTE: gps-max really is supposed to be inclusive of the second
    # described by [gps-max, gps-max+1).  If you are tempted to change
    # the behavior to [gps-min, gps-max-1), see the above comment.
    parser.add_option("-M", "--gps-max", help="[default: None] Largest second "
                      "of interest.  Frames intersecting the open interval "
                      "(GPS_MAX,GPS_MAX+1) are included. ",
                      default=None, type="int")
    
    parser.add_option("-r", "--regexp", help="[default: ''] include "
                      "only lines from files in FILE_LIST matching regular "
                      "expression.", default='')
    
    parser.add_option("-c", "--command", help="[default: expand] valid "
                      "values are %s." % ", ".join(CMD_LIST), 
                      default="expand", choices=CMD_LIST)
    
    parser.add_option("-e", "--exists", help="Test existence of files in "
                      "diskcache. Only "
                      "sensible when used with '-c expand'.",
                      default=False, action="store_true")

    parser.add_option("--no-update-file-count", 
                      help = "If flag is present, then do not update "
                      "the file_count field of the diskcache.",
                      default=False, action="store_true")

    parser.add_option("--no-prune", help="If flag is present, then"
                      "preserve all all entries with empty segmentlists.",
                      default=False, action="store_true")

    (opts, args) = parser.parse_args()
    
    for f in args:
        dc = DiskCacheFile(f, minimum_gps=opts.gps_min,
                           maximum_gps=opts.gps_max, regexp=opts.regexp, 
                           prune=bool(not opts.no_prune), 
                           update_file_count=bool(not opts.no_update_file_count))
        if opts.command == "expand":
            for i, f in enumerate(dc.expand()):
                if i > TOO_MANY_FILES:
                    raise RuntimeError("Too many files to expand")
                if opts.exists: print(exists(f), f)
                else: print(f)
        elif opts.command == "verify":
            """
            list directories of interest, check that each entry in list of
            directories lives in the set identified by the diskcache
            """
            for i,f in enumerate(dc.expand()):
                if i > TOO_MANY_FILES:
                    raise RuntimeError("Too many files to verify")
            
            s0 = set(list(dc.expand()))

            # list all directories of interest
            s1=set()
            for d in dc:
                s1.update(set(join(d["directory"],l) 
                              for l in os.listdir(d["directory"]) 
                              if join(d["directory"], l) in dc))

            # FIXME
            # offer useful output when these differ
            if s1 != s0:
                raise RuntimeError("Oops!")

        elif opts.command == "raw":
            for d in dc: print(d)
        else:
            raise ProgrammingError("Unknown type")
