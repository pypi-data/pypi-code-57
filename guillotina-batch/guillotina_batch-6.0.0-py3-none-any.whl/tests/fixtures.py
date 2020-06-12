from guillotina import testing


def settings_configurator(settings):
    if "applications" not in settings:
        settings["applications"] = []
    settings["applications"].extend(
        ["guillotina_batch", "guillotina_batch.tests.package"]
    )


testing.configure_with(settings_configurator)
