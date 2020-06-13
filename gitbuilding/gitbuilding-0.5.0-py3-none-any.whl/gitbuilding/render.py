"""
This contains GBRenderer, the class responsible for rendering processed markdown into HTML
It also contains the URLRules GitBuilding uses for HTML and some other helper functions.
"""

# This warning should be re-enabled once we find a better way to render that isn't
# piles of HTML in python strings.
# pylint: disable=line-too-long

import os
import codecs
import datetime
import re
import logging
from markdown import markdown
from gitbuilding.buildup import URLRules
from gitbuilding import utilities
from gitbuilding.buildup.buildup import IMAGE_REGEX

_LOGGER = logging.getLogger('BuildUp.GitBuilding')

class URLRulesHTML(URLRules):
    """
    The BuildUp URLRules used in GitBuilding for both the server and the static HTML.
    This is a child-class of buildup.URLRules with functions to strip off '.md' file
    extensions, rerouted stl links (for parts only) to markdown pages, and to replace
    empty links with "missing".
    """
    def __init__(self, rel_to_root=False):

        super(URLRulesHTML, self).__init__(rel_to_root=rel_to_root)
        def fix_missing(url):
            if url == "":
                return "missing"
            return url

        def stl_to_page(url):
            if url.endswith('.stl'):
                return url[:-4]
            return url

        def md_to_page(url):
            if url.endswith('.md'):
                return url[:-3]
            return url

        self.add_modifier(fix_missing)
        self.add_modifier(md_to_page)
        self.add_part_modifier(stl_to_page)


def _is_active_nav_item(nav_item, link):
    """
    Checks if the item in the navigation dictionary or any of the
     terms in the sub-navigation are the active page
    """
    if nav_item["link"] == link:
        return True
    if "subnavigation" in nav_item:
        for sub_nav_item in nav_item["subnavigation"]:
            if _is_active_nav_item(sub_nav_item, link):
                return True
    return False

def format_warnings(warnings):
    """
    Returns warnings for the live renderer to display
    """
    output = ""
    for warning in warnings:
        if warning["fussy"]:
            cssclass = "fussywarning"
            warntype = "FussyWarning"
        else:
            cssclass = "warning"
            warntype = "Warning"
        output += f'<p class="{cssclass}">{warntype}: {warning["message"]}</p>\n'
    return output

