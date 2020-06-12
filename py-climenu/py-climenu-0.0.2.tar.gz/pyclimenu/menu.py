"""Python module for creating menu in CLI"""

import math
from typing import Any, Callable, Dict, List, Optional


class BaseMenu(object):
    """Represents the base menu.

    This class is used to display a menu with automatic numbering and selection.
    This class is to be overridden by a new menu subclass that features menu
    items specific for its application.

    Attributes:
        name: Menu name used for title.
        display_exit: Bool to show exit option.
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
                 display_exit: Optional[bool] = True):
        """Inits BaseMenu."""
        self.menu_items: List[Dict[str, Any]] = []

        self.exit_text = BaseMenu.default_exit_text
        self.invalid_option_text = BaseMenu.default_invalid_option_text
        self.selection_text = BaseMenu.default_selection_text

        self.name = name
        self.display_exit = display_exit

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

    def display(self) -> None:
        """Method to be overridden by each menu subclass."""

    def get_selection(self, selection: int) -> Any:
        """Returns the menu item by index."""
        try:
            item = self.menu_items[selection - 1]
            return item
        except IndexError:
            raise IndexError

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

        if self.display_exit:
            print(f"{0:{width}}: {self.exit_text}")


class Menu(BaseMenu):
    """Represents a standard menu with menu option callbacks.

    Standard menu where each menu item will have a callback to be called when
    that menu option is selected.
    """
    def __init__(self, name: str):
        """Inits Menu"""
        super().__init__(name)

    def display(self) -> None:
        """Displays the menu and calls selected callback."""
        self.print()

        while (
                selection := int(input(self.selection_text.format(len(self))))
        ) != 0:
            try:
                item = self.get_selection(selection)
                item["value"]()
            except IndexError:
                print(self.invalid_option_text)

            self.print()


class BasicMenu(Menu):
    """Basic menu for simple implementations.

    Basic Menu can be used in lieu of Menu when the implementation does not
    require the menu instance to be kept once the menu has been exited.
    """
    def __init__(self,
                 name: Optional[str] = None,
                 items: Optional[Dict[str, Callable[[], None]]] = None):
        """Creates and displays the menu and menu items."""
        super().__init__(name)
        self.add_items(items)
        self.display()


class OptionMenu(BaseMenu):
    """Options menu for selecting an option and returns a value.

    Functions similar to HTML select element. Displays a list of options to
    return the selected value."""
    def __init__(self, name: str):
        """Inits OptionMenu"""
        super().__init__(name, display_exit=False)

    def display(self) -> Any:
        """Displays display text for each menu option.

        Returns:
            Value of the selected option.
        """
        self.print()

        while (
                selection := int(input(self.selection_text.format(len(self))))
        ) != 0:
            try:
                item = self.get_selection(selection)
                return item.value
            except IndexError:
                print(self.invalid_option_text)

            self.print()


class BasicOptionMenu(OptionMenu):
    """Basic option menu for simple implementations.

    Basic Option Menu can be used for a simple option menu where option menu
    items do not need to be stored and the selected value can be always
    accessed.

    Attributes:
        selection: Value of the selected option.
    """
    def __init__(
            self,
            name: Optional[str] = None,
            items: Optional[Dict[str, Any]] = None
    ):
        """Inits BasicOptionMenu"""
        super().__init__(name)
        self.add_items(items)
        self.selection = self.display()
