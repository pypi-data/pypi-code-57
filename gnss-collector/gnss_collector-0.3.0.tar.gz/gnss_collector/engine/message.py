import asyncio
from networktools.time import timestamp
from orm_collector.manager import SessionCollector, object_as_dict
import ujson as json
from networktools.colorprint import gprint, bprint, rprint
from basic_queuetools.queue import read_queue_gen
from .conf.settings import COMMANDS, groups, dirs


class MessageManager:
    def __init__(self, engine, *args, **kwargs):
        self.engine = engine
        self.commands = COMMANDS
        self.msg_process = dict(
            ADD_STA=self.recv_add_sta,
            ADD_DATADB=self.recv_add_datadb,
            INIT_VAR=self.recv_init_var,
            GET_CMD=self.recv_get_cmd,
            GET_INFO=self.recv_get_info,
            GET_LST=self.recv_get_lst,
            UPD_STA=self.recv_upd_sta,
            UPD_DATADB=self.recv_upd_datadb,
            SAVE_DB=self.recv_save_db,
            UPD_DB=self.recv_upd_db,
            GET_DB=self.recv_get_db,
            DEL_DB=self.recv_del_db,
            COLLECT_STA=self.recv_collect_sta,
            STOP_STA=self.recv_stop_sta,
            END=self.recv_end
        )

    async def recv_add_sta(self, idx, cmd):
        """
        Add a new station to list
        """
        c_key = 'ADD_STA'
        # Loads station dictionary
        args = cmd.get('command', {}).get('args')
        # add station
        ans = ''
        try:
            for item in args:
                station_data = item.get('station')
                (ids, sta) = self.engine.add_station(**station_data)
                # SEND MSG STA [CODE] ADDED
                dbdata_data = item.get('dbdata')
                type_name = dbdata_data.get('type_name', 'RethinkDB')
                (idb, db) = self.engine.new_datadb(type_name, **dbdata_data)
                ans = dict(
                    zip(
                        ('ids', 'idb', 'idm'),
                        (ids, idb, idx)))
                if not item.get('test', True):
                    # save data on database
                    id_db = self.engine.save_db(
                        None, 'dbdata', dbdata_data)
                    id_sta = self.engine.save_db(
                        None, 'station', station_data)
                    id_data = {'station': id_sta,
                               'dbdata': id_db}
                    ans.update({'id_data': id_data})
        except Exception as ex:
            ans = 'NO_ADDED %s' % ex
        cmd['command'].update({'args': [], 'answer': ans})
        rprint("=====SENDING ANSWER=====")
        bprint(cmd)
        return cmd

    async def recv_add_datadb(self, idx, cmd):
        """
        Add a DBTYPE for store data collected
        """
        c_key = 'ADD_DATADB'
        dbtype = cmd.get('dbtype')
        args = cmd.get('args')
        try:
            idd = self.engine.new_datadb(dbtype, **args)
            ans = 'ADDED %s' % idd
        except Exception as exec:
            ans = 'NOT_ADDED'
        cmd['command'].update({'answer': [ans]})
        return cmd

    async def recv_init_var(self, idx, cmd):
        c_key = 'INIT_VAR'
        varname = cmd.get('varname')
        idv = cmd.get('id')
        queue = self.engine.queue_process
        ans_queue = self.engine.queue_ans_process
        ans = ''
        if varname == 'STATION':
            q = 0
            queue.put(idv)
            if not ans_queue.empty():
                for i in range(ans_queue.qsize()):
                    ans = ans_queue.get()
        elif varname == 'DATABASE':
            pass
        cmd['command'].update({'answer': ans})
        return cmd

    def get_cmd(self):
        cmd = self.commands
        cmd_str = json.dumps(cmd)
        return cmd_str

    async def recv_get_cmd(self, idm, cmd):
        """
        Send the COMMANDS list to user
        """
        c_key = 'GET_CMD'
        ans = ''
        try:
            ans = self.get_cmd()
        except:
            ans = ['NO_E_CMDLST']
        cmd['command'].update({'answer': ans})
        return cmd

    async def recv_get_info(self, idm, cmd):
        """
        Send a bit of information required
        """
        c_key = 'GET_INFO'
        varname = cmd.get('varname')
        idx = cmd.get('idx')
        ans = ''
        try:
            if varname == 'STA' or varname == 'STATIONS':
                if idx in self.stations.keys():
                    ans = self.stations[idx]
                    status = self.status_task[idx]
                    ans['STATUS'] = status
                else:
                    ans = "There are no station with %s" % idx

            elif varname == 'DB' or varname == 'DBDATA':
                if idx in self.db_data.keys():
                    ans = self.db_data[idx]
                else:
                    ans = "There are no dbdata with %s id" % idx
        except:
            ans = 'NO_IDX_IN_VARNAME'
        cmd['command'].update({'answer': ans})
        return cmd

    async def recv_get_lst(self, idm,  msg):
        """
        Send some list, the varname could be:
        [VARNAME]=
        {
        IDS --> Engine.ids
        IDD --> Engine.idd
        INST --> self.instances.keys())
        DB_INST --> self.db_instances.keys() <-mustb be copy from
        DB_INST_STA --> self.db_instaces[key] for all
        PROT --> self.collect_objects.keys()
        STA --> self.stations
        DB -_> self.dbdata
        STATUS_STA --> self.status_sta
        FIRST_TIME --> self.first_time

        }
        """
        rprint("msg in to get list-> %s" % msg)
        c_key = 'GET_LST'
        command = msg.get('command').get('action')
        varname = msg.get('command').get('varname')
        args = msg.get('args', [])
        kwargs = msg.get('kwargs', {})
        varlist = ''
        dump_list = dict(
            IDS=self.dumps_ids,
            IDD=self.dumps_idd,
            IPT=self.dumps_ipt,
            IDM=self.dumps_idm,
            INST=self.dumps_inst,
            DB_INST=self.dumps_db_inst,
            DB_INST_STA=self.dumps_db_inst_sta,
            PROTOCOL=self.dumps_prot,
            STATION=self.dumps_sta,
            DBDATA=self.dumps_db_data,
            DBTYPE=self.dumps_db_type,
            STATUS_STA=self.dumps_status_sta,
            FIRST_TIME=self.dumps_first_time
        )
        try:
            if varname in dump_list:
                varlist = dump_list.get(varname)(*args)
                rprint("Varlist result--->%s" % varlist)
                msg.get('command').update({'answer': varlist})
            else:
                msg.get('command').update({'answer': []})
        except Exception as exec:
            print(exec)
            ans = 'NO_LIST'
            msg.get('command').update({'answer': []})
        return msg

    def dumps_ids(self):
        return self.ids

    def dumps_idd(self):
        return self.idd

    def dumps_ipt(self):
        return self.ipt

    def dumps_idm(self):
        return self.idm
    # IPT,IDM...

    def dumps_inst(self):
        return list(self.instances.keys())

    def dumps_db_inst(self):
        return list(self.db_instances.keys())

    def dumps_db_inst_sta(self):
        return list(self.db_instances_sta.keys())

    def dumps_db_data(self):
        return self.engine.db_data._getvalue()

    def dumps_db_type(self):
        return self.engine.db_type._getvalue()

    def dumps_prot(self):
        return list(self.collect_objects.keys())

    def dumps_sta(self):
        return self.engine.stations._getvalue()

    def dumps_dbtype(self):
        return self.engine.db_types._getvalue()

    def dumps_status_sta(self):
        return self.status_sta._getvalue()

    def dumps_first_time(self):
        return self.first_time

    async def recv_upd_sta(self, idx, cmd):
        c_key = 'UPD_STA'
        ids = cmd.get('ids')
        key = cmd.get('key')
        value = cmd.get('value')
        ans = ''
        try:
            if key in self.engine.stations[ids]:
                this_type = type(self.db_data[ids][key])
                this_value = this_type(value)
                self.engine.stations[ids][key] = this_value
            ans = 'UPDATED'
        except:
            ans = 'KEY_ERROR'
        cmd['command'].update({'answer': ans})
        return cmd

    async def recv_upd_datadb(self, idm, cmd):
        """
        Update some key-value on database
        """
        c_key = 'UPD_DATADB'
        idd = cmd.get('idd')
        key = cmd.get('key')
        value = cmd.get('value')
        ans = ''
        try:
            # cancel instance idd
            # stop collect data from stations ligated to idd
            # delete idd instance
            if key in self.db_data[idd]:
                this_type = type(self.db_data[idd][key])
                this_value = this_type(value)
                self.db_data[idd][key] = this_value
            ans = 'UPDATED_DB key:%s, value: %s' % (key, this_value)
        except Exception as ex:
            ans = 'ERROR'
        cmd['command'].update({'answer': ans})
        return cmd

    async def recv_save_db(self, idx, cmd):
        """
        Save data from station [STA] or [DB]
        """
        c_key = 'SAVE_DB'
        varname = cmd.get('varname')
        option = cmd.get('option')
        result = []
        vardata = object
        idv_list = []
        ans = dict()
        if varname == 'STATION':
            vardata = self.stations
        elif varname == 'DBDATA':
            vardata = self.db_data
        if option == 'ONE':
            idv_list = cmd.get('ids')
        elif option == 'GROUP':
            idv_list = cmd.get('ids')
        elif option == 'ALL':
            idv_list = list(vardata.keys())
        else:
            idv_list = 'NOIDS'

        tname = self.get_tname(varname)

        dbmanager = None
        for idv in idv_list:
            # save vardata
            try:
                args = []
                if varname == 'DBDATA':
                    args = vardata[idv]['args']
                elif varname == 'PROTOCOL':
                    args = vardata[idv]['args']
                elif varname == 'DBTYPE':
                    args = vardata[idv]['args']
                elif varname == 'STATION':
                    args = vardata[idv]
                dbmanager = self.save_db(dbmanager, tname, args)
                ans[idv] = 'OK'
            except Exception as exec:
                print(exec)
                raise exec
                ans[idv] = 'NO %s' % exec
        cmd['command'].update({'answer': ans})
        return cmd

    async def recv_upd_db(self, idx, cmd):
        """
        Update some data on database
        """
        c_key = 'UPD_DB'

        varname = cmd.get('command').get('action')
        idv = cmd.get('command').get('id')
        new_dict = cmd.get('args')

        result = []
        vardata = object

        idv_list = []

        ans = 'OK'

        if varname == 'STATION':
            vardata = self.stations[idv]
            for k in new_dict.keys():
                if k in vardata.keys():
                    vardata[k] = new_dict[k]
            self.stations[idv] = vardata

        elif varname == 'DBDATA':
            vardata = self.db_data[idv]
            for k in new_dict.keys():
                if k == 'name':
                    vardata['name'] = new_dict[k]
                else:
                    vardata['args'][k] = new_dict[k]
            self.db_data[idv] = vardata

        # TO DO:
        elif varname == 'DBTYPE':
            vardata = self.dbtype[idv]
            for k in new_dict.keys():
                if k == 'name':
                    vardata['name'] = new_dict[k]
                else:
                    vardata['args'][k] = new_dict[k]
            self.db_data[idv] = vardata

        elif varname == 'PROTOCOL':
            vardata = self.protocol[idv]
            for k in new_dict.keys():
                if k == 'name':
                    vardata['name'] = new_dict[k]
                else:
                    vardata['args'][k] = new_dict[k]
            self.db_data[idv] = vardata

        tname = self.get_tname(varname)

        try:
            self.update_db(tname, idv)
            ans = 'OK UPDATED %s, now restart data collect for this relationship' % idv
        except Exception as exec:
            print(exec)
            ans = 'NO UPDATED %s, exception  %s' % (idv, exec)
        cmd['command'].update({'answer': ans})
        return cmd

    def update_db(self, tname, idv):
        dbmanager = SessionCollector()
        if tname == 'station':
            # new data
            station = self.stations[idv]
            # obtain data from database
            inst_station = dbmanager.station(**station)
            # update on database
            dbmanager.update_station(inst_station, station)
        elif tname == 'database':
            # new data
            dbdata = self.dbdata[idv]['args']
            # obtain data from database
            inst_dbdata = dbmanager.dbdata(**dbdata)
            # update on database
            dbmanager.update_dbdata(inst_dbdata, dbdata)
        elif tname == 'dbtype':
            dbtype = self.dbtype[idv]['args']
            # obtain data from database
            inst_dbtype = dbmanager.dbtype(**dbtype)
            dbtype.update_dbtype(inst_dbtype, dbtype)
        elif tname == 'protocol':
            protocol = self.protocol[idv]['args']
            # obtain data from database
            inst_protocol = dbmanager.protocol(**protocol)
            dbtype.update_dbtype(inst_protocol, protocol)

    async def recv_get_db(self, idx, cmd):
        """
        Get some info from database
        """
        c_key = 'GET_DB_LST'
        tname = self.get_tname(cmd.get('table_name'))
        (session, queryset) = self.get_db(tname)
        # queryset yo dict
        # table_list=dict(zip(queryset.keys(), queryset))
        table = []
        for u in queryset:
            this_object = object_as_dict(u)
            if tname == 'station':
                position = u.get_position()
                this_object['position'] = format(position)
            table.append(this_object)
        cmd['command'].update({'answer': table})
        return cmd

    def get_db(self, tname):
        dbmanager = SessionCollector()
        if tname == 'station':
            return (dbmanager, dbmanager.get_stations())
        elif tname == 'database':
            return (dbmanager, dbmanager.get_dbdatas())
        elif tname == 'protocol':
            return (dbmanager, dbmanager.get_protocol())
        elif tname == 'dbtype':
            return (dbmanager, dbmanager.get_dbtype())

    async def recv_del_db(self, idx, cmd):
        """
        Del some data on table from database
        """
        c_key = 'DEL_DB'
        vname = cmd.get('varname')
        option = cmd.get('option')
        vlist = cmd.get('ids')
        if option == 'ONE':
            input_ = [vlist]
        elif option == 'GROUP':
            input_ = vlist
        elif option == 'ALL':
            if option == 'STA':
                input_ = self.engine.stations.keys()
            elif option == 'DB':
                input_ = self.engine.db_data.keys()
        tname = self.engine.get_tname(vname)
        ans = ''
        try:
            self.engine.del_db(tname, input_)
            ans = 'OK'
        except:
            ans = 'NO'
        cmd['command'].update({'answer': ans})
        return cmd

    async def recv_del_ins(self, idx, cmd):
        """
        Delete some data from instances
        """
        c_key = 'DEL_INS'
        vname = cmd.get('varname')
        option = cmd.get('option')
        idx = cmd.get('idx')
        if option == 'ONE':
            input_ = idx
        elif option == 'GROUP':
            input_ = idx
        elif option == 'ALL':
            if option == 'STA':
                input_ = self.engine.stations.keys()
            elif option == 'DB':
                input_ = self.engine.db_data.keys()
        varin = self.engine.get_var(vname)
        for l in input_:
            if option == 'STA':
                self.del_sta(l)
            else:
                del varin[l]
        ans = 'OK'
        cmd['command'].update({'answer': ans})
        return cmd

    async def recv_collect_sta(self, idx, cmd):
        """
        Start to collect data from some station
        """
        c_key = 'COLLECT_STA'
        bprint(
            "Activando recoleccion en estacion %s" %
            cmd)
        ids_list = cmd.get("command").get('args')
        ans_dict = {}
        ans = {}
        for ids in ids_list:
            self.engine.wait.update({ids: False})
            rprint(self.engine.stations.get(ids))
            print(self.engine.instances, ids in self.engine.instances,
                  ids in self.engine.stations)
            if ids in self.engine.stations:
                try:
                    print("Enviando orden de recolectar->", ids)
                    # self.engine.enqueued.append(ids)
                    rprint("====EENQUEUED=====")
                    bprint(self.engine.enqueued)
                    self.engine.queue_process.put(ids)
                    # Read the queue ans
                    # worst option
                    while self.engine.queue_ans_process.empty():
                        bprint("Esperando a que se llene cola")
                        await asyncio.sleep(1)
                    for elem in read_queue_gen(self.engine.queue_ans_process):
                        rprint("Valor en cola-Respuesta")
                        bprint(elem)
                        ids = elem.get('station')
                        ans.update({ids: elem})
                    ###
                except:
                    ans = {}
                ans_dict.update(ans)
        cmd['command'].update({'answer': ans_dict})
        return cmd

    async def recv_stop_sta(self, idx, cmd):
        """
        Stop to collect data from ids station
        """
        c_key = 'STOP_STA'
        bprint("Recv stop sta CMD--->")
        rprint(cmd)
        stations, cores = cmd.get('command').get('args', (None, None))

        answer = {}

        while len(answer.keys()) < len(stations):
            gprint("TTT")
            rprint(len(answer.keys()))
            rprint(len(stations))
            gprint("TTT")
            await asyncio.sleep(.1)
            for ipt in cores:
                rprint("IPT->%s" % ipt)
                for ids in stations:
                    bprint("IDS->%s" % ids)
                    gprint("Engine ids->%s ::: ipt->%s" %
                           (ids, self.engine.get_ipt(ids)))
                    ipt_x = self.engine.get_ipt(ids)
                    if ipt == ipt_x:
                        # a wise control to wait a gap in the async while
                        rprint("Esperando que se libere")
                        while self.engine.free_ids[ids]:
                            await asyncio.sleep(0.01)
                        self.engine.wait[ids] = True
                        rprint("Deteniendo ids....")
                        await self.engine.stop(ipt, ids)
                        ans = {ids: {'stopped': True}}
                        answer.update(ans)
                        self.engine.wait[ids] = False
                        rprint(len(answer.keys()))
                        rprint(len(stations))
                        bprint("While condition .::: %s" %
                               (len(answer.keys()) < len(stations)))

        cmd['command'].update({'answer': answer})
        return cmd

    async def recv_end(self, idx, cmd):
        pass

    async def interpreter(self, msg):
        # save msg on log
        idm = self.engine.set_idm()
        msg.update({'timestamp_in': timestamp()})
        # process incoming msg
        # first action code
        # ie: GET_LST
        c_key = msg.get('command', {}).get('action')
        in_cmd = msg
        in_cmd.update({'timestamp_in': timestamp()})
        group = msg.get('group')
        COMMAND = self.commands.get(c_key, {})
        bprint("=====INTEPRETER=======")
        rprint("COMMAND>%s" % COMMAND)
        bprint("MSG IN %s" % in_cmd)
        bprint("=====INTEPRETER=======")
        if group in COMMAND.get('group'):
            coro_callback = self.msg_process.get(c_key)
            bprint("Coroutine->%s" % coro_callback)
            return await coro_callback(idm, in_cmd)
