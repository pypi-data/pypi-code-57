from dataclasses import dataclass


@dataclass
class Bucket:
    treatment: str
    size: int
