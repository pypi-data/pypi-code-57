from wagtail.images.models import Image
from ...cms import constants
from .mock import Mock


class MockEntries(Mock):

    def svg(self, size='m', bg=False, theme=constants.THEME_SPACE):
        ret = {
            'type': 'svg',
            'value': {
                'svg': {
                    'file': self.file(self.SVG_CUBE).id,
                    'size': size
                }
            }
        }
        ret['value'].update(self.base(bg=bg, theme=theme))
        return ret

    def image(self, size='m', bg=False, theme=constants.THEME_SPACE):
        ret = {
            'type': 'image',
            'value': {
                'image': {
                    'file': self.file(self.IMG_BLOG, model=Image).id,
                    'size': size
                }
            }
        }
        ret['value'].update(self.base(bg=bg, theme=theme))
        return ret

    def text(self, txt=None, size='big', align=None, bg=False, theme=constants.THEME_SPACE):
        ret = {
            'type': 'text',
            'value': {
                'text': {
                    'value': txt if txt else eval('self.' + size),
                },
                'align': align
            }
        }
        ret['value'].update(self.base(bg=bg, theme=theme, container='content'))
        return ret

    def media_text(self, reverse=False, bg=False, theme=constants.THEME_SPACE, size_media='m',
                   button_1=constants.BUTTON_GREEN_FULL, button_2=None, media='svg', align=None,
                   section=False):
        ret = {
            'type': 'media_text',
            'value': {
                'h2': self.h,
                'text': {
                    'value': self.normal
                },
                'media': [{
                    'type': media,
                    'value': {
                        'file': self.file(self.SVG_CUBE).id if media == 'svg' else self.file(self.IMG_BLOG,
                                                                                             model=Image).id,
                        'size': size_media
                    },
                }],
                'buttons': [],
                'reverse': reverse,
                'align': align,
                'section': section
            }
        }
        ret['value'].update(self.base(bg=bg, theme=theme))
        if button_1:
            ret['value']['buttons'].append({
                'type': 'button',
                'value': self.button(button_1)
            })
        if button_2:
            ret['value']['buttons'].append({
                'type': 'button',
                'value': Mock.button(m_type=button_2)
            })
        return ret

    def cards(self, stop=None, container='full', bg=False, theme=constants.THEME_SPACE, card='freelance',
              carousel=True):
        ret = {
            'type': 'cards',
            'value': {
                'cards': [],
                'carousel': carousel
            }
        }
        card_freelance = [58, 58, 58, 58, 58, 58, 58]
        card_feature = [58, 58, 58, 58, 58, 58, 58]
        card_service = [58, 58, 58, 58, 58, 58, 58]

        cci = {
            'svg': {
                'file': self.file(self.SVG_CUBE).id,
                'size': 'm'
            },
            'text': {
                'value': self.small,
                'align': 'center'
            },
            'button': self.button(constants.BUTTON_WHITE_LIGHT)
        }
        card_custom = [cci, cci, cci, cci, cci, cci, cci]

        i = 0
        for card_item in eval('card_' + card):
            if not carousel and stop and i == stop:
                break
            ret['value']['cards'].append({
                'type': card,
                'value': {
                    card: card_item
                }
            })
            if card == 'custom':
                ret['value']['cards'][i]['value'] = card_item
            i += 1

        ret['value'].update(self.base(bg=bg, theme=theme, container=container, padding=True))
        return ret

    def first_content(self, align='left', bg=False, theme=constants.THEME_SPACE, button_1=constants.BUTTON_GREEN_LIGHT,
                      button_2=constants.BUTTON_GREEN_FULL):
        ret = {
            'type': 'first_content',
            'value': {
                'h1': self.h,
                'text': {
                    'value': self.text_first_content,
                },
                'buttons': [{
                    'type': 'button',
                    'value': self.button(button_1)
                }, {
                    'type': 'button',
                    'value': self.button(button_2)
                }],
                'align': align
            }
        }
        ret['value'].update(self.base(bg=bg, theme=theme, container='regular'))
        return ret

    def cta(self):
        ret = {
            'type': 'cta',
            'value': {}
        }
        return ret

    def contact_freelance(self):
        ret = {
            'type': 'contact_freelance',
            'value': {}
        }
        return ret

    def jobs_popular(self):
        ret = {
            'type': 'jobs_popular',
            'value': {}
        }
        return ret

    def timeline(self, bg=False, theme=constants.THEME_SPACE):
        item = {
            'type': 'text',
            'value': {
                'value': self.xs
            }
        }
        ret = {
            'type': 'timeline',
            'value': {
                'items': [
                    item,
                    item,
                    item,
                    item,
                    item
                ]
            }
        }
        ret['value'].update(self.base(bg=bg, theme=theme, container='content'))
        return ret

    def grid_info(self, bg=False, theme=constants.THEME_SPACE_INVERSE):
        info = {
            'type': 'svg_info',
            'value': {
                'file': self.file(self.SVG_CUBE).id,
                'title': self.h,
                'text_hover': {
                    'value': self.xs
                }
            }
        }
        ret = {
            'type': 'grid_info',
            'value': {
                'infos': [
                    info,
                    info,
                    info,
                    info,
                    info,
                    info,
                ]
            }
        }
        ret['value'].update(self.base(bg=bg, theme=theme, container='regular'))
        return ret

    def medias_line(self, nb_media=6, bg=False, theme=constants.THEME_SPACE_INVERSE):
        media = {
            'type': 'svg_label',
            'value': {
                'file': self.file(self.SVG_CUBE).id,
                'label': self.h,
            }
        }
        i = 0
        medias = []
        while i < nb_media:
            medias.append(media)
            i += 1
        ret = {
            'type': 'medias_line',
            'value': {
                'medias': medias
            }
        }
        ret['value'].update(self.base(bg=bg, theme=theme, container='full'))
        return ret

    def buttons(self, align='left', bg=False, theme=constants.THEME_SPACE):
        ret = {
            'type': 'buttons',
            'value': {
                'buttons': [
                    {
                        'type': 'button',
                        'value': self.button(constants.BUTTON_WHITE_FULL)
                    },
                    {
                        'type': 'button',
                        'value': self.button(constants.BUTTON_WHITE_LIGHT)
                    },
                ],
                'align': align
            }
        }
        ret['value'].update(self.base(bg=bg, theme=theme, container='content'))
        return ret
