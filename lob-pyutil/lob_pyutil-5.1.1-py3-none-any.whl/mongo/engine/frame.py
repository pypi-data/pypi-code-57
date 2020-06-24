from mongoengine import Document, StringField
from antarctic.PandasFields import FrameField


class Frame(Document):
    name = StringField(max_length=200, required=True, unique=True)
    frame = FrameField()
