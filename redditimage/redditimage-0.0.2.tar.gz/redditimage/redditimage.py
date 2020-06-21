from typing import Optional
import time

from PIL import Image, ImageDraw, ImageFont

from .utils import pil_utils as piu
from .utils import reddit_image_utils as riu

from .compact_image import CompactImage
from .models.relative_position import RelativePosition
# from .pil_utils import text_wrap, image, text_image

class RedditImage:

    def create_title(
        self,
        title: str,
        upvotes: int,
        sub: str,
        poster_username: str,
        timestamp: float,
        width: int
    ) -> Image:
        sub_font    = ImageFont.truetype(FONT_PATH_BOLDEST, FONT_SIZE_HEADER)
        header_font = ImageFont.truetype(FONT_PATH_BOLD,    FONT_SIZE_HEADER)
        title_font  = ImageFont.truetype(FONT_PATH_BOLD,    FONT_SIZE_TITLE)

        votes_img = self.__votes_image(64, upvotes=upvotes)
        ci = CompactImage(DISTANCE, PADDING, bg_color=COLOR_BG, image=votes_img)

        sub_img = piu.text_image(riu.sub(sub), sub_font, fg_color=COLOR_TEXT_LIGHT, wrap_instead_of_font_downscale=False)
        ci.add_image(sub_img, positioned=RelativePosition.Right, to_image=votes_img, extra_distance_x=int(1.5*DISTANCE))

        header_str = '· Posted by ' + riu.username(poster_username) + ' · ' + riu.date_text(timestamp) + ' ago'
        header_img = piu.text_image(header_str, header_font, height=sub_img.size[1], fg_color=COLOR_TEXT_DARK,wrap_instead_of_font_downscale=False)
        ci.add_image(header_img, positioned=RelativePosition.Right, to_image=sub_img, centered=True)

        title_img = piu.text_image(title, title_font, width=width-votes_img.size[0] - 2*PADDING - DISTANCE, fg_color=COLOR_TEXT_LIGHT, wrap_instead_of_font_downscale=True)
        ci.add_image(title_img, positioned=RelativePosition.Bottom, to_image=sub_img)
        ci.add_image(self.__footer_img, positioned=RelativePosition.Bottom, to_image=title_img)

        return ci.render(width=width)

    def create_subtitle(
        self,
        subtitle: str,
        width: int
    ) -> Image:
        return CompactImage(
            DISTANCE,
            2*PADDING,
            bg_color=COLOR_BG, 
            image=piu.text_image(
                subtitle,
                ImageFont.truetype(FONT_PATH_BOLD, FONT_SIZE_SUBTITLE),
                fg_color=COLOR_TEXT_LIGHT,
                wrap_instead_of_font_downscale=True,
                width=width - 4*PADDING
            )
        ).render(width=width)

    def create_thumbnail(
        self,
        title: str,
        sub: str,
        image_overlay_path: str,
        width: int = 1920,
        height: int = 1080
    ) -> Image:
        from colorthief import ColorThief
        overlay_len_perc = 0.4
        text_len_perc = 1.0 - overlay_len_perc
        overlay = piu.resized(Image.open(image_overlay_path).convert("RGBA"), width=int(float(width)*overlay_len_perc), height=height - PADDING_THUMBNAIL)
        # dominant_color = ColorThief(image_overlay_path).get_color(quality=1)
        # print(dominant_color)
        dominant_color = riu.saturate_color(ColorThief(image_overlay_path).get_color(quality=1))

        bg_img = piu.image(width, height, COLOR_BG)
        bg_img.paste(overlay, (width-overlay.size[0], height-overlay.size[1]), overlay)

        sub_img = piu.text_image(riu.sub(sub), ImageFont.truetype(FONT_PATH_THUMBNAIL, FONT_SIZE_THUMBNAIL_SUB), fg_color=COLOR_TEXT_LIGHT, wrap_instead_of_font_downscale=False)
        ci = CompactImage(
            DISTANCE,
            PADDING_THUMBNAIL,
            sub_img
        )

        # halo_col = (0, 0, 0)   # black
        # halo_col = (255, 255, 255)

        title_img = piu.text_image(
            title,
            ImageFont.truetype(FONT_PATH_THUMBNAIL, FONT_SIZE_THUMBNAIL_TITLE),
            fg_color=dominant_color,
            wrap_instead_of_font_downscale=True,
            width=int(float(width)*text_len_perc) - PADDING_THUMBNAIL - DISTANCE,
            height=height - sub_img.size[1] - PADDING_THUMBNAIL - DISTANCE,
            # halo_color=halo_col#(255, 255, 255, 255)
        )
        title_img_extra_distance_y = int((float(height - PADDING_THUMBNAIL - DISTANCE - sub_img.size[1]) - title_img.size[1])/2)

        ci.add_image(title_img, positioned=RelativePosition.Bottom, to_image=sub_img, extra_distance_y=title_img_extra_distance_y)
        rendered = ci.render(width=int(float(width)*text_len_perc) - DISTANCE, height=height)

        bg_img.paste(rendered, (0,0), rendered)

        return bg_img

    def create_comment(
        self,
        content: str,
        upvotes: int,
        poster_username: str,
        timestamp: float,
        width: int,
        comment_level: int = 0
    ) -> Image:
        username_font   = ImageFont.truetype(FONT_PATH_BOLDEST, FONT_SIZE_HEADER)
        header_font     = ImageFont.truetype(FONT_PATH_BOLD,    FONT_SIZE_HEADER)
        comment_font    = ImageFont.truetype(FONT_PATH_REGULAR, FONT_SIZE_COMMENT)

        votes_img = self.__votes_image(40)
        ci = CompactImage(DISTANCE, PADDING, bg_color=COLOR_BG)
        ci.add_image(votes_img, extra_distance_x=comment_level*COMMENT_OFFSET)

        username_img = piu.text_image(riu.username(poster_username), username_font, fg_color=COLOR_TEXT_LIGHT, wrap_instead_of_font_downscale=False)
        ci.add_image(username_img, positioned=RelativePosition.Right, to_image=votes_img, extra_distance_x=int(1.5*DISTANCE))

        header_img = piu.text_image(riu.number_text(upvotes) + ' points · ' + riu.date_text(timestamp) + ' ago', header_font, height=username_img.size[1], fg_color=COLOR_TEXT_DARK,wrap_instead_of_font_downscale=False)
        ci.add_image(header_img, positioned=RelativePosition.Right, to_image=username_img, centered=True)

        content_img = piu.text_image(content, comment_font, width=width-votes_img.size[0] - 2*PADDING - DISTANCE, fg_color=COLOR_TEXT_LIGHT, wrap_instead_of_font_downscale=True)
        ci.add_image(content_img, positioned=RelativePosition.Bottom, to_image=username_img)
        ci.add_image(self.__footer_img, positioned=RelativePosition.Bottom, to_image=content_img)

        return ci.render(width=width)


    @property
    def __footer_img(self) -> Image:
        try:
            return self.___footer_img
        except AttributeError:
            self.___footer_img = piu.text_image(
                'Reply   Give Award   Share   Report   Save',
                ImageFont.truetype(FONT_PATH_BOLD, FONT_SIZE_HEADER),
                fg_color=COLOR_TEXT_DARK,
                wrap_instead_of_font_downscale=False
            )

            return self.___footer_img

    @staticmethod
    def __votes_image(width: int, upvotes: Optional[int] = None) -> Image:
        img_upvote = Image.open(IMAGE_PATH_UPVOTE)
        img_upvote.thumbnail((width, width), Image.ANTIALIAS)
        img_downvote = Image.open(IMAGE_PATH_DOWNVOTE)
        img_downvote.thumbnail((width, width), Image.ANTIALIAS)

        ci = CompactImage(DISTANCE, 0, image=img_upvote)

        img_votes = None

        if upvotes is not None:
            img_votes = piu.text_image(
                riu.number_text(upvotes),
                ImageFont.truetype(FONT_PATH_BOLDEST, FONT_SIZE_VOTES),
                width=int(float(width)*1.5),
                fg_color=COLOR_TEXT_LIGHT,
                wrap_instead_of_font_downscale=False,
                align='center'
            )

            ci.add_image(img_votes, positioned=RelativePosition.Bottom, to_image=img_upvote, centered=True)

        ci.add_image(img_downvote, positioned=RelativePosition.Bottom, to_image=img_votes if img_votes is not None else img_upvote, centered=True)

        return ci.render()


