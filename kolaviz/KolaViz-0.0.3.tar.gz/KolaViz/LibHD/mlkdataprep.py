# -*-coding:utf-8-*-
import pandas as pd
import re
import datetime as dt


class Replies:
    def __init__(self, fn=None, rdf=None):
        """load a file where tuples are separated by ;ET; and element ;EE;
        return a pd.DfFrame"""
        if fn is not None:
            with open(fn, "r") as f:
                rep = f.read()

            tuples = rep.split(";ET;\n")

            # removing duplicates
            s = pd.Series(pd.Series(tuples).unique())
            rdf = s.str.split(";EE;", expand=True)

            # removing last empty column
            rdf = rdf.drop(8, axis=1)

            rdf.columns = [
                "p_id",
                "p_meta",
                "p_text",
                "author_id",
                "p_type",
                "p_title",
                "p_comment",
                "p_upvote",
            ]

            # if line with no post_id, remove it
            if any(rdf.p_id == ""):
                rdf = rdf.drop(rdf.loc[rdf.p_id == ""].index)

            self.df = rdf.copy()
        elif rdf is None:
            raise Exception("Au moins fn ou rdf doivent être non None")
        else:
            # c'est que fn is none et pas rdf
            self.df = rdf

    def __str__(self):
        return "%s" % self.df

    def expand_ids(self):
        eids = self.df.p_id.str.split("/", expand=True).drop([1, 3], axis=1)
        eids.columns = ["threads_ids", "replies_ids", "comments_ids"]
        return eids

    def get_Fids(self, type_id):
        loc = 0
        if type_id == "thread":
            loc = "threads_ids"
        elif type_id == "reply":
            loc = "replies_ids"
        elif type_id == "comment":
            loc = "comments_ids"
        else:
            raise Exception(">>%s<< No such type_id." % type_id)

        s = self.expand_ids().loc[:, loc].dropna().unique()

        return pd.Series(s)

    def get_Fusers(self):
        return self.df.author_id.unique()

    def get_nb_Fcomments(self):
        return len(self.get_Fids("comment"))

    def get_nb_Frc(self):
        return len(self.get_Fids("reply"))

    def get_nb_Freplies(self):
        return len(self.df) - self.get_nb_Fthreads()

    def get_nb_Fthreads(self):
        return len(self.get_Fids("thread"))

    def get_nb_Fusers(self):
        return len(self.get_Fusers())

    def get_posts_with_uid(self, uid):
        return self.df.loc[self.df.author_id == uid]

    def get_posts_with_uname(self, uname="Malik Koné"):
        return self.df[self.get_all_unames().str.contains(uname)]

    def get_all_unames(self):
        unames = self.expand_metas().full_names.str.strip()
        return unames

    def expand_metas(self):
        # remettre ça dans la dfframe principale, ou s'en servir juste pour indice
        pat = (
            r" *(?P<full_names>.*?)"
            "(?P<roles>(?:(?:Teaching )?Staff|Instructor))?"
            "(?P<forum_names>(?:Week|Assign|General)[^·]*?)? · "
            "(?P<humanized_dates>[^·]*)"
            "(?P<extras>·? Edited.*)?$"
        )
        return self.df.p_meta.str.extract(pat, expand=True)


