import sys
import os
import argparse
import json
import re
import errno
import io
import copy
import txmongo
from twisted.internet import reactor, protocol, defer, task
from twisted.python import log, failure
from mpd import MPDProtocol
from functools import partial
from kmpc.mpdfactory import MpdConnection
from kmpc.extra import KmpcHelpers, SmartStdout, set_defaultencoding_globally
from kmpc.version import VERSION_STR

Helpers = KmpcHelpers()

class MpdParser(object):
    """The main class which queries mpd and dispatches events."""
    def __init__(self, args):
        self.mode = []
        # check what modes were specified, if none then do everything
        if (not args.artists and not args.releases and not args.recordings
                and not args.files and not args.aggregate):
            self.mode = ['artists','releases','recording','files','aggregate']
        else:
            if args.artists:
                self.mode.append('artists')
            if args.releases:
                self.mode.append('releases')
            if args.recordings:
                self.mode.append('recordings')
            if args.files:
                self.mode.append('files')
            if args.aggregate:
                self.mode.append('aggregate')
        # these variables track what uuids we need to operate on
        self.queue = {}
        self.queue['artist'] = {}
        self.queue['release'] = {}
        self.queue['recording'] = {}
        self.args = args
        # how many tasks are left to wait on
        self.waitleft = 0
        # how many mpd queries are left to wait on
        self.mpdqueries = 0
        # aggregation pipelines
        self.recording_pipeline = [
            {'$lookup': {
                'from': "file",
                'localField': "recording.id",
                'foreignField': "musicbrainz_trackid",
                'as': "file_data"
            }},
            {'$unwind': "$recording.artist-credit"},
            {'$unwind': "$recording.release-list"},
            {'$unwind': "$file_data"},
            {'$lookup': {
                'from': "release",
                'localField': "recording.release-list.id",
                'foreignField': "release.id",
                'as': "release_data"
            }},
            {'$unwind': "$release_data"},
            {'$group': {
                '_id': "$recording.id",
                "rating": {'$max': "$file_data.rating"},
                "artist_id": {'$addToSet': "$recording.artist-credit.artist.id"},
                "release_id": {'$addToSet': "$recording.release-list.id"},
                "release_group_id": {'$addToSet': "$release_data.release.release-group.id"}
            }},
            {'$out': "recording_with_rating"}
        ]
        self.artist_pipeline = [
            {'$lookup': {
                'from': "recording_with_rating",
                'localField': "artist.id",
                'foreignField': "artist_id",
                'as': "recording_data"
            }},
            {'$unwind': "$recording_data"},
            {'$group': {
                '_id': "$artist.id",
                'name': {'$first': "$artist.name"},
                'rating': {'$avg': "$recording_data.rating"},
                'stddev': {'$stdDevPop': "$recording_data.rating"},
                'total_tracks': {'$sum': 1},
                'rated_tracks': {'$push': "$recording_data.rating"}
            }},
            {'$project': {
                "name": 1,
                "rating": 1,
                "stddev": 1,
                "total_tracks": 1,
                "rated_tracks": {'$filter':{
                    'input': "$rated_tracks",
                    'cond': {'$ne':["$$this",None]}
                }}
            }},
            {'$project': {
                "name": 1,
                "rating": 1,
                "stddev": 1,
                "total_tracks": 1,
                "top_tracks": {'$filter':{
                    'input': "$rated_tracks",
                    'cond': {'$gte':["$$this",9]}
                }},
                "favorite_tracks": {'$filter':{
                    'input': "$rated_tracks",
                    'cond': {'$gte':["$$this",10]}
                }},
                "rated_tracks": {'$size': "$rated_tracks"}
            }},
            {'$project': {
                "name": 1,
                "rating": 1,
                "stddev": 1,
                "total_tracks": 1,
                "rated_tracks": 1,
                "top_tracks": {'$size': "$top_tracks"},
                "favorite_tracks": {'$size': "$favorite_tracks"},
                "percent_rated": {'$divide':["$rated_tracks","$total_tracks"]},
            }},
            {'$project': {
                "name": 1,
                "rating": 1,
                "stddev": 1,
                "total_tracks": 1,
                "rated_tracks": 1,
                "top_tracks": 1,
                "favorite_tracks": 1,
                "percent_rated": 1,
                "percent_top_tracks": {'$divide':["$top_tracks","$total_tracks"]}
            }},
            {'$out': "artist_track_rating"}
        ]
        self.release_pipeline = [
            {'$group': {
                '_id': "$release.release-group.id",
                'name': {'$first': "$release.release-group.title"},
                'type': {'$first': "$release.release-group.type"},
                'release': {'$push': "$release"},
            }},
            {'$project': {
                "release.release-group": 0
            }},
            {'$unwind': "$release"},
            {'$lookup': {
                'from': "recording_with_rating",
                'localField': "release.id",
                'foreignField': "release_id",
                'as': "recording_data"
            }},
            {'$unwind': "$recording_data"},
            {'$group': {
                '_id': "$_id",
                'name': {'$first': "$name"},
                'type': {'$first': "$type"},
                'artist_id': {'$first': "$release.artist-credit.artist.id"},
                'artist_name': {'$first': "$release.artist-credit.artist.name"},
                'rating': {'$avg': "$recording_data.rating"},
                'stddev': {'$stdDevPop': "$recording_data.rating"},
                'total_tracks': {'$sum': 1},
                'rated_tracks': {'$push': "$recording_data.rating"},
            }},
            {'$project': {
                "name": 1,
                "type": 1,
                "artist_id": 1,
                "artist_name": 1,
                "rating": 1,
                "stddev": 1,
                "total_tracks": 1,
                "rated_tracks": {'$filter':{
                    'input': "$rated_tracks",
                    'cond': {'$ne':["$$this",None]}
                }}
            }},
            {'$project': {
                "name": 1,
                "type": 1,
                "artist_id": 1,
                "artist_name": 1,
                "rating": 1,
                "stddev": 1,
                "total_tracks": 1,
                "top_tracks": {'$filter':{
                    'input': "$rated_tracks",
                    'cond': {'$gte':["$$this",9]}
                }},
                "favorite_tracks": {'$filter':{
                    'input': "$rated_tracks",
                    'cond': {'$gte':["$$this",10]}
                }},
                "rated_tracks": {'$size': "$rated_tracks"}
            }},
            {'$project': {
                "name": 1,
                "type": 1,
                "artist_id": 1,
                "artist_name": 1,
                "rating": 1,
                "stddev": 1,
                "total_tracks": 1,
                "rated_tracks": 1,
                "top_tracks": {'$size': "$top_tracks"},
                "favorite_tracks": {'$size': "$favorite_tracks"},
                "percent_rated": {'$divide':["$rated_tracks","$total_tracks"]},
            }},
            {'$project': {
                "name": 1,
                "type": 1,
                "artist_id": 1,
                "artist_name": 1,
                "rating": 1,
                "stddev": 1,
                "total_tracks": 1,
                "rated_tracks": 1,
                "top_tracks": 1,
                "favorite_tracks": 1,
                "percent_rated": 1,
                "percent_top_tracks": {'$divide':["$top_tracks","$total_tracks"]}
            }},
            {'$out': "album_track_rating"}
        ]
        log.startLogging(sys.stdout)
        log.msg("Starting MpdParser with mode "+format(self.mode))
        self.mpdconnection = MpdConnection(
                args.ip, args.port,
                None, [self.dispatch], True, False)
        self.mongouri = "mongodb://"+self.args.mongoip+":"+self.args.mongoport
        self.mongo = txmongo.MongoConnection(host=self.args.mongoip,
                port=int(self.args.mongoport))
        log.msg("mongo at "+self.mongouri)

    def dispatch(self, conn):
        """Start the callback chain for each mode."""
        if 'artists' in self.mode:
            # if --artistid specified, operate only on that list
            if self.args.artistid:
                d = defer.Deferred()
                d.addCallback(partial(self.handle_list,'artist'))
                d.addErrback(log.err)
                d.callback(self.args.artistid.split(','))
            else:
                (self.mpdconnection.protocol.
                        list('musicbrainz_artistid').
                        addCallback(partial(self.handle_list,'artist')).
                        addErrback(log.err))
                self.mpdqueries += 1
        if 'releases' in self.mode:
            # if --releaseid specified, operate only on that list
            if self.args.releaseid:
                d = defer.Deferred()
                d.addCallback(partial(self.handle_list,'release'))
                d.addErrback(log.err)
                d.callback(self.args.releaseid.split(','))
            else:
                (self.mpdconnection.protocol.
                        list('musicbrainz_albumid').
                        addCallback(partial(self.handle_list,'release')).
                        addErrback(log.err))
                self.mpdqueries += 1
        if 'recordings' in self.mode:
            # if --recordingid specified, operate only on that list
            if self.args.recordingid:
                d = defer.Deferred()
                d.addCallback(partial(self.handle_list,'recording'))
                d.addErrback(log.err)
                d.callback(self.args.recordingid.split(','))
            else:
                (self.mpdconnection.protocol.
                        list('musicbrainz_trackid').
                        addCallback(partial(self.handle_list,'recording')).
                        addErrback(log.err))
                self.mpdqueries += 1
        if 'files' in self.mode:
            # if --songpath specified, operate only on that list
            if self.args.songpath:
                paths = self.args.songpath.split(',')
            else:
                paths = ['']
            for path in paths:
                log.msg("listallinfo '"+path+"'")
                (self.mpdconnection.protocol.
                        listallinfo(path).
                        addCallback(partial(self.handle_list,'file')).
                        addErrback(log.err))
                self.mpdqueries += 1
        if 'aggregate' in self.mode:
            self.waitleft += 1
            collection = self.mongo.music['recording']
            d = collection.aggregate(self.recording_pipeline)
            d.addCallback(self.apipe2)
            
    def apipe2(self, result):
        log.msg("recording pipeline results: "+str(result))
        collection = self.mongo.music['artist']
        d = collection.aggregate(self.artist_pipeline)
        d.addCallback(self.apipe3)
    
    def apipe3(self, result):
        log.msg("artist pipeline results: "+str(result))
        collection = self.mongo.music['release']
        d = collection.aggregate(self.release_pipeline)
        d.addCallback(self.apipe4)
    
    def apipe4(self, result):
        log.msg("release pipeline results: "+str(result))
        self.check_exit()

    def check_exit(self, *args):
        """Decrements the task counter, then exits if 0."""
        self.waitleft -= 1;
        log.msg("check_exit: "+str(self.waitleft)+" tasks left")
        if self.waitleft < 1:
            reactor.stop()

    def handle_list(self, qtype, result):
        """Parses the results of an mpd query and acts on it."""
        log.msg("handle_list: found "+qtype+" results")
        ulist = []
        for row in result:
            if qtype == 'file':
                if 'file' in row:
                    self.waitleft += 1
                    ulist.append((self.mpdconnection.protocol.
                            sticker_get('song', row['file'], 'rating').
                            addCallback(partial(
                                    self.write_mongo_file_data_with_sticker,
                                    row)).
                            addErrback(partial(
                                    self.write_mongo_file_data,
                                    row)).
                            addCallback(partial(
                                    self.handle_write_mongo_file_data,
                                    row)).
                            addErrback(log.err)))
                    self.mpdqueries += 1
            else:
                # MB tags can have more than one uuid separated by /
                for uuid in str(row).split('/'):
                    if len(uuid) > 0:
                        self.queue[qtype][uuid] = 1
        if qtype == 'file':
            self.waitleft +=1
            callbacks = defer.DeferredList(ulist)
            callbacks.addCallback(self.check_exit)
        else:
            self.waitleft += 1
            for uuid in self.queue[qtype].keys():
                ulist.append({"uuid":uuid,"qtype":qtype})
                self.waitleft += 1
            finished = self.parallel(ulist, 50, self.write_mongo_data)
            finished.addErrback(log.err)
            finished.addCallback(self.check_exit)
        # disconnect mpd after all queries are complete
        self.mpdqueries -= 1
        if self.mpdqueries < 1:
            self.mpdconnection.reactor.disconnect()
        # if we got all the way here and didn't do anything, we're done
        if self.waitleft == 0:
            self.check_exit()

    def parallel(self, iterable, count, callable, *args, **kwargs):
        # log.msg("parallel: "+format([iterable, count, callable, args, kwargs]))
        coop = task.Cooperator()
        work = (callable(elem, *args, **kwargs) for elem in iterable)
        return defer.DeferredList([coop.coiterate(work) for i in xrange(count)])

    def get_mb_cache(self, uuid, qtype):
        """Gets data object for an artist, recording, or release from
        cache and insert it into mongo."""
        mbpath = os.path.join(self.args.cachepath, qtype, Helpers.upath(uuid),
                uuid+'.json')
        data = {}
        with open(mbpath) as json_file:
            data = json.load(json_file)
        return data

    def write_mongo_data(self, elem):
        qtype = elem["qtype"]
        uuid = elem["uuid"]
        collection = self.mongo.music[qtype]
        data = self.get_mb_cache(uuid, qtype)
        d = collection.update(
                {qtype+".id":uuid},
                data,
                safe=True, upsert=True)
        d.addCallback(partial(self.handle_write_mongo_data, elem))
        return d

    def handle_write_mongo_data(self, elem, result):
        qtype = elem["qtype"]
        uuid = elem["uuid"]
        msg = u'Mongo data '
        if result['updatedExisting']:
            msg += u'updated '
        else:
            msg += u'added '
        msg += u'for '+qtype+" "+uuid
        log.msg(msg)
        self.check_exit()

    def write_mongo_file_data(self, data, result):
        filename = data['file']
        collection = self.mongo.music['file']
        d = collection.update(
                {"file":filename},
                data,
                safe=True, upsert=True)
        return d

    def write_mongo_file_data_with_sticker(self, data, result):
        rating = int(result)
        data['rating'] = rating
        return self.write_mongo_file_data(data, result)

    def handle_write_mongo_file_data(self, data, result):
        filename = data['file']
        msg = u'Mongo data '
        if result['updatedExisting']:
            msg += u'updated '
        else:
            msg += u'added '
        msg += u'for file '+filename
        log.msg(msg)
        self.check_exit()

