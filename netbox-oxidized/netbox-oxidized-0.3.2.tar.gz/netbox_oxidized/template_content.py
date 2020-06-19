from extras.plugins import PluginTemplateExtension
from django.urls import reverse
from urllib import parse

from .models import OxidizedNode
from .utils import get_oxidized_nodeinfo, get_oxidized_nodeversion_list

class DeviceNodeStats(PluginTemplateExtension):
    model = 'dcim.device'

    def buttons(self):
        node = None
        try:
            node = OxidizedNode.objects.get(device_id=self.context["object"].id)
            #if already to oxidixed dont show add button
            return ""
        except:
            ip = self.context["object"].primary_ip
            if ip:
                ip = str(ip.address).split('/')[0]
            else:
                ip = '0.0.0.0'
            qs = 'device={0}&name={1}&ipaddress={2}&group=default&return_url=%2Fdcim%2Fdevices%2F{0}'.format(self.context["object"].id, self.context["object"].name, ip)
            url = reverse('plugins:netbox_oxidized:oxidizednode_add')
            return '<a href="{}?{}" class="btn btn-default"><span class="fa fa-plus" aria-hidden="true"></span> Add to Oxidized</a>'.format(url,qs)

    def right_page(self):
        name = None
        try:
            node = OxidizedNode.objects.get(device_id=self.context["object"].id)
            name = node.name
        except:
            pass

        if name:
            oxidized_url = self.context['config'].get('oxidized_url')

            data = get_oxidized_nodeinfo(oxidized_url, name, ssl_verify=False)
            stat_data = {}

            if data and not data.get('error'):
                stat_data['time'] = data['last']['end']
                stat_data['runtime'] = round(float(data['last']['time']),2) 
                stat_data['status'] = data['last']['status']
                stat_data['mtime'] = data['mtime']
            else:
                stat_data['status'] = data['error']
            return self.render('netbox_oxidized/inc/node_stats.html', extra_context={
                'stat_data': stat_data,
            })
        else:
            return ""

template_extensions = [DeviceNodeStats]