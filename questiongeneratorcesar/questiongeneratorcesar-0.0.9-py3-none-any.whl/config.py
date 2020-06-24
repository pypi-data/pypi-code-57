from dataclasses import dataclass

MAX_SYNONYM_ANSWERS = 9
MAX_SENTENCE_SCRABBLE_LENGTH = 9
MIN_SENTENCE_SCRABBLE_LENGTH = 2

@dataclass
class DbConfig:
    user_db: str
    password_db: str
    uri_db: str