def main_app():
    sys.stdout = sys.stderr = SmartStdout()
    set_defaultencoding_globally('utf-8')
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip",
            help="ip address or hostname of mpd server (default 127.0.0.1)",
            default="127.0.0.1")
    parser.add_argument("-p", "--port",
            help="port of mpd server (default 6600)",
            default="6600")
    parser.add_argument("-m", "--mongoip",
            help="ip address or hostname of mongo server (default 127.0.0.1)",
            default="127.0.0.1")
    parser.add_argument("-q", "--mongoport",
            help="port of mongo server (default 27017)",
            default="27017")
    # TODO: using ~ is not portable, but this app probably won't run on a
    # non-Unix-like OS anyway...
    parser.add_argument("-c", "--cachepath",
            help="directory to save mb cache (default ~/.kmpccache)",
            default=os.path.expanduser('~/.kmpccache'))
    parser.add_argument("--artists",
            help="scan artists", action="store_true")
    parser.add_argument("--releases",
            help="scan releases", action="store_true")
    parser.add_argument("--recordings",
            help="scan recordings", action="store_true")
    parser.add_argument("--files",
            help="scan files", action="store_true")
    parser.add_argument("--artistid",
            help="comma-delimited list of artistids to operate on")
    parser.add_argument("--releaseid",
            help="comma-delimited list of releaseids to operate on")
    parser.add_argument("--recordingid",
            help="comma-delimited list of recordingids to operate on")
    # TODO: this is broken on filenames that have a comma in them
    parser.add_argument("--songpath",
            help="comma-delimited list of songpaths to operate on")
    parser.add_argument("--aggregate", action="store_true",
            help="perform aggregation queries")
    args = parser.parse_args()
    print format(args)
    mpdparser = MpdParser(args)
    reactor.run()

if __name__ == "__main__":
    main_app()
