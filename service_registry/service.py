class Service(object):
    def __init__(self, stype, version, data=None):
        self.type = stype
        self.version = version
        self.update(data or {})

    @property
    def id(self):
        return str(id(self))

    def update(self, data):
        self.data = {}
        self.data.update(data)

    def __json__(self):
        return {'id': self.id, 'type': self.type, 'version': self.version, 'data': self.data}
