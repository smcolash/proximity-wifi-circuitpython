class Beacon (object):
    items = {}

    def __init__ (self, macid, name, devices, enabled):
        super ().__init__ ()

        if macid in Beacon.items:
            raise Exception ('duplicate beacon')

        Beacon.items[macid] = self

        self.macid = macid
        self.name = name
        self.devices = devices
        self.enabled = enabled
