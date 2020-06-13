"""Python module for creating menu in CLI"""

import math
from typing import Any, Callable, Dict, List, Optional, Type


class BaseMenu:
    """Represents the base menu.

    This class is used to display a menu with automatic numbering and selection.
    This class is to be overridden by a new menu subclass that features menu
    items specific for its application.

    Attributes:
        name: Menu name used for title.
        exit_option: Bool to show exit option.
        menu_items: List of menu items.
        exit_text: Text to be displayed for exit option.
        invalid_option_text: Text to be displayed when an invalid option is
        selected.
        selection_text: Text to be displayed as selection prompt.
    """
    default_exit_text: str = "Exit"
    default_invalid_option_text: str = "Invalid option"
    default_selection_text: str = "Please select an option [0-{}]: "

    def __init__(self,
                 name: Optional[str] = None,
                 exit_option: Optional[bool] = True):
        """Inits BaseMenu."""
        self.menu_items: List[Dict[str, Any]] = []
        self.selection: Any = None

        self.exit_text = BaseMenu.default_exit_text
        self.invalid_option_text = BaseMenu.default_invalid_option_text
        self.selection_text = BaseMenu.default_selection_text

        self.name = name
        self.exit_option = exit_option

    def __len__(self) -> int:
        """Returns number of menu items."""
        return len(self.menu_items)

    def add_item(self, display: str, value: Any) -> None:
        """Adds a menu item to menu item list."""
        self.menu_items.append({"display": display, "value": value})

    def add_items(self, items: Dict[str, Any]) -> None:
        """Adds a list of menu items to menu item list."""
        for display, value in items.items():
            self.add_item(display, value)

    def display(self) -> Any:
        """Method to be overridden by each menu subclass."""
        self.selection = self.menu()
        return self.selection

    def get_selection(self, selection: int) -> Any:
        """Returns the menu item by index."""
        try:
            item = self.menu_items[selection - 1]
            return item
        except IndexError:
            raise IndexError

    def menu(self) -> Any or None:
        """Shows the menu and returns the selected item

        Returns:
            Value of selected item
        """
        while True:
            self.print()

            selection = self.prompt_selection()
            if selection == 0 and self.exit_option:
                return None
            try:
                item = self.get_selection(selection)
                return item["value"]
            except IndexError:
                print(self.invalid_option_text)

    def print(self) -> None:
        """Displays all the menu options for selection.

        Displays the menu title, all the menu options, and an exit option if
        flag is set.
        """
        width = math.floor(math.log(len(self), 10)) + 1

        print("\n")

        if self.name is not None:
            print(self.name)

        for i, menu_item in enumerate(self.menu_items, start=1):
            print(f"{i:{width}}: {menu_item['display']}")

        if self.exit_option:
            print(f"{0:{width}}: {self.exit_text}")

    def prompt_selection(self) -> int:
        """Prompt user for selection

        Returns:
            Number of selection
        """
        return int(input(self.selection_text.format(len(self))))


class BaseBasicMenu(BaseMenu):
    """Basic Base menu for simple implementations of menus.

    Can be override in conjunction with a menu type, or the menu type can be
    passed in to create an instance.
    """
    def __init__(self,
                 name: Optional[str] = None,
                 items: Optional[Dict[str, Any]] = None):
        super().__init__(name)
        self.add_items(items)
        self.display()


class Menu(BaseMenu):
    """Represents a standard menu with menu option callbacks.

    Standard menu where each menu item will have a callback to be called when
    that menu option is selected.
    """
    def add_item(self, display: str, value: Callable[[], None]) -> None:
        super().add_item(display, value)

    def display(self) -> None:
        while super().display() is not None:
            self.selection()


class BasicMenu(BaseBasicMenu, Menu):
    """Basic menu for simple implementations.

    Basic Menu can be used in lieu of Menu when the implementation does not
    require the menu instance to be kept once the menu has been exited.
    """
    def __init__(self,
                 name: Optional[str] = None,
                 items: Optional[Dict[str, Callable[[], None]]] = None):
        """Creates and displays the menu and menu items."""
        super().__init__(name, items)


class OptionMenu(BaseMenu):
    """Options menu for selecting an option and returns a value.

    Functions similar to HTML select element. Displays a list of options to
    return the selected value."""
    def __init__(self, name: str):
        """Inits OptionMenu"""
        super().__init__(name, exit_option=False)

    def display(self) -> Any:
        super().display()
        return self.selection


class BasicOptionMenu(BaseBasicMenu, OptionMenu):
    """Basic option menu for simple implementations.

    Basic Option Menu can be used for a simple option menu where option menu
    items do not need to be stored and the selected value can be always
    accessed.
    """
