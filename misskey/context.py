class Header(object):
    def __init__(self, data):
        self.id = data.get('id')
        self.type = data.get('type')
