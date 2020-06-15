"""Template view for devices.

(c) 2020 Justin Drew
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

# from extras.plugins import PluginTemplateExtension
# from .models import Tunnel
#
#
# class DeviceTunnels(PluginTemplateExtension):
#     """Class to display tunnels for a device."""
#
#     model = "dcim.devices"
#
#     def full_width_page(self):
#         """Render content of device_tunnel_list on device page."""
#         return self.render("netbox_tunnels/device_tunnel_list.html", extra_context={"tunnels": Tunnel.objects.all(),})
#
#
# template_extensions = [DeviceTunnels]
