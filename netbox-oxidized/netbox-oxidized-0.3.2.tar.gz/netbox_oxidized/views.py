from django.shortcuts import get_object_or_404, render
from django.views.generic import View
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.conf import settings
from dcim.models import Device

import json
import requests
from urllib3.exceptions import InsecureRequestWarning
import logging
from datetime import datetime

from django_tables2 import RequestConfig
from utilities.paginator import EnhancedPaginator, get_paginate_count
from utilities.forms import TableConfigForm
from utilities.views import ObjectListView, ObjectEditView,ObjectDeleteView, BulkDeleteView

from .tables import *
from .forms import *
from .models import OxidizedNode
from .filters import *
from .utils import get_oxidized_nodeinfo



class OxidizedNodeListView(PermissionRequiredMixin, ObjectListView):

    permission_required = 'netbox_oxidized.view_oxidizednode'
    queryset = OxidizedNode.objects.prefetch_related('device')
    filterset = OxidizedNodeFilterSet
    filterset_form = OxidizedNodeFilterForm
    table = OxidizedDeviceNodeTable
    template_name = 'netbox_oxidized/node_list.html'
    action_buttons = ('add')
    model = OxidizedNode

class OxidizedNodeCreateView(PermissionRequiredMixin, ObjectEditView):
    permission_required = 'netbox_oxidized.add_oxidizednode'
    model = OxidizedNode
    model_form = OxidizedNodeForm
    template_name = 'netbox_oxidized/oxidizednode_edit.html'
    default_return_url = 'plugins:netbox_oxidized:oxidizednode_list'

class OxidizedNodeEditView(OxidizedNodeCreateView):
    permission_required = 'netbox_oxidized.edit_oxidizednode'

class OxidizedNodeBulkDeleteView(PermissionRequiredMixin, BulkDeleteView):
    permission_required = 'netbox_oxidized.delete_oxidizednode'
    queryset = OxidizedNode.objects.all()
    filterset = OxidizedNodeFilterSet
    table = OxidizedDeviceNodeTable
    default_return_url = 'plugins:netbox_oxidized:oxidizednode_list'

class OxidizedNodeDeleteView(PermissionRequiredMixin, ObjectDeleteView):
    permission_required = 'netbox_oxidized.delete_oxidizednode'
    model = OxidizedNode
    default_return_url = 'plugins:netbox_oxidized:oxidizednode_list'


class OxidizedNodeView(PermissionRequiredMixin, View):
    permission_required = 'netbox_oxidized.view_oxidizednode'


    def get(self, request, pk):
        version_data = []
        stat_data = {}
        version_data = []

        node = get_object_or_404(OxidizedNode.objects.all(), pk=pk)
        # get oxidized Live data
        oxidized_url = settings.PLUGINS_CONFIG['netbox_oxidized']['oxidized_url']

        if oxidized_url and oxidized_url != '':
            # retrieve node versions
            r = requests.get('{}/node/version?node_full={}&format=json'.format(oxidized_url,node.name, verify=False))
            if r.status_code == 200:
                data = r.json()
                for entry in data:
                    vid = len(data) - data.index(entry)
                    vdate = datetime.strptime(entry['date'], '%Y-%m-%d %H:%M:%S %z')
                    version_data.append({'version': vid, 'date': vdate, 'author': entry['author']['name'], 'message':entry['message']})
        
        data = get_oxidized_nodeinfo(oxidized_url, node.name, ssl_verify=False)
        if data and not data.get('error'):
            stat_data['time'] = data['last']['end']
            stat_data['runtime'] = round(float(data['last']['time']),2) 
            stat_data['status'] = data['last']['status']
            stat_data['mtime'] = data['mtime']
        else:
            stat_data['status'] = data['error']


        ##dummydata
        #version_data=[{'version': 1, 'date': '2020-05-21 12:00:00 +1000'}]
        #stat_data = {'time':'2020-05-21 12:00:00 +1000', 'runtime':'6', 'status':'success','mtime': '2020-05-21 12:00:00 +1000', 'version_count': len(version_data)}
        vtable = OxidizedNodeVersionTable(version_data)
        paginate = {
            'paginator_class': EnhancedPaginator,
            'per_page': get_paginate_count(request)
        }
        RequestConfig(request, paginate).configure(vtable)                
        return render(request, 'netbox_oxidized/node.html', {
            'node': node,
            'stat_data': stat_data,
            'version_table': vtable
            
        })

class OxidizedImportNodeListView(View):

    def get(self, request):
        table_data = []
        oxidized_url = settings.PLUGINS_CONFIG['netbox_oxidized']['oxidized_url']
        if oxidized_url and oxidized_url != '':
            r = requests.get('{}/{}'.format(oxidized_url,'nodes?format=json', verify=False))

            if r.status_code == 200:
                table_data = r.json()
            else:
                table_data = [
                    {'name': 'test', 'fullname':'test_data', 'ipaddress': '10.0.0.1', 'Model': 'Cisco', 'group': 'default', 'status': 'success', 'mtime':'2020-5-5', 'time':'2020-5-7'}
                ]
        rm_list = []
        for item in table_data:
            try:
                OxidizedNode.objects.get(name=item['name'])
                rm_list.append(table_data.index(item))
            except OxidizedNode.DoesNotExist:
                item['pk'] = item['name']
            # if q.count() > 0:
            #     table_data.remove(item)
        for i in rm_list:
            table_data = [x for x in table_data if table_data.index(x) not in rm_list]
        table = OxidizedNodeTable(table_data)
        context = {
            'table': table,
            'table_config_form': TableConfigForm(table),
            'permissions': {'change': True}
        }

        # Apply the request context
        paginate = {
            'paginator_class': EnhancedPaginator,
            'per_page': get_paginate_count(request)
        }
        RequestConfig(request, paginate).configure(table)
        return render(request, 'netbox_oxidized/import_list.html',context)
