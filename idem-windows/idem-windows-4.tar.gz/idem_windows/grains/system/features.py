import enum


class InstallState(enum.IntEnum):
    Enabled = 1
    Disabled = 2
    Absent = 3
    Unknown = 4


async def load_features(hub):
    optional_features = await hub.exec.wmi.get("Win32_OptionalFeature")
    features = {}
    for feature in sorted(optional_features):
        name = feature.Name.replace("-", "_").lower()
        features[name] = InstallState(feature.InstallState).name

    hub.grains.GRAINS.wsl = (
        features.get("microsoft_windows_subsystem_linux") == "Enabled"
    )
