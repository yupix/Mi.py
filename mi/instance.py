class Instance(object):
    __slots__ = (
        'home',
        'name',
        'host',
        'software_name',
        'software_version',
        'icon_url',
        'favicon_url',
        'theme_color'
    )

    def __init__(self,
                 home: str = None,
                 name: str = None,
                 host: str = None,
                 software_name: str = None,
                 software_version: str = None,
                 icon_url: str = None,
                 favicon_url=None,
                 theme_color=None
                 ):
        self.home = home
        self.name = name
        self.host = host
        self.software_name = software_name
        self.software_version = software_version
        self.icon_url = icon_url
        self.favicon_url = favicon_url
        self.theme_color = theme_color

    @classmethod
    def from_dict(cls, data: dict):
        self = cls.__new__(cls)
        self.home = data.get('instance', {}).get('home')
        self.name = data.get('instance', {}).get('name')
        self.software_name = data.get('instance', {}).get('softwareName')
        self.icon_url = data.get('instance', {}).get('iconUrl')
        self.favicon_url = data.get('instance', {}).get('faviconUrl')
        self.theme_color = data.get('instance', {}).get('themeColor')
