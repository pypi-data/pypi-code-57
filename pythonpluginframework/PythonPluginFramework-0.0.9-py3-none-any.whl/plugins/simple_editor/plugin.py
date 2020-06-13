

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.Qsci import QsciScintilla, QsciLexerPython

context = None
def init(context_):
    global context
    context = context_


class SimpleEditorWidget(QTextEdit):
    def __init__(self, parent):
        super().__init__(parent)
        self.selAllShort = QShortcut(QKeySequence("Ctrl+s"), self)
        self.selAllShort.activated.connect(self.on_save)

    def on_init(self, node):
        self._node = node
        value = node.get_prop('key2')
        self.setText(value)
        print("on_init:", value)
        return ""
    def on_save(self):
        value = self.toPlainText()
        self._node.set_prop('key2', value)
        print("on_save:", value)
        return ""
    def on_close(self):
        print("on close...")
        return ""

class SimplePythonEditor(QsciScintilla):
    ARROW_MARKER_NUM = 8

    def __init__(self, parent=None):
        super(SimplePythonEditor, self).__init__(parent)

        # Set the default font
        font = QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(10)
        self.setFont(font)
        self.setMarginsFont(font)

        # Margin 0 is used for line numbers
        fontmetrics = QFontMetrics(font)
        self.setMarginsFont(font)
        self.setMarginWidth(0, fontmetrics.width("00000") + 6)
        self.setMarginLineNumbers(0, True)
        self.setMarginsBackgroundColor(QColor("#cccccc"))

        # Clickable margin 1 for showing markers
        self.setMarginSensitivity(1, True)
        self.marginClicked.connect(self.on_margin_clicked)
        #self.connect(self,
        #    SIGNAL('marginClicked(int, int, Qt::KeyboardModifiers)'),
        #    self.on_margin_clicked)
        self.markerDefine(QsciScintilla.RightArrow,
            self.ARROW_MARKER_NUM)
        self.setMarkerBackgroundColor(QColor("#ee1111"),
            self.ARROW_MARKER_NUM)

        # Brace matching: enable for a brace immediately before or after
        # the current position
        #
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        # Current line visible with special background color
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#ffe4e4"))

        # Set Python lexer
        # Set style for Python comments (style number 1) to a fixed-width
        # courier.
        #
        lexer = QsciLexerPython()
        lexer.setDefaultFont(font)
        self.setLexer(lexer)
        #print(QsciScintilla.SCI_STYLESETFONT)
        #self.SendScintilla(QsciScintilla.SCI_STYLESETFONT, 1, 'Courier')
        self.SendScintilla(QsciScintilla.SCI_STYLESETFONT, 1)

        # Don't want to see the horizontal scrollbar at all
        # Use raw message to Scintilla here (all messages are documented
        # here: http://www.scintilla.org/ScintillaDoc.html)
        self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)

        # not too small
        self.setMinimumSize(600, 450)

    def on_margin_clicked(self, nmargin, nline, modifiers):
        # Toggle marker for the line the margin was clicked on
        if self.markersAtLine(nline) != 0:
            self.markerDelete(nline, self.ARROW_MARKER_NUM)
        else:
            self.markerAdd(nline, self.ARROW_MARKER_NUM)

    def on_init(self, node):
        self._node = node
        self.setText(open(__file__).read())
        return ""
    def on_save(self):
        return ""
    def on_close(self):
        return ""

class EditorExtension:
    def data_kind(self):
        return ['Project']
    def is_match_data(self, node):
        if node.get_kind() == 'Project':
            return True
        else:
            return False
    def create_editor(self, parent):
        return SimplePythonEditor(parent)


config = {
    'pluginid': 'UI::Core::SimpleEditor',
    "extensions" : [
        {
            "name": "PL::Basic::Editor",
            "impl": EditorExtension()
        }
    ]
}