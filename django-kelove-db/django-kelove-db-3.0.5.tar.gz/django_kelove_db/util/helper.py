# ==================================================================
#       文 件 名: helper.py
#       概    要: 助手工具
#       作    者: IT小强 
#       创建时间: 6/8/20 2:37 PM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

from importlib import import_module

from django.conf import settings

STATUS_CHOICES: list = [(-1, '草稿'), (0, '待审'), (1, '通过'), (2, '驳回')]

JSON_FIELD_SETTINGS: dict = {
    "mode": "code",
    "modes": ["code", "form", "text", "tree", "view", "preview"],
}
"""
* Markdown Editor
 * {
 * mode                 : "gfm",          // gfm or markdown
 * name                 : "",             // Form element name for post
 * value                : "",             // value for CodeMirror, if mode not gfm/markdown
 * theme                : "",             // Editor.md self themes, before v1.5.0 is CodeMirror theme, default empty
 * editorTheme          : "default",      // Editor area, this is CodeMirror theme at v1.5.0
 * previewTheme         : "",             // Preview area theme, default empty
 * markdown             : "",             // Markdown source code
 * appendMarkdown       : "",             // if in init textarea value not empty, append markdown to textarea
 * width                : "100%",
 * height               : "100%",
 * path                 : "./lib/",       // Dependents module file directory
 * pluginPath           : "",             // If this empty, default use settings.path + "../plugins/"
 * delay                : 300,            // Delay parse markdown to html, Uint : ms
 * autoLoadModules      : true,           // Automatic load dependent module files
 * watch                : true,
 * placeholder          : "Enjoy Markdown! coding now...",
 * gotoLine             : true,           // Enable / disable goto a line
 * codeFold             : false,
 * autoHeight           : false,
 * autoFocus            : true,           // Enable / disable auto focus editor left input area
 * autoCloseTags        : true,
 * searchReplace        : true,           // Enable / disable (CodeMirror) search and replace function
 * syncScrolling        : true,           // options: true | false | "single", default true
 * readOnly             : false,          // Enable / disable readonly mode
 * tabSize              : 4,
 * indentUnit           : 4,
 * lineNumbers          : true,           // Display editor line numbers
 * lineWrapping         : true,
 * autoCloseBrackets    : true,
 * showTrailingSpace    : true,
 * matchBrackets        : true,
 * indentWithTabs       : true,
 * styleSelectedText    : true,
 * matchWordHighlight   : true,           // options: true, false, "onselected"
 * styleActiveLine      : true,           // Highlight the current line
 * dialogLockScreen     : true,
 * dialogShowMask       : true,
 * dialogDraggable      : true,
 * dialogMaskBgColor    : "#fff",
 * dialogMaskOpacity    : 0.1,
 * fontSize             : "13px",
 * saveHTMLToTextarea   : false,          // If enable, Editor will create a <textarea name="{editor-id}-html-code"> tag save HTML code for form post to server-side.
 * disabledKeyMaps      : [],
 *
 * onload               : function() {},
 * onresize             : function() {},
 * onchange             : function() {},
 * onwatch              : null,
 * onunwatch            : null,
 * onpreviewing         : function() {},
 * onpreviewed          : function() {},
 * onfullscreen         : function() {},
 * onfullscreenExit     : function() {},
 * onscroll             : function() {},
 * onpreviewscroll      : function() {},
 *
 * imageUpload          : false,          // Enable/disable upload
 * imageFormats         : ["jpg", "jpeg", "gif", "png", "bmp", "webp"],
 * imageUploadURL       : "",             // Upload url
 * crossDomainUpload    : false,          // Enable/disable Cross-domain upload
 * uploadCallbackURL    : "",             // Cross-domain upload callback url
 *
 * toc                  : true,           // Table of contents
 * tocm                 : false,          // Using [TOCM], auto create ToC dropdown menu
 * tocTitle             : "",             // for ToC dropdown menu button
 * tocDropdown          : false,          // Enable/disable Table Of Contents dropdown menu
 * tocContainer         : "",             // Custom Table Of Contents Container Selector
 * tocStartLevel        : 1,              // Said from H1 to create ToC
 * htmlDecode           : false,          // Open the HTML tag identification
 * pageBreak            : true,           // Enable parse page break [========]
 * atLink               : true,           // for @link
 * emailLink            : true,           // for email address auto link
 * taskList             : false,          // Enable Github Flavored Markdown task lists
 * emoji                : false,          // :emoji: , Support Github emoji, Twitter Emoji (Twemoji);
 * // Support FontAwesome icon emoji :fa-xxx: > Using fontAwesome icon web fonts;
 * // Support Editor.md logo icon emoji :editormd-logo: :editormd-logo-1x: > 1~8x;
 * tex                  : false,          // TeX(LaTeX), based on KaTeX
 * flowChart            : false,          // flowChart.js only support IE9+
 * sequenceDiagram      : false,          // sequenceDiagram.js only support IE9+
 * previewCodeHighlight : true,           // Enable / disable code highlight of editor preview area
 *
 * toolbar              : true,           // show or hide toolbar
 * toolbarAutoFixed     : true,           // on window scroll auto fixed position
 * toolbarIcons         : "full",         // Toolbar icons mode, options: full, simple, mini, See `editormd.toolbarModes` property.
 * toolbarTitles        : {},
 * toolbarHandlers      : {
 * ucwords : function() {
 * return editormd.toolbarHandlers.ucwords;
 * },
 * lowercase : function() {
 * return editormd.toolbarHandlers.lowercase;
 * }
 * },
 * toolbarCustomIcons   : {               // using html tag create toolbar icon, unused default <a> tag.
 * lowercase        : "<a href=\"javascript:;\" title=\"Lowercase\" unselectable=\"on\"><i class=\"fa\" name=\"lowercase\" style=\"font-size:24px;margin-top: -10px;\">a</i></a>",
 * "ucwords"        : "<a href=\"javascript:;\" title=\"ucwords\" unselectable=\"on\"><i class=\"fa\" name=\"ucwords\" style=\"font-size:20px;margin-top: -3px;\">Aa</i></a>"
 * },
 * toolbarIconTexts     : {},
 *
 * lang : {  // Language data, you can custom your language.
 * name        : "zh-cn",
 * description : "开源在线Markdown编辑器<br/>Open source online Markdown editor.",
 * tocTitle    : "目录",
 * toolbar     : {
 * //...
 * },
 * button: {
 * //...
 * },
 * dialog : {
 * //...
 * }
 * //...
 * }
 * }
"""
EDITOR_MD_FIELD_SETTINGS: dict = {
    'readOnly': False,
    'theme': '',
    'previewTheme': '',
    'editorTheme': 'default',
    'autoFocus': False,
    'toolbarAutoFixed': False,
    'emoji': True,
    'codeFold': True,
    'tocDropdown': True,
    """
    添加以下配置，化身代码编辑器
    # 'watch': False,
    # 'toolbar': False,
    # 'mode': 'python'
     * 可选语言：
        text/html
        javascript
        php
        text/xml
        text/json
        clike
        javascript
        perl
        go
        python
        clike
        css
        ruby
    """
    'mode': 'markdown',
}


