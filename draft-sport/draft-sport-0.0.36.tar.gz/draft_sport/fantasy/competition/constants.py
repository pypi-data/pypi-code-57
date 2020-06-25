"""
Draft Sport Python
Competition Constants Module
author: hugh@blinkybeach.com
"""
from draft_sport.fantasy.competition.competition import Competition


class CompetitionConstants:

    DRAFT_RUGBY_2020 = Competition(
        public_id='sru_2020_2',
        name='Draft Rugby 2020'
    )

    DRAFT_RUGBY_2020_PRE_COVID = Competition(
        public_id='sru_2020_1',
        name='Draft Rugby 2020 (Pre-Covid)'
    )