def __path(sub_path: str) -> str:
    import os

    return os.path.join(os.path.dirname(os.path.abspath(__file__)), sub_path)

# RESOURCES PATHS
    # FOLDERS
__RESOURCES_PATH        = 'resources'
__FONTS_RESOURCES_PATH  = __RESOURCES_PATH + '/' + 'fonts'
__IMAGES_RESOURCES_PATH = __RESOURCES_PATH + '/' + 'images'
    # FONTS
FONT_PATH_REGULAR       = __path(__FONTS_RESOURCES_PATH + '/regular.ttf')
FONT_PATH_BOLD          = __path(__FONTS_RESOURCES_PATH + '/bold.ttf')
FONT_PATH_BOLDEST       = __path(__FONTS_RESOURCES_PATH + '/boldest.ttf')
FONT_PATH_THUMBNAIL     = __path(__FONTS_RESOURCES_PATH + '/thumbnail.ttf')
    # IMAGES
IMAGE_PATH_UPVOTE       = __path(__IMAGES_RESOURCES_PATH + '/up.png')
IMAGE_PATH_DOWNVOTE     = __path(__IMAGES_RESOURCES_PATH + '/down.png')

# FONT SIZES
FONT_SIZE_HEADER    = 24
FONT_SIZE_TITLE     = 50
FONT_SIZE_SUBTITLE  = 28
FONT_SIZE_COMMENT   = 28
FONT_SIZE_VOTES     = 30

FONT_SIZE_THUMBNAIL_SUB     = 100
FONT_SIZE_THUMBNAIL_TITLE   = 150

# COLORS
COLOR_BG            = (20, 20, 21, 255)
COLOR_TEXT_LIGHT    = (205, 209, 212)
COLOR_TEXT_DARK     = (109, 112, 113)

# DISTANCES
DISTANCE            = 10
PADDING             = 2*DISTANCE
PADDING_THUMBNAIL   = 5*DISTANCE
COMMENT_OFFSET      = 10*DISTANCE