from . import config
from .types.instance import Instance as InstancePayload


class Instance:
    def __init__(self, data: InstancePayload):
        self.host: str = data.get('host', config.i.instance['uri'])
        self.name: str = data.get('name', config.i.instance['name'])
        self.software_name: str = data.get('software_name')
        self.software_version: str = data.get('software_version', config.i.instance['version'])
        self.icon_url: str = data.get('icon_url')
        self.favicon_url: str = data.get('favicon_url')
        self.theme_color: str = data.get('theme_color')
