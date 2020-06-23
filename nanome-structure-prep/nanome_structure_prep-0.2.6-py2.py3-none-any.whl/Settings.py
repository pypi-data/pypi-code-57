import nanome
import os
import re

MENU_PATH = os.path.join(os.path.dirname(__file__), 'json/Settings.json')
OFF_ICON_PATH = os.path.join(os.path.dirname(__file__), 'assets/off.png')
ON_ICON_PATH = os.path.join(os.path.dirname(__file__), 'assets/on.png')

class Settings():
    def __init__(self, plugin, on_close):
        self.__plugin = plugin
        self.__menu = nanome.ui.Menu.io.from_json(MENU_PATH)
        self.__menu.register_closed_callback(on_close)

        # layout node setup (bonds)
        ln_btn_bonds = self.__menu.root.find_node('Bonds Button')
        btn_bonds = ln_btn_bonds.get_content()
        btn_bonds.icon.active = True
        btn_bonds.icon.value.set_all(OFF_ICON_PATH)
        btn_bonds.icon.value.selected = ON_ICON_PATH
        btn_bonds.icon.value.selected_highlighted = ON_ICON_PATH
        btn_bonds.selected = True

        # button config (bonds)
        btn_bonds.outline.active = False
        btn_bonds.name = ln_btn_bonds.name
        btn_bonds.register_pressed_callback(self.set_option)

        # layout node setup (dssp)
        ln_btn_dssp = self.__menu.root.find_node('DSSP Button')
        btn_dssp = ln_btn_dssp.get_content()
        btn_dssp.icon.active = True
        btn_dssp.icon.value.set_all(OFF_ICON_PATH)
        btn_dssp.icon.value.selected = ON_ICON_PATH
        btn_dssp.icon.value.selected_highlighted = ON_ICON_PATH
        btn_dssp.selected = True

        # button config (dssp)
        btn_dssp.outline.active = False
        btn_dssp.name = ln_btn_dssp.name
        btn_dssp.register_pressed_callback(self.set_option)

        self.use_bonds = True
        self.use_dssp = True

        btn_bonds.selected = self.use_bonds
        btn_dssp.selected = self.use_dssp

    def open_menu(self):
        self.__menu.enabled = True
        self.__plugin.menu = self.__menu
        self.__plugin.update_menu(self.__plugin.menu)

    def set_option(self, button):
        button.selected = not button.selected
        option_name = 'bonds' if 'bonds' in button.name.lower() else 'dssp'
        setattr(self, 'use_' + option_name, button.selected)
        self.__plugin.update_content(button)
