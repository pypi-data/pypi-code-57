import pickle
import pathlib

PACKAGE_ROOT = pathlib.Path(__file__).resolve().parent.parent

POS_DICTIONARY_FILE = PACKAGE_ROOT / "resources" / "pos_dictionary.pk"
SOUND_DICTIONARY_FILE = PACKAGE_ROOT / "resources" / "sounds_dictionary.pk"
SYNONYM_DICTIONARY_FILE = PACKAGE_ROOT / "resources" / 'synonym_dictionary.pk'
ANTONYM_DICTIONARY_FILE = PACKAGE_ROOT / "resources" / 'antonym_dictionary.pk'
MEANSLIKE_DICTIONARY_FILE = PACKAGE_ROOT / "resources" / 'meanslike_dictionary.pk'
PRESUFF_DICTIONARY_FILE = PACKAGE_ROOT / "resources" / 'presuff_dictionary.pk'
INTRUDER_DICTIONARY_FILE = PACKAGE_ROOT / "resources" / 'intruder_dictionary.pk'
RELNOUN_DICTIONARY_FILE = PACKAGE_ROOT / "resources" / 'relnoun_dictionary.pk'
PARTWORDTYPING_DICTIONARY_FILE = PACKAGE_ROOT / "resources" / 'partwordtyping_dictionary.pk'
MINIMAL_PAIR_DICTIONARY_FILE = PACKAGE_ROOT / "resources" / 'minimal_pairs_dictionary.pk'
MULTISYNONYM_DICTIONARY_FILE = PACKAGE_ROOT / "resources" / 'multisynonym_dictionary.pk'
SPANISH_DEFINITIONS_DICTIONARY_FILE = PACKAGE_ROOT / "resources" / 'spanish_definitions_dictionary.pk'
ENGLISH_DEFINITIONS_DICTIONARY_FILE = PACKAGE_ROOT / "resources" / 'english_definitions_dictionary.pk'

CORRECT = "correct"
BAITS = "baits"

with open(POS_DICTIONARY_FILE, 'rb') as config_dictionary_file:
    pos2words = pickle.load(config_dictionary_file)

with open(SYNONYM_DICTIONARY_FILE, 'rb') as config_dictionary_file:
    word2synonyms = pickle.load(config_dictionary_file)

with open(SOUND_DICTIONARY_FILE, 'rb') as config_dictionary_file:
    word2soundslike = pickle.load(config_dictionary_file)

with open(ANTONYM_DICTIONARY_FILE, 'rb') as config_dictionary_file:
    word2antonym = pickle.load(config_dictionary_file)

with open(MEANSLIKE_DICTIONARY_FILE, 'rb') as config_dictionary_file:
    word2meanslike = pickle.load(config_dictionary_file)

with open(PRESUFF_DICTIONARY_FILE, 'rb') as config_dictionary_file:
    word2presuffix = pickle.load(config_dictionary_file)

with open(INTRUDER_DICTIONARY_FILE, 'rb') as config_dictionary_file:
    word2intruder = pickle.load(config_dictionary_file)

with open(RELNOUN_DICTIONARY_FILE, 'rb') as config_dictionary_file:
    word2relnoun = pickle.load(config_dictionary_file)

with open(PARTWORDTYPING_DICTIONARY_FILE, 'rb') as config_dictionary_file:
    word2partwordtyping = pickle.load(config_dictionary_file)

with open(MINIMAL_PAIR_DICTIONARY_FILE, 'rb') as config_dictionary_file:
    word2minimalpair = pickle.load(config_dictionary_file)

with open(MULTISYNONYM_DICTIONARY_FILE, 'rb') as config_dictionary_file:
    word2multisynonym = pickle.load(config_dictionary_file)

with open(SPANISH_DEFINITIONS_DICTIONARY_FILE, 'rb') as config_dictionary_file:
    word2spanishdefinitions = pickle.load(config_dictionary_file)

with open(ENGLISH_DEFINITIONS_DICTIONARY_FILE, 'rb') as config_dictionary_file:
    word2englishdefinitions = pickle.load(config_dictionary_file)
