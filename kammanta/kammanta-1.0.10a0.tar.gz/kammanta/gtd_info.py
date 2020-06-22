

INBOX_STR = (
    "The inbox is where you first place notes and other materials "
    "that you later intend to sort. It's good practice to clean your inbox once per day "
    "(or more often)"
)

TICKLER_STR = (
    "The tickler is a place where you can store things that you want to be reminded of at a later date. "
    "When the time is up for a tickler item it's placed in the inbox"
)

NA_STR = "Next actions are doable actions that are practical and does not require thinking"
PRJ_STR = "Projects are goals that take more than one action to complete, and lasts less than six months"

CONTACTS_STR = (
    "Contacts are people that you know, you can store contact info and other things "
    "like how you can best support and contribute to the well-being of each other"
)

AGENDAS_STR = (
    "Agendas are collections of things that you want to bring up with people, "
    "often with one of your contacts, but it can also be in meetings with several people"
)

AOI_STR = "Areas of interest and accountability are things that you want to keep track of every week"
GOALS_STR = "Goals are long-term objectives, for things that take 6-12 months"
VISION_STR = "Visions are diffuse goals in the future that can help motivate you"
PURPOSE_AND_PRINCIPLES_STR = (
    "Purpose is the ultimate guideline for what you want to achieve, "
    "and principles are the way that you want to be in the world"
)

# Reference here


def get_guide_text() -> str:
    guide_text_str = ""

    guide_text_str += "## Inbox\n\n" + INBOX_STR + "\n\n\n"
    guide_text_str += "## Tickler\n\n" + TICKLER_STR + "\n\n\n"

    guide_text_str += "## Next Actions\n\n" + NA_STR + "\n\n\n"
    guide_text_str += "## Projects\n\n" + PRJ_STR + "\n\n\n"

    guide_text_str += "## Contacts\n\n" + CONTACTS_STR + "\n\n\n"
    guide_text_str += "## Agendas\n\n" + AGENDAS_STR + "\n\n\n"

    guide_text_str += "## Focus and Direction\n\n\n"
    guide_text_str += "### Areas of Interest and Accountability\n\n" + AOI_STR + "\n\n\n"
    guide_text_str += "### Goals\n\n" + GOALS_STR + "\n\n\n"
    guide_text_str += "### Vision\n\n" + VISION_STR + "\n\n\n"
    guide_text_str += "### Purpose and Principles\n\n" + PURPOSE_AND_PRINCIPLES_STR + "\n\n\n"

    return guide_text_str

