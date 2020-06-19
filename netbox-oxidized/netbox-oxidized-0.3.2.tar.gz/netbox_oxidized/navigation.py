from extras.plugins import PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices

menu_items = (
    PluginMenuItem(
        link='plugins:netbox_oxidized:oxidizednode_list',
        link_text = 'Nodes',
        permissions = [],
        buttons = (
            PluginMenuButton(
                link='plugins:netbox_oxidized:oxidizednode_add',
                title='Add a new node',
                icon_class='fa fa-plus',
                color=ButtonColorChoices.GREEN,
                permissions=['netbox_oxidized.add_oxidizednode']
            ),
            #TODO create bulk CSV import
            PluginMenuButton(
                link='plugins:netbox_oxidized:oxidizednode_list',
                title='Import',
                icon_class='fa fa-download',
                color=ButtonColorChoices.BLUE,
                permissions=['netbox_oxidized.add_oxidizednode']
            ),
        )
    ),
    PluginMenuItem(
        link='plugins:netbox_oxidized:importnode_list',
        link_text = 'Import Oxidized',
        permissions = []
    ),
)