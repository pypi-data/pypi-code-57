import django_tables2 as tables
from django_tables2.utils import A, Accessor

from utilities.tables import BaseTable as NetboxBaseTable, ToggleColumn
from .models import OxidizedNode

class BaseTable(tables.Table):
    class Meta():
        attrs = {
            'class': 'table table-hover table-headings',
        }

    def __init__(self, *args, columns=None, **kwargs):
        super().__init__(*args, **kwargs)

        # Hide non-default columns
        default_columns = getattr(self.Meta, 'default_columns', list())
        if default_columns:
            for column in self.columns:
                if column.name not in default_columns:
                    self.columns.hide(column.name) 

               
    @property
    def configurable_columns(self):
        selected_columns = [
            (name, self.columns[name].verbose_name) for name in self.sequence if name not in ['pk','actions']
        ]
        available_columns = [
            (name, column.verbose_name) for name, column in self.columns.items() if name not in self.sequence and name not in ['pk','actions']
        ]
        return selected_columns + available_columns

    @property
    def visible_columns(self):
        return [name for name in self.sequence if self.columns[name].visible]

class OxidizedNodeTable(BaseTable):

    class Meta(BaseTable.Meta):
        default_columns =('pk','name','model','group','status', 'mtime', 'time')

    #name = tables.LinkColumn(viewname='plugins:netbox_oxidized:config-versions', args=[A('name')])
    pk = ToggleColumn(visible=True)
    name = tables.Column()
    fullname = tables.Column()
    ipaddress = tables.Column(verbose_name='IP Address')
    model = tables.Column()
    group = tables.Column()
    status = tables.Column()
    mtime = tables.Column(verbose_name='Last Modified')
    time = tables.Column(verbose_name='Last Checked')


class OxidizedNodeVersionTable(BaseTable):
    class Meta(BaseTable.Meta):
        default_columns =('version','date','message')

    version = tables.Column()
    date = tables.DateTimeColumn(format='Y-m-d H:i:s')
    author = tables.Column()
    message = tables.Column()
    

class OxidizedDeviceNodeTable(NetboxBaseTable):
    pk = ToggleColumn()
    name = tables.LinkColumn()
    ipaddress = tables.Column()
    node_model = tables.Column()
    group = tables.Column()
    device = tables.LinkColumn(viewname='dcim:device',args=[Accessor('device.pk')])

    class Meta(NetboxBaseTable.Meta):
        model = OxidizedNode
        default_columns = ('pk','name','ipaddress','node_model', 'group')
        fields = [ 'pk','name', 'ipaddress', 'node_model', 'group','device']
