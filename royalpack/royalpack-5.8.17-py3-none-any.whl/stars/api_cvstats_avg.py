import royalnet.utils as ru
from royalnet.backpack.tables import *
from royalnet.constellation.api import *
from ..tables import Cvstats


class ApiCvstatsAvgStar(ApiStar):
    path = "/api/cvstats/avg/v1"

    methods = ["GET"]

    summary = "Get some averages on the cvstats."

    tags = ["cvstats"]

    async def api(self, data: ApiData) -> ru.JSON:
        results = data.session.execute("""
SELECT *
FROM (
         SELECT date_part('hour', c.h)   ph,
                AVG(c.members_connected) members_connected,
                AVG(c.users_connected)   users_connected,
                AVG(c.members_online)    members_online,
                AVG(c.users_online)      users_online,
                AVG(c.members_playing)   members_playing,
                AVG(c.users_playing)     users_playing,
                AVG(c.members_total)     members_total,
                AVG(c.users_total)       users_total
         FROM (
                  SELECT date_trunc('hour', c.timestamp) h,
                         AVG(c.members_connected)        members_connected,
                         AVG(c.users_connected)          users_connected,
                         AVG(c.members_online)           members_online,
                         AVG(c.users_online)             users_online,
                         AVG(c.members_playing)          members_playing,
                         AVG(c.users_playing)            users_playing,
                         AVG(c.members_total)            members_total,
                         AVG(c.users_total)              users_total
                  FROM cvstats c
                  GROUP BY h
              ) c
         GROUP BY ph
) all_time
LEFT JOIN
(
         SELECT date_part('hour', c.h)   ph,
                AVG(c.members_connected) members_connected,
                AVG(c.users_connected)   users_connected,
                AVG(c.members_online)    members_online,
                AVG(c.users_online)      users_online,
                AVG(c.members_playing)   members_playing,
                AVG(c.users_playing)     users_playing,
                AVG(c.members_total)     members_total,
                AVG(c.users_total)       users_total
         FROM (
                  SELECT date_trunc('hour', c.timestamp) h,
                         AVG(c.members_connected)        members_connected,
                         AVG(c.users_connected)          users_connected,
                         AVG(c.members_online)           members_online,
                         AVG(c.users_online)             users_online,
                         AVG(c.members_playing)          members_playing,
                         AVG(c.users_playing)            users_playing,
                         AVG(c.members_total)            members_total,
                         AVG(c.users_total)              users_total
                  FROM cvstats c
                  WHERE c.timestamp > current_timestamp - interval '7 day'
                  GROUP BY h
              ) c
         GROUP BY ph
) last_week ON last_week.ph = all_time.ph
LEFT JOIN
(
         SELECT date_part('hour', c.h)   ph,
                AVG(c.members_connected) members_connected,
                AVG(c.users_connected)   users_connected,
                AVG(c.members_online)    members_online,
                AVG(c.users_online)      users_online,
                AVG(c.members_playing)   members_playing,
                AVG(c.users_playing)     users_playing,
                AVG(c.members_total)     members_total,
                AVG(c.users_total)       users_total
         FROM (
                  SELECT date_trunc('hour', c.timestamp) h,
                         AVG(c.members_connected)        members_connected,
                         AVG(c.users_connected)          users_connected,
                         AVG(c.members_online)           members_online,
                         AVG(c.users_online)             users_online,
                         AVG(c.members_playing)          members_playing,
                         AVG(c.users_playing)            users_playing,
                         AVG(c.members_total)            members_total,
                         AVG(c.users_total)              users_total
                  FROM cvstats c
                  WHERE c.timestamp > current_timestamp - interval '30 day'
                  GROUP BY h
              ) c
         GROUP BY ph
) last_month ON last_month.ph = all_time.ph
LEFT JOIN
(
         SELECT date_part('hour', c.h)   ph,
                AVG(c.members_connected) members_connected,
                AVG(c.users_connected)   users_connected,
                AVG(c.members_online)    members_online,
                AVG(c.users_online)      users_online,
                AVG(c.members_playing)   members_playing,
                AVG(c.users_playing)     users_playing,
                AVG(c.members_total)     members_total,
                AVG(c.users_total)       users_total
         FROM (
                  SELECT date_trunc('hour', c.timestamp) h,
                         AVG(c.members_connected)        members_connected,
                         AVG(c.users_connected)          users_connected,
                         AVG(c.members_online)           members_online,
                         AVG(c.users_online)             users_online,
                         AVG(c.members_playing)          members_playing,
                         AVG(c.users_playing)            users_playing,
                         AVG(c.members_total)            members_total,
                         AVG(c.users_total)              users_total
                  FROM cvstats c
                  WHERE c.timestamp > current_timestamp - interval '1 day'
                  GROUP BY h
              ) c
         GROUP BY ph
) last_day ON last_day.ph = all_time.ph;
        """)

        return [{
            "h": r[0],
            "all_time": {
                "members_connected": float(r[1]),
                "users_connected": float(r[2]),
                "members_online": float(r[3]),
                "users_online": float(r[4]),
                "members_playing": float(r[5]),
                "users_playing": float(r[6]),
                "members_total": float(r[7]),
                "users_total": float(r[8])
            },
            "last_week": {
                "members_connected": float(r[10]),
                "users_connected": float(r[11]),
                "members_online": float(r[12]),
                "users_online": float(r[13]),
                "members_playing": float(r[14]),
                "users_playing": float(r[15]),
                "members_total": float(r[16]),
                "users_total": float(r[17])
            },
            "last_month": {
                "members_connected": float(r[19]),
                "users_connected": float(r[20]),
                "members_online": float(r[21]),
                "users_online": float(r[22]),
                "members_playing": float(r[23]),
                "users_playing": float(r[24]),
                "members_total": float(r[25]),
                "users_total": float(r[26])
            },
            "last_day": {
                "members_connected": float(r[28]),
                "users_connected": float(r[29]),
                "members_online": float(r[30]),
                "users_online": float(r[31]),
                "members_playing": float(r[32]),
                "users_playing": float(r[33]),
                "members_total": float(r[34]),
            },
        } for r in sorted(results.fetchall(), key=lambda s: s[0])]
