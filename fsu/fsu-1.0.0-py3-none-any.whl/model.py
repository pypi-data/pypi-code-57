from sqlalchemy import Column, func
from sqlalchemy import Integer, DateTime

def common_columns():
    return [
        Column("id"        , Integer , primary_key=True, autoincrement=True),
        Column("created_at", DateTime, index=True, server_default=func.current_timestamp()),
        Column("updated_at", DateTime, index=True, server_default=func.current_timestamp(), server_onupdate=func.current_timestamp()),
    ]
