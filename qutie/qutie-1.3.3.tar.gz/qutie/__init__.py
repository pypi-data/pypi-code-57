"""Yet another pythonic UI library for rapid prototyping using
[PyQt5](https://pypi.org/project/PyQt5/).

Qutie (pronounced as _cutie_) provides a simple and easy to use pythonic
interface to [PyQt5](https://pypi.org/project/PyQt5/).

## Quick start

```python
import qutie as ui

app = ui.Application()
window = ui.Widget(
    title="Example",
    icon='orange',
    width=320,
    height=240,
    layout=ui.Column(
        ui.Label("Hello world!", color='blue'),
        ui.Row(
            ui.Button("Click!", clicked=lambda: ui.show_info(text="Hello world!")),
            ui.Button("Quit", clicked=app.quit)
        )
    )
)
window.show()
app.run()
```

## Pythonic API

### Iterables

`list.List`s, `tree.Tree`s and `table.Table`s behave like ```iterators```,
providing ```list```-like methods for access and manipulation.

>>> for item in tree:
...     item[0].color = 'red'
>>> tree[0].value = "spam"
>>> tree.append(["eggs"])
>>> tree.insert(0, ["ham"])
>>> tree.remove(tree[0])
>>> tree.index(tree[0])
0
>>> len(tree)
1

### Events

Any callable class property can be an event, events can emit any kind of
positional and keysword arguments.

>>> widget.my_event = lambda message: print(message)
>>> widget.emit('my_event', "Cheese shop")

### Something missing?

Any underlying PyQt5 instance can be accessed directly using property ```qt```.

>>> widget.qt.setWindowTitle("Spam!")
>>> widget.qt.customContextMenuRequested.conenct(lambda pos: None)

"""

from .action import *
from .application import *
from .button import *
from .checkbox import *
from .combobox import *
from .dialog import *
from .frame import *
from .groupbox import *
from .icon import *
from .label import *
from .layout import *
from .list import *
from .mainwindow import *
from .menu import *
from .messagebox import *
from .number import *
from .object import *
from .pixmap import *
from .progressbar import *
from .scrollarea import *
from .settings import *
from .splitter import *
from .stack import *
from .table import *
from .tabs import *
from .text import *
from .textarea import *
from .tree import *
from .widget import *
from .worker import *

__version__ = '1.3.3'
