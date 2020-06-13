from am91.gaia import BaseManifest, ConfigField

class Manifest(BaseManifest):
    def fields(self):
        return [
            ConfigField("author", "Author"),
            ConfigField("email", "Email"),
            ConfigField("license", "License"),
            ConfigField("description", "Description")
        ]