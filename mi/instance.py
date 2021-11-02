from .types.instance import Instance as InstancePayload


class Instance:
    def __init__(self, data: InstancePayload):
        self.host: str = data['host']
        self.name: str = data['name']
        self.software_name: str = data['software_name']
        self.software_version: str = data['software_version']
        self.icon_url: str = data['icon_url']
        self.favicon_url: str = data['favicon_url']
        self.theme_color: str = data['theme_color']
