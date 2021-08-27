from misskey.instance import Instance


class User(object):
    __slots__ = (
        'id',
        'name',
        'username',
        'host',
        'avatar_url',
        'avatar_blurhash',
        'avatar_color',
        'instance',
        'emojis'
    )

    def __init__(self, data: dict):
        self.id = data.get('id')
        self.name = data.get('name', data.get('username', None))
        self.username = data.get('username')
        self.host = data.get('host')
        self.avatar_url = data.get('avatarUrl')
        self.avatar_blurhash = data.get('avatarBlurhash')
        self.avatar_color = data.get('avatarColor')
        self.instance = Instance(data)
        self.emojis = data.get('emojis')