class ExpandedReplies:
    def __init__(self, fn=None, rdf=None):
        self.rep = Replies(fn=fn, rdf=rdf)
        self.df = self.rep.df.join(self.rep.expand_metas())

        self.df = self.df.drop("p_meta", axis=1)

        self.df.p_upvote = self.df.p_upvote.apply(coerce_upvotes)
        self.df.loc[:, "age"] = self.df.humanized_dates.apply(dehumanize_dates)

        users = self.get_ids()["users"]
        self.df.loc[:, "uid"] = self.df.author_id.apply(lambda x: users.index(x))

        rolesIds = list(self.df.roles.unique())
        self.df.loc[:, "rolesid"] = self.df.roles.apply(lambda x: rolesIds.index(x))

        threadsIds = self.get_ids()["threads"]
        self.df.loc[:, "tid"] = self.df.p_id.apply(lambda x: indexeur(x, threadsIds))

        repliesIds = self.get_ids()["replies"]
        self.df.loc[:, "rid"] = self.df.p_id.apply(lambda x: indexeur(x, repliesIds))

        commentsIds = self.get_ids()["comments"]
        self.df.loc[:, "cid"] = self.df.p_id.apply(lambda x: indexeur(x, commentsIds))

        pTypesIds = list(self.df.p_type.unique())
        self.df.loc[:, "p_typeid"] = self.df.p_type.apply(lambda x: pTypesIds.index(x))

        # on règle un pb de duplicate dans les données aspirées en ignorant les vairation sur quelques colonnes et en ne gardant que les plus ancienne date.
        # le problème c'est que ces entrées on le même p_id
        ignoreCols = [
            "p_text",
            "forum_names",
            "p_comment",
            "p_upvote",
            "age",
            "humanized_dates",
        ]
        # garde celle avec le max age?
        backupWithGoodDates = (
            self.df.loc[:, ignoreCols + ["p_id"]]
            .groupby("p_id")
            .aggregate(max)
            .loc[:, ignoreCols]
        )

        self.df = (
            self.df.drop(ignoreCols, axis=1)
            .drop_duplicates()
            .dropna(axis=0, how="all")
            .join(backupWithGoodDates, on="p_id", how="left")
        )

        self.df.loc[:, "p_ts"] = self.df.age.apply(get_ts_from_age, asTs=False)
        #        self.df.loc[:, "p_ts"] = self.df.age.apply(get_ts_from_age, asTs=False)

        # au niveau des noms de forums on forward fill the nans
        self.df.forum_names = self.df.forum_names.ffill()
        self.create_new_ts()

    def __str__(self):
        return "%s" % self.df

    def get_staff_infos(self):
        """Return the staff names uid and roles"""
        idx = self.df.roles.str.contains("Staff").dropna().index
        staff_infos = self.df.loc[
            idx, ["author_id", "full_names", "roles"]
        ].drop_duplicates()

        return staff_infos

    def statistiques_generales(self):
        m = self.df.p_type == "thread_starter"
        nb_threads = len(self.df.loc[m])
        nb_posts = len(self.df)
        nb_users = len(self.df.author_id.drop_duplicates())
        return nb_threads, nb_posts, nb_users

    def get_ids(self):
        """renvois un dictionnaires de list d'identifiants pour:
        - tous les users,
        - les staffs
        - les mentors
        - les nonStaffs
        - le thread
        - les replies
        - les comments
        """
        users = self.df.author_id.unique()
        staffs = self.get_staff_infos().author_id.values
        mask = self.df.full_names.str.contains("Mentor").values
        mentors = self.df.iloc[mask, :].author_id.unique()

        threads = self.get_pid_where("thread_starter")
        replies = self.get_pid_where("reply")
        comments = self.get_pid_where("reply_comment")

        # threads = self.df.p_id.where(self.df.p_type == "thread_starter").dropna(how="all").unique()
        # replies = self.df.p_id.where(self.df.p_type == "reply").dropna(how="all").unique()
        # comments = self.df.p_id.where(self.df.p_type == "reply_comment").dropna(how="all").unique()
        IDS = {
            "users": list(users),
            "staffs": list(staffs),
            "mentors": list(mentors),
            "staffs_n_mentors": list(staffs) + list(mentors),
            "nonStaffs": list(set(users) - set(staffs) - set(mentors)),
            "threads": list(threads),
            "replies": list(replies),
            "comments": list(comments),
        }
        return IDS

    def get_pid_where(self, p_type):
        return self.df.p_id.where(self.df.p_type == p_type).dropna(how="all").unique()

    def get_uname_from_uid(self, uid):
        mask = self.df.author_id == uid
        uname = self.df.full_names.loc[mask].iloc[0]
        return uname

    def get_user_groups(self):
        return self.df.sort_values("age").groupby("author_id")

    def get_thread_groups(self):
        gkeys = self.df.p_id.apply(lambda x: x.split("/")[0])
        return self.df.groupby(gkeys)

    def get_tid_groups(self):
        return self.df.sort_values("age").groupby("tid")

    def get_uid_groups(self):
        return self.df.sort_values("age").groupby("uid")

    def create_new_ts(self):
        """givent the erdf estime une nouvelle colonne avec les p_newts
        des timestamps vraisemblables
        """
        import numpy.random as rnd

        pTsGs = self.df.groupby("p_ts")
        pTsG_keys = sorted(list(pTsGs.groups.keys()))  # group keys are timestamps
        NpTsGs = len(pTsGs)

        for i, pTsG_key in enumerate(pTsG_keys):
            pTsG_df = pTsGs.get_group(pTsG_key)
            if i < NpTsGs - 2:
                # la dernière date possible est celle du group suivant
                most_recent_p_ts = pTsG_keys[i + 1]
            else:
                # on est sur le dernier group. le plus récent.
                # on suppose que les publications se sont faite dans la semaine
                most_recent_p_ts = pTsG_key + pd.Timedelta(7, unit="D")

            tidGs = pTsG_df.groupby("tid")  # groupe le group de timestamp par thread id
            _ = sorted(list(tidGs.groups.keys()))
            NtidGs = len(tidGs)

            # on génère des dates aléatoire séparées de 10 minutes pour les débuts de messages
            # de même age dans un même thread
            tidTs_choices = pd.date_range(pTsG_key, most_recent_p_ts, freq="600S")[:-1]
            # on en selection autant qu 'il y a de thread pour cette date (ou timestamp)
            tidG_ts = sorted(rnd.choice(tidTs_choices, size=(NtidGs,), replace=False))
            # et on utilise ses temps pour les attribut aux publications
            for j, (tidG_k, tidG_df) in enumerate(tidGs):  # suppose sorted
                # ATTENTION si  tidG_ts[j] est trop proche de most_recent peut manque de place pour générer tous les new ts
                p_ts_choices = pd.date_range(tidG_ts[j], most_recent_p_ts, freq="60S")[
                    :-1
                ]
                try:
                    new_ts = sorted(
                        rnd.choice(p_ts_choices, size=(len(tidG_df),), replace=False)
                    )
                except ValueError:
                    # pour simplifier si il y a pb on pourrait autoriser que des message soit poster en même temps,
                    p_ts_choices = pd.date_range(
                        tidG_ts[j], most_recent_p_ts, freq="S"
                    )[:-1]
                    new_ts = sorted(
                        rnd.choice(p_ts_choices, size=(len(tidG_df),), replace=False)
                    )
                idx = tidG_df.index
                self.df.loc[
                    idx, "p_newts"
                ] = new_ts  # faudrait s'assurer qu'un auteur ne plubie pas deux message exactement en même temps