def load_object(path: str):
    """
    Load an object given its absolute object path, and return it.
    object can be a class, function, variable or an instance.
    path ie: 'scrapy.downloadermiddlewares.redirect.RedirectMiddleware'
    """

    dot = path.rindex('.')
    module, name = path[:dot], path[dot + 1:]
    mod = import_module(module)
    return getattr(mod, name)


def get_kelove_databases_settings(key: str = None, default=None):
    """
    获取配置
    :param key:
    :param default:
    :return:
    """
    try:
        kelove_databases_settings = settings.KELOVE_DATABASES
    except AttributeError:
        kelove_databases_settings = {}

    if not isinstance(kelove_databases_settings, dict):
        kelove_databases_settings = {}

    default_kelove_databases_settings = {
        'FOREIGN_DELETE_TYPE': 'django.db.models.deletion.PROTECT',
        'DB_CONSTRAINT': False,
        'DB_CONSTRAINT_USER': False,
        'USER_EDITABLE': False,
        'STATUS_CHOICES': STATUS_CHOICES,
        'DOC_TITLE': '数据库设计文档',
        'JSON_FIELD_SETTINGS': JSON_FIELD_SETTINGS,
        'EDITOR_MD_FIELD_SETTINGS': EDITOR_MD_FIELD_SETTINGS,
    }
    kelove_databases_settings = {**default_kelove_databases_settings, **kelove_databases_settings}

    if isinstance(kelove_databases_settings['FOREIGN_DELETE_TYPE'], str):
        kelove_databases_settings['FOREIGN_DELETE_TYPE'] = load_object(kelove_databases_settings['FOREIGN_DELETE_TYPE'])

    if key is None:
        return kelove_databases_settings
    else:
        return kelove_databases_settings.get(key, default)
