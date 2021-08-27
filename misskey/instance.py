class Instance(object):
    __slots__ = (
        'home',
        'name',
        'software_name',
        'icon_url',
        'favicon_url',
        'theme_color'
    )

    def __init__(self, data):
        self.home = data.get('instance', {}).get('home')
        self.name = data.get('instance', {}).get('name')
        self.software_name = data.get('instance', {}).get('softwareName')
        self.icon_url = data.get('instance', {}).get('iconUrl')
        self.favicon_url = data.get('instance', {}).get('faviconUrl')
        self.theme_color = data.get('instance', {}).get('themeColor')
