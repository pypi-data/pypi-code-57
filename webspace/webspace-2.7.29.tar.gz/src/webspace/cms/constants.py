BLOCK_TEMPLATES_PATH = 'webspace/cms/blocks'
PAGES_TEMPLATES_PATH = 'webspace/cms/pages'

THEME_SPACE = 'space'
THEME_SPACE_INVERSE = 'space-inverse'
THEME_LIGHT = 'light'


THEME_CHOICES = (
    (THEME_SPACE, "Space"),
    (THEME_SPACE_INVERSE, "Space Inverse"),
    (THEME_LIGHT, "Light"),
)

SIZE_XS = 'xs'
SIZE_S = 's'
SIZE_M = 'm'
SIZE_L = 'l'
SIZE_X = 'x'
SIZE_XL = 'xl'

SIZE_CHOICES = (
    (SIZE_XS, 'XS'),
    (SIZE_S, 'S'),
    (SIZE_M, 'M'),
    (SIZE_L, 'L'),
    (SIZE_X, 'X'),
    (SIZE_XL, 'XL'),
)


CONTAINER_REGULAR = 'regular'
CONTAINER_CONTENT = 'content'
CONTAINER_FULL = 'full'

CONTAINER_CHOICES = (
    (CONTAINER_REGULAR, 'Regular'),
    (CONTAINER_CONTENT, 'Content (blog)'),
    (CONTAINER_FULL, 'Full (width 100%)'),
)

BUTTON_GREEN_LIGHT = 'green-light'
BUTTON_GREEN_FULL = 'green-full'
BUTTON_WHITE_LIGHT = 'white-light'
BUTTON_WHITE_FULL = 'white-full'
BUTTON_BLUE_LIGHT = 'blue-light'
BUTTON_BLUE_FULL = 'blue-full'

BUTTON_CHOICES = (
    (BUTTON_GREEN_LIGHT, 'Green Light'),
    (BUTTON_GREEN_FULL, 'Green Full'),
    (BUTTON_WHITE_LIGHT, 'White Light'),
    (BUTTON_WHITE_FULL, 'White Full'),
    (BUTTON_BLUE_LIGHT, 'Blue Light'),
    (BUTTON_BLUE_FULL, 'Blue Full'),
)

ALIGN_TEXT_NULL = None
ALIGN_TEXT_LEFT = 'left'
ALIGN_TEXT_JUSTIFY = 'justify'
ALIGN_TEXT_CENTER = 'center'
ALIGN_TEXT_RIGHT = 'right'

ALIGN_TEXT_CHOICES = (
    (ALIGN_TEXT_NULL, "Unset"),
    (ALIGN_TEXT_LEFT, "Left"),
    (ALIGN_TEXT_CENTER, "Center"),
    (ALIGN_TEXT_RIGHT, "Right"),
    (ALIGN_TEXT_JUSTIFY, "Justify"),
)

BACKROUND_POSITION_TOP = 'top'
BACKROUND_POSITION_CENTER = 'center'
BACKROUND_POSITION_BOTTOM = 'bottom'
BACKROUND_POSITION_LEFT = 'left'
BACKROUND_POSITION_RIGHT = 'right'

BACKROUND_POSITION_CHOICES = (
    (BACKROUND_POSITION_TOP, "Top"),
    (BACKROUND_POSITION_CENTER, "Center"),
    (BACKROUND_POSITION_BOTTOM, "Bottom"),
    (BACKROUND_POSITION_LEFT, "Left"),
    (BACKROUND_POSITION_RIGHT, "Right"),
)