class GBRenderer:
    """
    This class is the renderer for GitBuilding HTML
    """

    def __init__(self, config, root="/"):

        self.config = config
        self.author_list = utilities.author_list(self.config)
        self.root = root
        self.custom_style = []
        self.custom_favicons = []
        # Variables that can be accessed by custom Footer/Header
        self.populate_vars()
        self.scan_assets()

    def populate_vars(self):
        """
        This function populates the list of variables that can be used in
        custom headers and footers
        """
        self.variables = {"title": self.config.title,
                          "year": datetime.datetime.now().year,
                          "root": self.root}

        self.variables["authors"] = self.author_list
        self.variables["email"] = self.config.email
        self.variables["affiliation"] = self.config.affiliation
        if self.config.license is None:
            self.variables["license"] = None
        else:
            if self.config.license_file is None:
                self.variables["license"] = self.config.license
            else:
                licence_url = self.config.license_file
                if licence_url.endswith('.md'):
                    licence_url = licence_url[:-3]
                self.variables["license"] = (f'<a href="{self.root}{licence_url}">'
                                             f'{self.config.license}</a>')

        for key in self.config.variables.keys():
            self.variables[key] = self.config.variables[key]

    def scan_assets(self):
        """
        This scans the assets folder of the project to look for custom CSS and favicons
        """
        if os.path.exists("assets"):
            for root, _, files in os.walk("assets"):
                for filename in files:
                    filepath = os.path.join(root, filename)
                    if filepath.endswith(".css"):
                        self.custom_style.append(filepath)
                    if filename == "favicon.ico":
                        self.custom_favicons.append(filepath)
                    if re.match(r"^favicon-[0-9]+x[0-9]+\.png$", filename):
                        self.custom_favicons.append(filepath)

    def safe_format(self, text, warn_intro="Problem formatting string - "):
        """
        Safely formats code as though it was an f-string but only allows a restricted variable set
        """

        # find all text inside braces
        matches = re.findall(r"((?<!\{)\{([^\{\}\n]+)\}(?!\}))", text)
        # Replace valid matches
        for match in matches:
            var = match[1].strip()
            if var in self.variables:
                text = text.replace(match[0], f"{self.variables[var]}")
            else:
                text = text.replace(match[0], "???")
                _LOGGER.warning('%s Variable "%s" not valid in this context.', warn_intro, var)

        # Find odd numbers of braces together

        cleantext = re.sub(r"(?<!\{)((?:\{\{)*)(\{)(?!\{)", r"\g<1>", text)
        cleantext = re.sub(r"(?<!\})((?:\}\})*)(\})(?!\})", r"\g<1>", cleantext)

        if not cleantext == text:
            _LOGGER.warning("%s Unmatched braces removed from format string", warn_intro)
        text = cleantext.replace("{{", "{")
        text = text.replace("}}", "}")

        return text

    def header(self, fullpage=True, nav=True, link=None, editorbutton=False):
        """
        This function returns the full top of the HTML page including the <head> section
        It includes the code from the project_header function and also the navigation.
        It opens the <div> for page content
        """

        output = ""
        if link is None:
            edlink = "editor"
        else:
            edlink = f"/{link}/editor"
        if fullpage:
            output += f"""<!DOCTYPE html>
<html>
<head>
    <title>{self.config.title}</title>
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">"""
            if self.custom_favicons:
                for favicon in self.custom_favicons:
                    if favicon.endswith("favicon.ico"):
                        output += f"""    <link rel="shortcut icon" href="{self.root}{favicon}" />"""
                    else:
                        output += f"""    <link rel="icon" type="image/png" href="{self.root}{favicon}" sizes="{re.findall('[0-9]+x[0-9]+',favicon)[-1]}" />"""
            else:
                output += f"""    <link rel="shortcut icon" href="{self.root}static/Logo/favicon.ico" />
    <link rel="icon" type="image/png" href="{self.root}static/Logo/favicon-32x32.png" sizes="32x32" />
    <link rel="icon" type="image/png" href="{self.root}static/Logo/favicon-16x16.png" sizes="16x16" />"""

            output += (f"""    <link href="{self.root}static/style.css" rel="stylesheet">\n""")

            for sheet in self.custom_style:
                output += f'    <link href="{self.root}{sheet}" rel="stylesheet">\n'
            output += f"""<script type="text/javascript" src="{self.root}static/3d-viewer.js"></script>
</head>
<body>"""
        else:
            for sheet in self.custom_style:
                output += f"""<style>{codecs.open(sheet, mode="r", encoding="utf-8").read()}</style>"""
        output += f"""<header class="site-header">
<div class="wrapper">
{self.project_header()}"""
        if editorbutton:
            output += f"""<div class=header-buttons><button onclick="window.location.href = '{edlink}';">Edit</button></div>"""
        output += """</div>
</header>
<div class="page-content">"""
        if nav and (len(self.config.navigation) > 0):
            output += f"""
            <div>
<nav class="sidebar">
    <a href="#" class="menu-icon">
    <svg viewBox="0 0 18 15">
        <path fill="#424242" d="M18,1.484c0,0.82-0.665,1.484-1.484,1.484H1.484C0.665,2.969,0,2.304,0,1.484l0,0C0,0.665,0.665,0,1.484,0 h15.031C17.335,0,18,0.665,18,1.484L18,1.484z"/>
        <path fill="#424242" d="M18,7.516C18,8.335,17.335,9,16.516,9H1.484C0.665,9,0,8.335,0,7.516l0,0c0-0.82,0.665-1.484,1.484-1.484 h15.031C17.335,6.031,18,6.696,18,7.516L18,7.516z"/>
        <path fill="#424242" d="M18,13.516C18,14.335,17.335,15,16.516,15H1.484C0.665,15,0,14.335,0,13.516l0,0 c0-0.82,0.665-1.484,1.484-1.484h15.031C17.335,12.031,18,12.696,18,13.516L18,13.516z"/>
    </svg>
    </a>
    <ul class="nav-list">
    {self.nav_links(link=link)}
    </ul>
</nav></div>"""
        output += """
<div class="wrapper">
"""
        return output

    def nav_links(self, link=None):
        """
        This function returns the side navigation
        """
        html = f'<li><a class="navhome" href="{self.root}">{self.config.title}</a></li>'
        for nav_item in self.config.navigation:
            li_class_txt = ""
            a_class_txt = ""
            if _is_active_nav_item(nav_item, link):
                li_class_txt = ' class="active"'
                if nav_item["link"] == link:
                    a_class_txt = 'class="active "'
            html += f'<li{li_class_txt}><a {a_class_txt}href="{self.root}{nav_item["link"]}">{nav_item["title"]}</a>'
            if "subnavigation" in nav_item:
                html += '<ul class="sub-nav-list">'
                for sub_nav_item in nav_item["subnavigation"]:
                    if _is_active_nav_item(sub_nav_item, link):
                        a_class_txt = 'class="active "'
                    else:
                        a_class_txt = ""
                    html += f'<li><a {a_class_txt}href="{self.root}{sub_nav_item["link"]}">{sub_nav_item["title"]}</a></li>'
                html += "</ul>"
            html += "</li>"
        return html

    def project_header(self):
        """
        This is the project header that can be customised.
        """
        html = "<div class=header-text>"
        if self.config.html_options.custom_header is not None:
            html += self.safe_format(self.config.html_options.custom_header,
                                     warn_intro="Problem formatting custom header - ")
        else:
            if self.config.title is not None:
                html += f'<a class="site-title" href="{self.root}">{self.config.title}</a>'
            if self.author_list is not None:
                html += '<p class="author">by '
                html += self.author_list
                html += "</p>"
            if self.config.affiliation is not None:
                html += f'<p class="affiliation">{self.config.affiliation}</p>'
        html += "</div>"
        return html

    def footer(self, fullpage=True):
        """
        This function closes the container div and includes the reference to GitBuilding (if used) and the
        project footer
        """
        gbpath = os.path.dirname(__file__)
        output = """</div>
</div>
<footer class="site-footer">
<div class="wrapper">"""
        if self.config.html_options.acknowledge_gitbuilding:
            output += f"""<a target="_blank" rel="noopener noreferrer" href="https://gitbuilding.io"><span class="icon">{codecs.open(os.path.join(gbpath,'static','Logo','GitBuilding.svg'), mode="r", encoding="utf-8").read()}</span>
<span class="info">Documentation powered by Git Building</span></a>"""
        output += f"""{self.project_footer()}
</div>
</footer>"""
        if fullpage:
            output += """</body>
</html>"""
        return output

    def project_footer(self):
        """
        This returns either the standard project footer or the customised footer
        """
        if self.config.html_options.custom_footer is not None:
            return self.safe_format(self.config.html_options.custom_footer,
                                    warn_intro="Problem formatting custom footer - ")
        html = ""
        if self.author_list is not None:
            html += '<p class="author">© '
            html += self.author_list
            html += f" {datetime.datetime.now().year}</p>"
        if self.config.email is not None:
            html += f'<p class="email">Contact: <a href="mailto:{self.config.email}">{self.config.email}</a></p>'
        if self.variables["license"] is not None:
            html += f'<p class="license">{self.config.title} is released under {self.variables["license"]}</p>'
        return html

    def render_md(self, md, link=None, fullpage=True, nav=True, editorbutton=False):
        """
        This function returns the rendered HTML for input markdown
        """

        # find more than one image on a line and replace with gallery
        imlines = re.findall(r'^((?:[ \t]*'+IMAGE_REGEX+'){2,}[ \t]*)$',
                             md,
                             re.MULTILINE)

        # imlines uses the IMAGE_REGEX which matches lots of groups. First is the whole line.
        imlines = [line[0] for line in imlines]
        for i, imline in enumerate(imlines):
            gallery = '\n\n<div class="gallery-thumb">'

            images = re.findall(IMAGE_REGEX, imline)

            for image in images:
                gallery += f"""<img onmouseover="getElementById('gallery-show{i}').src=this.src" src="{image[2]}" alt="{image[1]}" />"""

            gallery += f'</div><div class="gallery-show"><img id="gallery-show{i}" src="{images[0][2]}" alt="{images[0][1]}"/></div>'

            md = md.replace(imline, gallery)

        stls = re.findall(r"(^(\[[^\]]*\])\((.+?\.stl)\))", md, re.MULTILINE)
        for stl in stls:
            viewer_code = (f'{stl[1]}({stl[2]})\n'
                           f'<stl-part-viewer src="{stl[2]}" width="500" height="500"'
                           ' floorcolor="0xf1f1f1"></stl-part-viewer>')
            md = md.replace(stl[0],
                            viewer_code)

        content_html = markdown(md, extensions=["markdown.extensions.tables",
                                                "markdown.extensions.attr_list",
                                                "markdown.extensions.fenced_code"])
        return self.render(content_html,
                           link=link,
                           fullpage=fullpage,
                           nav=nav,
                           editorbutton=editorbutton)

    def render(self, html, link=None, fullpage=True, nav=True, editorbutton=False):
        """
        This function creates the full HTML page from the input HTML generated from BuildUp
        """

        output = self.header(fullpage=fullpage,
                             nav=nav,
                             link=link,
                             editorbutton=editorbutton)
        output += html
        output += self.footer(fullpage=fullpage)
        return output

    def missing_page(self):
        """
        This returns an HTML page for missing parts.
        """
        return self.render("<h1>Git Building Missing Part</h1>")

    def stl_page(self, stl_file):
        """
        This returns an HTML page with a live 3D view of the input STL file.
        """
        model_name = os.path.basename(os.path.splitext(stl_file)[0])
        stl_md = f"# {model_name}\n\n"
        stl_md += f"[Download STL]({self.root}{stl_file})\n\n"
        return self.render_md(stl_md,
                              os.path.splitext(stl_file)[0],
                              editorbutton=False)
