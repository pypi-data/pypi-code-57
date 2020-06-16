texts = {'Accept and Close', '', 'Next', 'Skip this question', 'See my matches', 'See More Matches'}
skip_text = {'', 'Next'}


def rows_filter(rows):
    """
    Keep pages and some clicks. Remove clicks made during quiz (they have either empty text or "Next").
    :param rows: user session
    :return: filtered user session
    """
    rows = [row for row in rows
            if (
                row.get('type', '') == 'page'
                or (row.get('event', '') in ('BG Click', 'BG Click2')
                    and row.get('bytegain', {}).get('clickText', '').strip() not in skip_text)
            )
            ]
    return rows