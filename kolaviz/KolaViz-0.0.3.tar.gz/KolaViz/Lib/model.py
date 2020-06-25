# -*- coding: utf-8 -*-
BASE_DIR = "."

# #### change data to send to visu. Check function unige too
ESSENTIALCOLS = [
    "threadID",
    "tTitle",
    "msgID",
    "author",
    "authorID",
    "msgMREd",
    "autRole",
    "wtext",
    "nmf_ctg",
    "iTokens",
    "strength",
]

LOGFMT1 = "%(asctime)s %(threadName)s~%(levelno)s /%(filename)s@%(lineno)s@%(funcName)s/ %(message)s"
LOGFMT = "/%(filename)s@%(lineno)s@%(funcName)s/ %(message)s"
# general constante
LOGLEVEL_DFT = "INFO"

# coursecode
CRSCD = {
    "c17": {
        "villes-africaines": "va",
        "python-machine-learning": "pml",
        "python-plotting": "pp",
    },
    "c18": {"ufm": "ufm", "ddl": "ddl"},
}

# # Définition d'un modèle minimal

KORCOLS = {
    # le thread (ou fil de discussion)
    # c'est le regroupement principal des messages
    # Il peut être créer par n'importe quel utilisateur
    "threadID",
    # Auteur
    "authorID",
    # Message
    "msgID",
    "msgContent",
    "msgMREd",  # message Most Recent Edition (time)
}

# ## Attributs extra du modèle
EXTRACOLS = {
    # hierachisation des threads
    "forumID",
    "forumCat",  # forum can abe organised in categories
    # messages extra
    "msgType",  # reply, thread_starter, comment,
    # parfois la plateforme (ex. Edx) peut distinguer les thread_starter qui sont des
    # questions des discussions ou question de quiz
    "msgCreaTs",  # message creation timestamp
    "authorRole",  # staff, tutor, mentor, instructor, learner
    "authorName",  # staff, tutor, mentor, instructor, learner
    "msgUV",  # message upvote, or stars.
    "msgStatus",  # pinned on top of thread or Forum, or not.
    # content related
    "msgTopic",  # usualy a vector showing the distribution of the messages terms over K topics
    "msgLang",  # for consitency should filter messages on the same language
    "msgLen",  # message Length
}


COURSE_DFT = "ddl_c18"
LANG_DFT = "fr"

# constantes pour les noms de fichiers
DATA_DIR = "Data"
DATABASE_DIR = "Data/DB"
HARMO_FNAME_DFT = f"{DATABASE_DIR}/cx_hdf_dataset.pkl"
TOK_OUTDIR_DFT = f"{DATA_DIR}/Tokenized_files"
CIR_OUTDIR_DFT = f"{DATA_DIR}/Graphes_and_circuits"
VEC_INDIR_DFT = TOK_OUTDIR_DFT
VEC_FNAME_DFT = f"{VEC_INDIR_DFT}/tokenized_1ng_mlkst_mlkwt.pkl"
STOPWORD_DIR = f"{DATA_DIR}/Stopwords"
VEC_OUTDIR_DFT = f"{DATA_DIR}/Clustered_files"

HARMO_ACTION_DFT = "build_save"

# vectorisation
TOK_PREFIX_DFT = "tokenized"
TOK_FNAME_DFT = f"{TOK_OUTDIR_DFT}/tokenized_1ng_mlkst_mlkwt.pkl"
TOK_TOKENIZERS = ["mlk"]
TOK_WORDENIZERS = ["mlk"]
TOK_NGRAMS = [1]
TOK_INFLUENCIAL_NUM = 7  # nombre de tokens à retourner pour les topiques
TOK_ACTION_DFT = "readH_save_build"

# for vectorisation
VEC_ACTION_DFT = "build"
VEC_ALPHA_DFT = 0
VEC_COUNT_DFT = "tfidf"


VEC_L1RATIO_DFT = 1
VEC_MAXITER_DFT = 500
VEC_MAXITER_DFT = 500
VEC_REDUX_DFT = 5
VEC_TOL_DFT = 1e-5
VEC_TOL_DFT = 1e-5
VEC_VERBOSE_DFT = False

# for circuits and graphes
CIR_ACTION_DFT = "read"
CIR_ENUMERATION_DFT = 4
CIR_STG_DFT = 2
CIR_DRAW_DFT = False
CIR_METHODS_DFT = ["all"]
CIR_WTDELTAS_DFT = [1]

# divers
SAMETHREADID_DFT = True
SAMETOP_DFT = True
SIMTYPE_DFT = "jaccard"
SIMFACTOR_DFT = 1.0


# ################ pour func4unige.py ################
STOPWLIST = {"en": "english", "fr": "french", "es": "spanish", "de": "german"}

# logging.setLevel('INFO')
COLT = {  # columns translation
    "_question_": "Q",
    "_questions": "Q",
    "_answer_": "A",
    "_answers": "A",
    "course": "crs",
    "membership": "mbs",
    "user_id": "uid",
    "discussion": "dsc",
    "answers_": "aw",
    "created_ts": "_cts",
    "updated_ts": "_uts",
    "group": "gp",
    "country": "ctr",
    "context": "ctx",
    "unige_": "U",
    "reported_or_inferred_": "",
    "language_cd": "lang",
    "droits_de_lhomme": "ddl",
    "understanding_financial_markets": "ufm",
}
