
###################################
#Actions LEVEL 3: Services
###################################

"""
Review the different commands vy services

Could be a new class?

Collector Service
=================
COMMANDS=dict(
    ADD_STA=dict(
        code="ADD|STA|[ARGS]",
        answer='ADD|STA|RECV|[ANSWER]',
        desc="information from a station, add to list and send a recv msg",
        group=groups[0:2]),
    ADD_DATADB=dict(
        code='ADD|DATADB|[DBTYPE]|[ARGS]',
        answer='ADD|DATADB|RECV|[ANSWER]',
        desc="add a [DBTYPE] instance with [ARGS], check if exist in DB list",
        group=groups[0:2]),
    INIT_VAR=dict(
        code='INIT|VAR|[VARNAME]|[IDx]',
        answer='INIT|VAR|RECV|[ANSWER]',
        desc='initialize the instance [sta] or [db] identifief by IDx',
        group=groups[0:2]),
    DEL_STA=dict(
        code="DEL|STA|[IDS]",
        answer="DEL|STA|RECV|[ANSWER]",
        desc="delete [ids] station from engine memory",
        group=groups[0:2],),
    COLLECT_STA=dict(
        code="COLLECT|STA|[IDS]",
        answer="COLLECT|STA|RECV|[ANSWER]",
        desc="collect data from [ids] station",
        group=groups[0:2],),
    STOP_STA=dict(
        code="STOP|STA|[IDS]",
        answer="STOP|STA|RECV|[ANSWER]",
        desc="stop collect data from [ids] station",
        group=groups[0:2],),
    GET_CMD=dict(
        code="GET|CMD",
        answer='GET|CMD|RECV|[ANSWER]',
        desc='a request for the list of commands',
        group=groups),
    GET_INFO=dict(
        code="GET|INFO|[VARNAME]|[IDX]",
        answer="GET|INFO|[VARNAME]|[IDX]|[ANSWER]",
        desc="if you need some information about [VARNAME]={STA, DB, PROT} in particular",
        group=groups),
    GET_LST=dict(
        code="GET|LST|[VARNAME]",
        answer="GET|LST|RECV|[VARNAME]|[ANSWER]",
        desc='a request for get the list of [VARNAME]={STA,PROT,DB} avalaibles on the engine',
        group=groups),
    UPD_STA=dict(
        code="UPD|STA|[IDS]|[KEY]|[VALUE]",
        answer="UPD|STA|RECV||[IDS]|[ANSWER]",
        desc='update [ids] station with new [value] on [key]	',
        group=groups[0:2]),
    UPD_DATADB=dict(
        code="UPD|DATDB|[IDD]|[KEY]|[VALUE]",
        answer="UPDA|DATADB|RECV||[IDS]|[ANSWER]",
        desc="update [idd] database with new [value] on [key]",
        group=groups[0:2]),
    SAVE_DB=dict(
        code="SAVE|DB|[VARNAME]|[OPTION]|[IDS]",
        answer="SAVE|DB|RECV|[VARNAME]|[ANSWER]",
        desc="save data from [ids] list station[s],OPTION={ONE,GROUP,ALL}",
        group=groups[0:2],),
    UPD_DB=dict(
        code="UPD|DB|[VARNAME]|[IDS]|[KEY]|[VALUE]",
        answer="UPD|DB|RECV|[VARNAME]|[ANSWER]",
        desc="update [ids] station on [key] with [value]",
        group=groups[0:2]),
    GET_DB=dict(
        code="GET|DB|LST|[TABLE_NAME]",
        answer="GET|DB|RECV|[ANSWER]",
        desc="a request for the list of elements in table",
        group=groups[0:2],),
    DEL_DB=dict(
        code="DEL|DB|[VARNAME]|[OPTION]|[IDS]",
        answer="DEL|DB|RECV|[VARNAME]|[ANSWER]",
        desc="delete [ids] list station[s], OPTION={ONE,GROUP,ALL}",
        group=groups[0:2]),
    END=dict(
        code="<END>",
        answer="<END>",
        desc="End of a message set",
        group=groups,)
    )



"""



