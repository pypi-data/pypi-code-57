from crownstone_cloud import CrownstoneCloud


class CloudDataUpdater:
    """
    Optional API.
    Contains callbacks that can be used with the Crownstone SSE lib, or own events.
    """

    def __init__(self, cloud_instance: CrownstoneCloud) -> None:
        """
        :param cloud_instance: your instance of the cloud lib.

        Make sure your instance is initialized with data first!
        """
        self.cloud_instance = cloud_instance

    def update_switch_state(self, switch_state_event) -> None:
        """
        Updates the switch state of a crownstone.

        :param switch_state_event: Instance of SwitchStateUpdateEvent of the Crownstone SSE lib.

        SwitchStateUpdateEvent is a class containing: sphere_id, cloud_id, unique_id, switch_state.
        """
        sphere = self.cloud_instance.spheres.find_by_id(switch_state_event.sphere_id)
        crownstone = sphere.crownstones.find_by_id(switch_state_event.cloud_id)
        crownstone.state = switch_state_event.switch_state

    def update_presence(self, presence_event) -> None:
        """
        Updates the presence in a location.

        :param presence_event: Instance of PresenceEvent of the Crownstone SSE lib.

        PresenceEvent is a class containing: event_type, sphere_id, location_id, user_id.
        """
        sphere = self.cloud_instance.spheres.find_by_id(presence_event.sphere_id)
        user = sphere.users.find_by_id(presence_event.user_id)

        if presence_event.type == 'enterLocation':
            location = sphere.locations.find_by_id(presence_event.location_id)
            location.present_people.append(user.cloud_id)

        if presence_event.type == 'exitLocation':
            location = sphere.locations.find_by_id(presence_event.location_id)
            location.present_people.remove(user.cloud_id)

        if presence_event.type == 'enterSphere':
            sphere.present_people.append(user.cloud_id)

        if presence_event.type == 'exitSphere':
            sphere.present_people.remove(user.cloud_id)

    def update_data(self, data_change_event) -> None:
        """
        Replace the current data with new data from the cloud after a change.

        :param data_change_event: Instance of DataChangeEvent of the Crownstone SSE lib.

        DataChangeEvent is a class containing: operation, sphere_id, changed_item_id, changed_item_name
        """
        if data_change_event.type == 'spheres':
            self.cloud_instance.spheres.update_sync()

        sphere = self.cloud_instance.spheres.find_by_id(data_change_event.sphere_id)

        if data_change_event.type == 'stones':
            sphere.crownstones.update_sync()

        if data_change_event.type == 'users':
            sphere.users.update_sync()

        if data_change_event.type == 'locations':
            sphere.locations.update_sync()