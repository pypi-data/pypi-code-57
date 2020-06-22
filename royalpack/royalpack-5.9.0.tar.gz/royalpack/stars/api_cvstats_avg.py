import royalnet.utils as ru
from royalnet.backpack.tables import *
from royalnet.constellation.api import *
from ..tables import Cvstats


class ApiCvstatsAvgStar(ApiStar):
    path = "/api/cvstats/avg/v1"

    tags = ["cvstats"]

    async def get(self, data: ApiData) -> ru.JSON:
        """Get some averages on the cvstats."""
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
                "members_connected": float(r[1]) if r[1] is not None else None,
                "users_connected": float(r[2]) if r[2] is not None else None,
                "members_online": float(r[3]) if r[3] is not None else None,
                "users_online": float(r[4]) if r[4] is not None else None,
                "members_playing": float(r[5]) if r[5] is not None else None,
                "users_playing": float(r[6]) if r[6] is not None else None,
                "members_total": float(r[7]) if r[7] is not None else None,
                "users_total": float(r[8]) if r[8] is not None else None,
            },
            "last_week": {
                "members_connected": float(r[10]) if r[10] is not None else None,
                "users_connected": float(r[11]) if r[11] is not None else None,
                "members_online": float(r[12]) if r[12] is not None else None,
                "users_online": float(r[13]) if r[13] is not None else None,
                "members_playing": float(r[14]) if r[14] is not None else None,
                "users_playing": float(r[15]) if r[15] is not None else None,
                "members_total": float(r[16]) if r[16] is not None else None,
                "users_total": float(r[17]) if r[17] is not None else None,
            },
            "last_month": {
                "members_connected": float(r[19]) if r[19] is not None else None,
                "users_connected": float(r[20]) if r[20] is not None else None,
                "members_online": float(r[21]) if r[21] is not None else None,
                "users_online": float(r[22]) if r[22] is not None else None,
                "members_playing": float(r[23]) if r[23] is not None else None,
                "users_playing": float(r[24]) if r[24] is not None else None,
                "members_total": float(r[25]) if r[25] is not None else None,
                "users_total": float(r[26]) if r[26] is not None else None,
            },
            "last_day": {
                "members_connected": float(r[28]) if r[28] is not None else None,
                "users_connected": float(r[29]) if r[29] is not None else None,
                "members_online": float(r[30]) if r[30] is not None else None,
                "users_online": float(r[31]) if r[31] is not None else None,
                "members_playing": float(r[32]) if r[32] is not None else None,
                "users_playing": float(r[33]) if r[33] is not None else None,
                "members_total": float(r[34]) if r[34] is not None else None,
            },
        } for r in sorted(results.fetchall(), key=lambda s: s[0])]
