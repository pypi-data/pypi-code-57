"""
Draft Sport Python
Season Constants Module
author: hugh@blinkybeach.com
"""
from draft_sport.fantasy.season.season import Season
from draft_sport.fantasy.competition.constants import CompetitionConstants
from nozomi import NozomiDate


class SeasonConstants:

    DRAFT_RUGBY_2020 = Season(
        public_id='draft_rugby_2020',
        name='Draft Rugby 2020',
        start_date=NozomiDate(year=2020, month=7, day=4),
        competition=CompetitionConstants.DRAFT_RUGBY_2020
    )

    DRAFT_RUGBY_2020_PRE_COVID = Season(
        public_id='draft_rugby_2020_1',
        name='Draft Rugby 2020 (Pre-Covid)',
        start_date=NozomiDate(year=2020, month=2, day=5),
        competition=CompetitionConstants.DRAFT_RUGBY_2020_PRE_COVID
    )