def coerce_upvotes(x):
    """soit un element x de type chaine de char, on va juste récupérer l'entier qui est dedans"""
    digit_rpat = re.compile(r"\d+")
    trouvaille = digit_rpat.findall(x)

    return int(trouvaille[0]) if trouvaille != [] else 0


def get_ts_from_age(x, refdt="5-feb-2018", asTs=True):
    """returns a timestamp from a humanized date and a reference date
par defautl refdt est 5-feb-2018 la date de récupération des donnes de coursera 2017
if asTs is True return as timestamp otherwise return a pd.Timestamp object
    """
    ts = pd.Timestamp(refdt)
    timeDelta = pd.Timedelta(x, unit="s")
    return (ts - timeDelta).timestamp() if asTs else (ts - timeDelta)


def dehumanize_dates(x):
    """soit la chaine de char x, avec une date humanize (ex '12 days ago ', '20 days ago ', '22 days ago') on la déhumanise et renvois le temps en secondes"""
    x.strip()
    val, unit = x.split(" ")[:2]
    val = 1 if "a" in val else int(val)
    if "minute" in unit:
        val = dt.timedelta(minutes=int(val))
    if "hour" in unit:
        val = dt.timedelta(minutes=60 * int(val))
    if "day" in unit:
        val = dt.timedelta(days=int(val))
    if "month" in unit:
        val = dt.timedelta(days=int(val) * 30)
    if "year" in unit:
        val = dt.timedelta(days=int(val) * 365)

    return int(val.total_seconds())


def indexeur(x, aList):
    """Returns the index position of the first element of aList contained in x"""
    for (k, listElt) in enumerate(aList):
        if listElt in x:
            return k
    return None
