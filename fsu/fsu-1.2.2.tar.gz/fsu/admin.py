from fastapi import FastAPI, Depends, Request, Header
from fastapi.exceptions import HTTPException
from databases import Database

from fsu.internal.error import FieldNotExist, ObjectNotExist, UnsupportedOperator
from fsu.internal.schema import ReadMany, ReadOne, UpdateMany, UpdateOne, DeleteMany, DeleteOne, CreateOne, \
                                LoginIn, LoginOut, GetCurrentUserOut
import fsu.internal.error_code as E
from fsu.security import sign_required, jwt_field_required, get_jwt_info
from fsu.wxwork import get_user_by_code
from fsu.sql import make_mapper, verbose_where
from fsu.error import handle_universal_logic_error, UniversalLogicError
from fsu.schema import OK
import jwt

def make_admin_app(
    corp_id,
    enums,
    jwt_secret,
    metadata,

    get_db,
    get_unicode_redis,
    get_secret_by_uaid,
    get_corp_secret_by_uaid,

    debug = False
):
    app    = FastAPI(openapi_prefix="/admin")
    tables = metadata.tables

    app.add_exception_handler(UniversalLogicError, handle_universal_logic_error)

    if not debug:
        app.middleware("http")(sign_required(ttl=60, get_secret_by_uaid=get_secret_by_uaid))

    admin_required = jwt_field_required("admin_id", jwt_secret)

    @app.post("/login", response_model=OK[LoginOut])
    async def login(
        i      : LoginIn,
        x_uaid : str = Header(...),
        db           = Depends(get_db),
        redis        = Depends(get_unicode_redis),
    ):
        corp_secret = await get_corp_secret_by_uaid(x_uaid)

        if corp_secret is None:
            raise HTTPException(401, "invalid X-UAID")

        user_info = await get_user_by_code(corp_id, corp_secret, x_uaid, i.code, redis)

        fsu_admin  = tables["fsu_admin"]
        admin_id   = None
        admin_user = await db.fetch_one(fsu_admin.select().where(fsu_admin.c.user_id == user_info["userid"]))

        if admin_user is None:
            admin_id = await db.execute(fsu_admin.insert().values(
                user_id = user_info["userid"],
                name    = user_info["name"],
            ))
        else:
            admin_id = admin_user[fsu_admin.c.id]

        token = jwt.encode({ "admin_id" : admin_id }, jwt_secret)

        return OK(data=LoginOut(access_token=token))

    @app.get("/user", response_model=OK[GetCurrentUserOut])
    @admin_required
    async def get_current_user(info = Depends(get_jwt_info(jwt_secret)), db = Depends(get_db)):
        admin_id = info.get("admin_id")

        if admin_id is None:
            raise UniversalLogicError(E.INVALID_TOKEN)

        fsu_admin = tables["fsu_admin"]
        mapper    = make_mapper("fsu_admin", metadata, GetCurrentUserOut)

        row = await db.fetch_one(mapper.select().where(fsu_admin.c.id == admin_id))

        if row is None:
            raise UniversalLogicError(E.INVALID_TOKEN)

        return OK(data=mapper.dict(row))

    @app.get("/enums")
    @admin_required
    async def get_enums():
        return OK(data=enums)

    @app.post("/read")
    @admin_required
    async def read_many(i : ReadMany, db : Database = Depends(get_db)):
        try:
            mapper = make_mapper(i.object, metadata, i.fields_)

            if i.filter is not None:
                mapper.where(i.filter)

            if i.order is not None:
                mapper.order_by(i.order)

            sql = mapper.select() \
                    .offset((i.page - 1) * i.size) \
                    .limit(i.size)

            count_sql = mapper.count()
        except ObjectNotExist as e:
            raise HTTPException(422, f"object `{e.object}` not exist")
        except FieldNotExist as e:
            raise HTTPException(422, f"field `{e.field}` of object `{e.object}` not exist")
        except UnsupportedOperator as e:
            raise HTTPException(422, f"operator `{e.op}` not supported")

        data  = [mapper.dict(r) for r in await db.fetch_all(sql)]
        total = await db.fetch_val(count_sql)

        return OK(data=data, total=total)

    @app.post("/read/{id}")
    @admin_required
    async def read_one(id : int, i : ReadOne, db : Database = Depends(get_db)):
        try:
            mapper = make_mapper(i.object, metadata, i.fields_)

            mapper.where(["EQ", ["id"], id])

            sql = mapper.select()
        except ObjectNotExist as e:
            raise HTTPException(422, f"object `{e.object}` not exist")
        except FieldNotExist as e:
            raise HTTPException(422, f"field `{e.field}` of object `{e.object}` not exist")
        except UnsupportedOperator as e:
            raise HTTPException(422, f"operator `{e.op}` not supported")

        data = mapper.dict(await db.fetch_one(sql))

        return OK(data=data)

    @app.post("/create")
    @admin_required
    async def create_one(i : CreateOne, db : Database = Depends(get_db)):
        if i.object not in tables:
            raise HTTPException(422, f"object `{i.object}` not exist")

        table = tables[i.object]

        for k, _ in i.values:
            if k not in table.c:
                raise HTTPException(422, f"field `{k}` of object `{i.object}` not exist")

        sql = table.insert().values(dict(i.values))
        await db.execute(sql)

        return OK()

    @app.post("/update")
    @admin_required
    async def update_many(i : UpdateMany, db : Database = Depends(get_db)):
        try:
            where_clause = verbose_where(i.object, metadata, i.filter)

            table = tables[i.object]

            sql = table.update().values(dict(i.values)).where(where_clause)
        except ObjectNotExist as e:
            raise HTTPException(422, f"object `{e.object}` not exist")
        except FieldNotExist as e:
            raise HTTPException(422, f"field `{e.field}` of object `{e.object}` not exist")
        except UnsupportedOperator as e:
            raise HTTPException(422, f"operator `{e.op}` not supported")

        ret = await db.execute(sql)

        return OK(data=ret)

    @app.post("/update/{id}")
    @admin_required
    async def update_one(id : int, i : UpdateOne, db : Database = Depends(get_db)):
        if i.object not in tables:
            raise HTTPException(422, f"object `{i.object}` not exist")

        table = tables[i.object]

        for k, _ in i.values:
            if k not in table.c:
                raise HTTPException(422, f"field `{k}` of object `{i.object}` not exist")

        sql = table.update().values(dict(i.values)).where(table.c.id == id)
        await db.execute(sql)

        return OK()

    @app.post("/delete")
    @admin_required
    async def delete_many(i : DeleteMany, db : Database = Depends(get_db)):
        try:
            where_clause = verbose_where(i.object, metadata, i.filter)

            table = tables[i.object]

            sql = table.delete().where(where_clause)
        except ObjectNotExist as e:
            raise HTTPException(422, f"object `{e.object}` not exist")
        except FieldNotExist as e:
            raise HTTPException(422, f"field `{e.field}` of object `{e.object}` not exist")
        except UnsupportedOperator as e:
            raise HTTPException(422, f"operator `{e.op}` not supported")

        ret = await db.execute(sql)

        return OK(data=ret)

    @app.post("/delete/{id}")
    @admin_required
    async def delete_one(id : int, i : DeleteOne, db : Database = Depends(get_db)):
        if i.object not in tables:
            raise HTTPException(422, f"object `{i.object}` not exist")

        table = tables[i.object]

        sql = table.delete().where(table.c.id == id)
        await db.execute(sql)

        return OK()

    return app
