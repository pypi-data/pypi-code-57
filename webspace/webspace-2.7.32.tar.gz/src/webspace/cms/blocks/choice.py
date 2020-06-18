from wagtail.core import blocks
from .. import constants


class ThemeChoiceBlock(blocks.ChoiceBlock):
    choices = constants.THEME_CHOICES
    default = constants.THEME_SPACE


class SizeChoiceBlock(blocks.ChoiceBlock):
    choices = constants.SIZE_CHOICES
    default = constants.SIZE_M


class ContainerChoiceBlock(blocks.ChoiceBlock):
    choices = constants.CONTAINER_CHOICES
    default = constants.CONTAINER_REGULAR


class ButtonChoiceBlock(blocks.ChoiceBlock):
    choices = constants.BUTTON_CHOICES
    default = constants.BUTTON_PRIMARY


class AlignTextChoiceBlock(blocks.ChoiceBlock):
    choices = constants.ALIGN_TEXT_CHOICES
    default = constants.ALIGN_TEXT_NULL


class BackgroundPositionChoiceBlock(blocks.ChoiceBlock):
    choices = constants.BACKROUND_POSITION_CHOICES
    default = constants.BACKROUND_POSITION_CENTER

