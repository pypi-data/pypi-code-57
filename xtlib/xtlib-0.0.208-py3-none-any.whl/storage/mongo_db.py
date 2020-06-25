#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# mongo_db.py: functions that read/write mongo_db data
import os
import sys
import time
import json
import copy
import arrow
import shutil
import numpy as np
import logging

from xtlib import utils
from xtlib import errors
from xtlib import constants
from xtlib import file_utils

from xtlib.console import console

logger = logging.getLogger(__name__)

MONGO_INFO = "__mongo_info__"

class MongoDB():
    '''
    We use MongoDB to provide fast query access to a large collection of run data.

    NOTE: *Every* underlying MongoDB operation should be wrapped with retryable code, since all sorts of general
    errors results from too much traffic can happen anywhere.

    Currently, we experience severe capacity problems running approx. 500 runs at once 
    (across all users on team).  We need to find a way to scale up to larger limits.
    '''
    def __init__(self, mongo_conn_str, run_cache_dir):
        if not mongo_conn_str:
            errors.internal_error("Cannot initialize MongoDB() with a empty mongo_conn_str")

        self.mongo_conn_str = mongo_conn_str
        self.run_cache_dir = run_cache_dir
        self.mongo_client = None
        self.mongo_db = None
        self.call_stats = {}

        # keep a count of how many retryable errors we have encountered
        self.retry_errors = 0

        self.run_cache_dir = os.path.expanduser(run_cache_dir) if run_cache_dir else None

        # initialize mondo-db now
        self.init_mongo_db_connection()

        # controls for mongo stats and logging
        self.update_job_stats = True
        self.update_run_stats = True
        self.add_log_records = True

    #---- UTILS ----

    def get_service_name(self):
        _, rest = self.mongo_conn_str.split("//", 1)
        if ":" in rest:
            name, _ = rest.split(":", 1)
        else:
            name, _ = rest.split("/", 1)

        return name
        
    def init_mongo_db_connection(self):
        ''' create mongo_db on-demand since it has some startup overhead (multiple threads, etc.)
        '''
        if not self.mongo_db:
            if self.mongo_conn_str:
                from pymongo import MongoClient

                self.mongo_client = MongoClient(self.mongo_conn_str)

                # this will create the mongo database called "xtdb", if needed
                self.mongo_db = self.mongo_client["xtdb"]

    def get_mongo_info(self):
        records = self.mongo_with_retries("get_mongo_info", lambda: self.mongo_db[MONGO_INFO].find({"_id": 1}, None), return_records=True)
        record = records[0] if records and len(records) else None
        return record

    def set_mongo_info(self, info): 
        self.mongo_with_retries("set_mongo_info", lambda: self.mongo_db[MONGO_INFO].update( {"_id": 1}, info, upsert=True) )
        
    def remove_workspace(self, ws_name):
        self.remove_cache(ws_name)

        # remove associated mongo_db container
        container = self.mongo_db[ws_name]

        self.mongo_with_retries("remove_workspace", lambda: container.drop())
        count = container.count()

        console.diag("  after mongo_db container={} dropped, count={}=".format(container, count))

        # remove counters for this workspace
        cmd = lambda: self.mongo_db.ws_counters.remove( {"_id": ws_name} )
        self.mongo_with_retries("remove_workspace", cmd, ignore_error=True)

        # remove legacy counters for this workspace
        end_id = ws_name + "-end_id"
        cmd = lambda: self.mongo_db.ws_counters.remove( {"_id": end_id} )
        self.mongo_with_retries("remove_workspace", cmd)

    def remove_cache(self, ws_name):
        # remove appropriate node of run_cache_dir
        if self.run_cache_dir:
            cache_fn = os.path.expanduser(self.run_cache_dir) + "/" + constants.RUN_SUMMARY_CACHE_FN
            cache_fn = cache_fn.replace("$ws", ws_name)
            cache_dir = os.path.dirname(cache_fn)

            if os.path.exists(cache_dir):
                console.print("  zapping cache_dir=", cache_dir)
                file_utils.zap_dir(cache_dir)

    def init_workspace_counters(self, ws_name, next_run, next_end):
        update_doc = { "_id": ws_name, "next_run": next_run, "next_end": next_end, "next_child" : {} }

        cmd = lambda: self.mongo_db.ws_counters.find_and_modify( {"_id": ws_name}, update=update_doc, upsert=True)
        self.mongo_with_retries("init_workspace_counters", cmd)

    def get_workspace_names(self):
        db = self.mongo_db
        records = self.mongo_with_retries("get_workspace_names", lambda: db.ws_counters.find(None, {"_id": 1}), return_records=True)
        names = [rec["_id"] for rec in records if rec["_id"] != "__jobs__"]
        return names

    def get_next_sequential_job_id(self, default_next):
        job_ws = "__jobs__"
        path = "next_job"

        db = self.mongo_db

        # does a counters doc exit for this ws_name?
        records = self.mongo_with_retries("get_next_sequential_job_id", lambda: db.ws_counters.find({"_id": job_ws}).limit(1), return_records=True)
        if not records:
            self.mongo_with_retries("get_next_sequential_job_id", lambda: db.ws_counters.insert_one( {"_id": job_ws, path: default_next} ))

        document = self.mongo_with_retries("get_next_sequential_job_id", lambda: \
                db.ws_counters.find_and_modify( {"_id": job_ws}, update={"$inc": {path: 1} }, new=False))

        next_id = document[path]
        return next_id

    def get_legacy_end_id(self, ws_name):
        db = self.mongo_db
        doc_id = ws_name + "-end_id"
        records = self.mongo_with_retries("get_legacy_end_id", lambda: db.ws_counters.find({"_id": doc_id}).limit(1), return_records=True)
        last_id = utils.safe_cursor_value(records, "last_id")
        return last_id

    def get_next_sequential_ws_id(self, ws_name, path, default_next_run):
        db = self.mongo_db

        assert not "/" in ws_name 
        assert not "/" in path 
        
        console.diag("ws={}, path={}, default_next_run={}".format(ws_name, path, default_next_run))

        # does a counters doc exist for this ws_name?
        records = self.mongo_with_retries("get_next_sequential_ws_id", lambda: db.ws_counters.find({"_id": ws_name}).limit(1), return_records=True)
        if not records:
            console.diag("LEGACY ws={} found in get_next_sequential_ws_id".format(ws_name))

            # we need BOTH next_run and next_end for a new record 
            last_id = self.get_legacy_end_id(ws_name)
            default_next_end = 1 + last_id if last_id else 1

            info = {"_id": ws_name, "next_run": default_next_run, "next_end": default_next_end, "next_child": {}}
            self.mongo_with_retries("get_next_sequential_ws_id", lambda: db.ws_counters.insert_one( info ))

        document = self.mongo_with_retries("get_next_sequential_ws_id", lambda: \
            db.ws_counters.find_and_modify( {"_id": ws_name}, update={"$inc": {path: 1} }, new=False))

        next_id = utils.safe_nested_value(document, path)

        if not next_id:
            # child id's start at 0; if we got that, skip it and get next one
            document = self.mongo_with_retries("get_next_sequential_ws_id", lambda: \
                db.ws_counters.find_and_modify( {"_id": ws_name}, update={"$inc": {path: 1} }, new=False))
            next_id = utils.safe_nested_value(document, path)
     
        return next_id

    def get_next_job_id(self, default_next=1):
        return self.get_next_sequential_job_id(default_next)

    def get_next_run_id(self, ws_name, default_next=1):
        return self.get_next_sequential_ws_id(ws_name, "next_run", default_next)

    def get_next_child_id(self, ws_name, run_name, default_next=1):
        return self.get_next_sequential_ws_id(ws_name, "next_child." + run_name, default_next)

    def get_next_end_id(self, ws_name, default_next_run=1):
        return self.get_next_sequential_ws_id(ws_name, "next_end", default_next_run)

    def mongo_with_retries(self, name, mongo_cmd, ignore_error=False, return_records=False):
        import pymongo.errors

        retry_count = 25
        result = None
        started = time.time()

        for i in range(retry_count):
            try:
                result = mongo_cmd()

                # most of the time, we want to ALSO want to retry building a record set from the cursor
                if return_records:
                    result = list(result) if result else []
                break
            # watch out for these exceptions: AutoReconnect, OperationFailure (and ???)
            except BaseException as ex:   # pymongo.errors.OperationFailure as ex:
                
                # this is to help us debug situations where we raise the exception without ever printing retry msgs
                print("got exception in mongo, i={}, retry_count={}, caller={}".format(i, retry_count, name), flush=True)

                # since we cannot config logger to supress stderr, don't log this
                #logger.exception("Error in mongo_with_retries, ex={}".format(ex))
                
                # pymongo.errors.OperationFailure: Message: {"Errors":["Request rate is large"]}
                if ignore_error:
                    console.print("ignoring mongo-db error: name={}, ex={}".format(name, ex))
                    break
                
                if i == retry_count-1:
                    # we couldn't recover - signal a hard error/failure
                    raise ex

                # we get hit hard on the "Request rate is large" errors when running 
                # large jobs (500 simultaneous runs), so beef up the backoff times to
                # [1,61] so we don't die with a hard failure here
                if i == 0:
                    backoff = 1 + 10*np.random.random()
                    self.retry_errors += 1
                else:
                    backoff = 1 + 60*np.random.random()

                ex_code = ex.code if hasattr(ex, "code") else ""
                ex_msg = str(ex)[0:60]+"..."

                console.print("retrying mongo-db: name={}, retry={}/{}, backoff={:.2f}, ex.code={}, ex.msg={}".format(name, i+1, retry_count, backoff, 
                    ex_code, ex_msg))
                    
                time.sleep(backoff)
                
        # track all mongo calls stats
        elapsed = time.time() - started

        if not name in self.call_stats:
            self.call_stats[name] = []
        self.call_stats[name].append(elapsed)

        #print("--> mongo call: {} (elapsed: {:.4f} secs)".format(name, elapsed))
        return result

    def print_call_stats(self):
        total_count = 0
        total_time = 0
        total_calls = 0

        for name, stats in self.call_stats.items():
            mean = np.mean(stats)
            print("  {}x {}: avg={:.4f}".format(len(stats), name, mean))

            total_calls += len(stats)
            total_time += np.sum(stats)
            total_count += 1

        print()
        print("  {}x {}: total={:.4f} secs".format(total_calls, "CALLS", total_time))
        print()

    #---- RUNS ----

    def create_mongo_run(self, dd):
        # create run document on Mongo DB
        # copy standard CREATE properties
        run_doc = copy.deepcopy(dd)

        # zap a few we don't want
        if "event" in run_doc:
            del run_doc["event"]

        if "time" in run_doc:
            del run_doc["time"]

        # add some new ones
        is_azure = utils.is_azure_batch_box(dd["box_name"])

        run_doc["_id"] = dd["run_name"]
        run_doc["status"] = "allocating" if is_azure else "created"
        run_doc["duration"] = 0
        
        # add the new RUN document
        ws_name = dd["ws"]

        cmd = lambda: self.mongo_db[ws_name].insert_one(run_doc)
        self.mongo_with_retries("create_mongo_run", cmd, ignore_error=True)

    def add_run_event(self, ws_name, run_name, log_record):

        if self.add_log_records:
            # first, add log record to ws/run document
            update_doc = { "$push": {"log_records": log_record} }
            self.mongo_with_retries("add_run_event", lambda: self.mongo_db[ws_name].update_one( {"_id": run_name}, update_doc, upsert=True) )

        if self.update_run_stats:
            event_name = log_record["event"]
            data_dict = log_record["data"]
            updates = {}

            if event_name == "hparams":
                # create a "hparams" dict property for the run record
                self.flatten_dict_update(updates, "hparams", data_dict)
                self.update_mongo_run_from_dict(ws_name, run_name, updates)

            elif event_name == "metrics":
                # create a "metrics" dict property for the run record (most recent metrics)
                self.flatten_dict_update(updates, "metrics", data_dict)
                self.update_mongo_run_from_dict(ws_name, run_name, updates)

            if event_name == "started":
                updates = { "status": "running" }
                #console.print("updating run STATUS=", updates)
                self.update_mongo_run_from_dict(ws_name, run_name, updates)

            elif event_name == "status-change":
                updates = { "status": data_dict["status"] }
                #console.print("updating run STATUS=", updates)
                self.update_mongo_run_from_dict(ws_name, run_name, updates)

    def flatten_dict_update(self, updates, dd_name, dd):
        for key, value in dd.items():
            updates[dd_name + "." + key] = value

    def update_mongo_run_at_end(self, ws_name, run_name, status, exit_code, restarts, end_time, log_records, hparams, metrics):
        # update run document on Mongo DB

        if self.update_run_stats:
            # update properties
            updates = {}
            updates["status"] = status
            updates["exit_code"] = exit_code
            updates["restarts"] = restarts
            updates["end_time"] = end_time

            # add the unique end_id (relative to ws_name)
            updates["end_id"] = self.get_next_end_id(ws_name)

            # structured properties
            if hparams:
                #updates["hparams"] = hparams
                self.flatten_dict_update(updates, "hparams", hparams)

            if metrics:
                #updates["metrics"] = metrics
                self.flatten_dict_update(updates, "metrics", metrics)
            
            # no longer need this step here (log records are now appended as they are logged)
            #updates["log_records"] = log_records

            self.update_mongo_run_from_dict(ws_name, run_name, updates)

    def update_mongo_run_from_dict(self, ws_name, run_name, dd):
        #console.print("update_mongo_run_from_dict: ws_name={}, run_name={}, dd={}".format(ws_name, run_name, dd))

        if self.update_run_stats:
            update_dd = copy.deepcopy(dd)
            update_dd["last_time"] = utils.get_time()

            update_doc = { "$set": update_dd}

            #console.print("update_mongo_run_from_dict: ws_name={}, run_name={}, update_doc={}".format(ws_name, run_name, update_doc))

            # do a REPLACE DOC update operation
            self.mongo_with_retries("update_mongo_run_from_dict", lambda: self.mongo_db[ws_name].update_one( {"_id": run_name}, update_doc) )

    def does_run_exist(self, ws, run_name):
        records = self.get_info_for_runs(ws, {"_id": run_name}, {"_id": 1})
        exists = len(records) == 1
        return exists

    def get_info_for_runs(self, ws_name, filter_dict, fields_dict=None):

        # filter_dict = {}
        # filter_dict["run_name"] = {"$in": run_names}

        run_records = self.mongo_with_retries("get_boxes_for_runs", lambda: self.mongo_db[ws_name].find(filter_dict, fields_dict), return_records=True)

        console.diag("after get_boxes_for_runs()")        
        return run_records

    def get_all_experiments_in_ws(self, ws_name):
        # cannot get "distinct" command to work ("command not supported")
        #cursor = db["__jobs__"].distinct("ws_name") 

        records = self.mongo_with_retries("get_all_experiments_in_ws", lambda: self.mongo_db["__jobs__"].find({"ws_name": ws_name}, {"exper_name": 1}), 
            return_records=True)

        exper_names = [rec["exper_name"] for rec in records if "exper_name" in rec]
        exper_names = list(set(exper_names))   # remove dups

        console.diag("after get_all_experiments()")        
        return exper_names

    def get_ws_runs(self, ws_name, filter_dict=None, include_log_records=False, first_count=None, last_count=None, sort_dict=None):
        '''
        design issue: we cannot use a single cache file for different filter requests.  Possible fixes:
            - do not cache here (current option)
            - name cache by filter settings (one cache file per setting) - not ideal
            - keep all runs for ws in cache and apply filter locally (TODO: this option)
        '''
        if include_log_records:
            fields_dict = None   # all fields, including log_records
            fn_cache = self.run_cache_dir + "/" + constants.ALL_RUNS_CACHE_FN
        else:
            fields_dict = {"log_records": 0}
            fn_cache = self.run_cache_dir + "/" + constants.RUN_SUMMARY_CACHE_FN

        fn_cache = fn_cache.replace("$aggregator", ws_name)

        return self.get_all_runs(None, ws_name, None, filter_dict, fields_dict, use_cache=False, fn_cache=fn_cache, first_count=first_count, 
            last_count=last_count, sort_dict=sort_dict)

    def get_all_runs(self, aggregator_dest, ws_name, job_or_exper_name, filter_dict=None, fields_dict=None, use_cache=True, 
        fn_cache=None, first_count=None, last_count=None, sort_dict=None, batch_size=None):
        '''
        cache design: 
            - organized all cached run information by the way it was accessed: a folder for each workspace (created on demand), 
              and under each, a folder specifying the filter_dict and fields_dict.  This way, we only use cache records for
              exactly matching query info.

            - whenever sort, first_count, or last_count is used (that is, included in the mongo db query), we should set "use_cache" to False.

            - note: since Azure Cosmos version of mongo-db doesn't correctly support sort/first/last (totally busted as of Aug 2019), we never
              include sort/first/last in mongo db query.

            - as of 12/20/2019, the only code that correctly uses the fn_cache is hparam_search.  all other code should call with use_cache=False.
        '''
        # PERF-critical function 
        # below code not yet cache-compliant
        use_cache = False

        records = []
        target = 0
        cache = None

        if use_cache and not fn_cache:
            # fn_cache = self.run_cache_dir + "/" + constants.ALL_RUNS_CACHE_FN
            # fn_cache = fn_cache.replace("$aggregator", ws_name)
            use_cache = False      # play it safe for now

        if use_cache and os.path.exists(fn_cache):
            # read CACHED runs
            started = time.time()
            cache = utils.load(fn_cache)
            elapsed = time.time() - started

            target = max([rec["end_id"] if "end_id" in rec else 0 for rec in cache])
            console.print("loaded {:,} records in {:.2f} secs from cache: {}".format(len(cache), elapsed, fn_cache))

        if not filter_dict:
            if aggregator_dest == "job":
                filter_dict = {"job_id": job_or_exper_name}
            elif aggregator_dest == "experiment":
                filter_dict = {"exper_name": job_or_exper_name}

        # if not fields_dict:
        #     # by default, do NOT return inner log records
        #     fields_dict = {"log_records": 0}

        # adjust filter to get only missing records
        if target:
            filter_dict["end_id"] = {"$gt": target}

        #console.print("  mongo: filter: {}, fields: {}, sort: {}".format(filter_dict, fields_dict, sort_dict))
        console.diag("  mongo: filter: {}, fields: {}".format(filter_dict, fields_dict))

        #records = self.mongo_db[ws_name].find(filter_dict, fields_dict)  
        def cmd_func():
            started = time.time()
    
            cursor = self.mongo_db[ws_name].find(filter_dict, fields_dict)

            #avail = cursor.count()

            # break query into multiple calls to avoid "message max exceeded" errors
            if batch_size:
                cursor = cursor.batch_size(batch_size)

            records = list(cursor)

            if console.level in ["diagnostics", "detail"]:
                elapsed = time.time() - started
                total_count = self.mongo_db[ws_name].count()
                console.diag("  mongo query returned {} records (of {}), took: {:2f} secs".format(len(return_count), total_count, elapsed))

            #explanation = cursor.explain()

            return records

        records = self.mongo_with_retries("get_all_runs", cmd_func)
        return_count = len(records)

        if cache:
            cache += records
            records = cache

        if return_count and use_cache:
            # write to cache 
            started = time.time()
            utils.save(records, fn_cache)
            elapsed = time.time() - started
            console.print("wrote {:,} records to cache, took: {:2f} secs".format(len(records), elapsed))

        return records

    def update_run_info(self, ws_name, run_id, dd, clear=False, upsert=True):

        if self.update_run_stats:
            if clear:
                update_doc = { "$unset": dd}
            else:
                update_doc = { "$set": dd}

            # update, create prop if needed
            self.mongo_with_retries("update_run_info", lambda: self.mongo_db[ws_name].update_one( {"_id": run_id}, update_doc, upsert=upsert) )

    def update_runs_from_filter(self, ws_name, filter, dd, clear=False, upsert=True):

        if self.update_run_stats:
            if clear:
                update_doc = { "$unset": dd}
            else:
                update_doc = { "$set": dd}

            # update, create prop if needed
            result = self.mongo_with_retries("update_runs_from_filter", lambda: self.mongo_db[ws_name].update_many( filter, update_doc, upsert=upsert) )
            return result

    #---- JOBS ----

    def does_jobs_exist(self):
        # does document for ws_name exist?
        job_id = "job1"
        cmd = lambda: self.mongo_db["__jobs__"].find({"_id": job_id}, {"_id": 1}).limit(1)
        records = self.mongo_with_retries("does_jobs_exist", cmd, return_records=True)
        found = len(records) > 0

        return found

    def get_info_for_jobs(self, filter_dict, fields_dict=None):

        job_records = self.mongo_with_retries("get_info_for_jobs", lambda: self.mongo_db["__jobs__"].find(filter_dict, fields_dict), return_records=True)

        console.diag("after get_info_for_jobs()")        
        return job_records

    def update_job_info(self, job_id, dd, clear=False, upsert=True):

        if self.update_job_stats:
            if clear:
                update_doc = { "$unset": dd}
            else:
                update_doc = { "$set": dd}

            # update, create if needed
            self.mongo_with_retries("update_job_info", lambda: self.mongo_db["__jobs__"].update_one( {"_id": job_id}, update_doc, upsert=upsert) )

    def get_job_names(self, filter_dict=None):
        job_names = []
        fields_dict = {"_id": 1}
        
        cmd_func = lambda: self.mongo_db["__jobs__"].find(filter_dict, fields_dict)
        jobs = self.mongo_with_retries("get_job_names", cmd_func, return_records=True)
        if jobs:
            # filter out just the names
            job_names = [ job["_id"] for job in jobs]

        return job_names

    def get_job_workspace(self, job_id):
        ''' returns name of workspace associated with job'''
        ws_name = None

        # does document for ws_name exist?
        cmd = lambda: self.mongo_db["__jobs__"].find({"_id": job_id}, {"ws_name": 1}).limit(1)
        records = self.mongo_with_retries("get_job_workspace", cmd, return_records=True)

        if records:
            result = records[0]
            if "ws_name" in result:
                ws_name = result["ws_name"]

        return ws_name

    def job_node_start(self, job_id):
        '''
        A job's node has started running.  We need to:
            - increment the job's "running_nodes" property
            - set the "job_status" property to "running"
        '''
        if self.update_job_stats:
            cmd = lambda: self.mongo_db["__jobs__"].find_and_modify( {"_id": job_id}, update={"$inc": {"running_nodes": 1} })
            self.mongo_with_retries("job_node_start", cmd)

            cmd = lambda: self.mongo_db["__jobs__"].find_and_modify( {"_id": job_id}, update={"$set": {"job_status": "running"} })
            self.mongo_with_retries("job_node_start", cmd)

    def job_node_exit(self, job_id):
        '''
        A job's node has finished running.  We need to:
            - decrement the job's "running_nodes" property 
            - if running_nodes==0, set the "job_status" property to "completed"
        '''
        if self.update_job_stats:
            cmd = lambda: self.mongo_db["__jobs__"].find_and_modify( {"_id": job_id}, update={"$inc": {"running_nodes": -1} })
            self.mongo_with_retries("job_node_exit", cmd)

            cmd = lambda: self.mongo_db["__jobs__"].find_and_modify( {"_id": job_id, "running_nodes": 0}, update={"$set": {"job_status": "completed"} })
            self.mongo_with_retries("job_node_exit", cmd)

    def update_connect_info_by_node(self, job_id, node_id, connect_info):
        key = "connect_info_by_node." + node_id
        update_doc = { "$set": {key: connect_info} }
        self.mongo_with_retries("update_connect_info_by_node", lambda: self.mongo_db["__jobs__"].update_one( {"_id": job_id}, update_doc) )

    def job_run_start(self, job_id):
        '''
        A job's run has started running.  We need to:
            - increment the job's "running_runs" property 
        '''
        if self.update_job_stats:
            cmd = lambda: self.mongo_db["__jobs__"].find_and_modify( {"_id": job_id}, update={"$inc": {"running_runs": 1} })
            self.mongo_with_retries("job_run_start", cmd)

    def job_run_exit(self, job_id, exit_code):
        '''
        A job's run has finished running.  We need to:
            - decrement the job's "running_runs" property 
            - increment the job's "completed_runs" property
            - if exit_code != 0, increment the job's "error_runs" property
        '''
        if self.update_job_stats:
            error_inc = 1 if exit_code else 0
            cmd = lambda: self.mongo_db["__jobs__"].find_and_modify( {"_id": job_id}, update={"$inc": {"running_runs": -1, "completed_runs": 1, "error_runs": error_inc} })
            self.mongo_with_retries("job_run_exit", cmd)

    def run_start(self, ws_name, run_name):
        '''
        A run has started running.  We need to:
            - set the run "start_time" property to NOW
            - set the run "queue_duration" property to NOW - created_time
        '''
        if self.update_run_stats:
            now = arrow.now()
            now_str = str(now)

            # get create_time of run
            cmd = lambda: self.mongo_db[ws_name].find({"_id": run_name}, {"create_time": 1})
            records = self.mongo_with_retries("run_start", cmd, return_records=True)

            doc = records[0] if records else None
            if doc and "create_time" in doc:
                create_time_str = doc["create_time"]
                create_time = arrow.get(create_time_str)

                # compute time in "queue" 
                queue_duration = utils.time_diff(now, create_time)

                cmd = lambda: self.mongo_db[ws_name].find_and_modify( {"_id": run_name}, update={"$set": {"start_time": now_str, "queue_duration": queue_duration} })
                self.mongo_with_retries("run_start", cmd)

    def run_exit(self, ws_name, run_name):
        '''
        A run has finished running.  We need to:
            - set the run "run_duration" property to NOW - start_time
        '''
        if self.update_run_stats:
            now = arrow.now()
            now_str = str(now)

            # get start_time of run
            cmd = lambda: self.mongo_db[ws_name].find({"_id": run_name}, {"start_time": 1})
            records = self.mongo_with_retries("run_exit #1", cmd, return_records=True)

            doc = records[0] if records else None
            if doc and "start_time" in doc:
                start_time_str = doc["start_time"]
                start_time = arrow.get(start_time_str)

                # compute run_duration 
                run_duration = utils.time_diff(now, start_time)

                cmd = lambda: self.mongo_db[ws_name].find_and_modify( {"_id": run_name}, update={"$set": {"run_duration": run_duration} })
                self.mongo_with_retries("run_exit #2", cmd)
