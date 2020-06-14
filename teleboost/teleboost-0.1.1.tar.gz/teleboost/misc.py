import re

from random_user_agent.user_agent import UserAgent  # type: ignore

user_agent_provider = UserAgent()

key_re = re.compile(r"data-view=\"(\S*)\"")
post_url_re = re.compile(r"http(?:s|)://\S*/(.*)/(\d*)")
