import adafruit_requests
import board
import digitalio
import socketpool
import ssl
import time
import wifi

pool = socketpool.SocketPool (wifi.radio)
requests = adafruit_requests.Session (pool, ssl.create_default_context ())

class Output (object):
    items = {}

    def __init__ (self, name, limit, enabled):
        super ().__init__ ()

        if name in Output.items:
            raise Exception ('duplicate device')

        Output.items[name] = self

        self.name = name
        self.limit = limit
        self.enabled = enabled
        self.last = time.time ()
        self.pending = False
        self.on = False

    @classmethod
    def status (cls):
        delimiter = False
        for name in cls.items:
            device = cls.items[name]

            if not device.enabled:
                continue

            if not delimiter:
                print ('-' * 33)
                delimiter = True

            print ('%-20s : %4d %1d %1d %1d' % (
                    device.name,
                    device.idletime (),
                    device.idle (),
                    device.on,
                    device.pending
                )
            )

    def idletime (self):
        return max (0, time.time () - self.last)

    def idle (self):
        if not self.enabled:
            return False

        return self.idletime () > self.limit

    def toggle (self, state):
        if not self.enabled:
            return False

        if state:
            self.last = time.time ()
            if not self.on:
                print ('toggle - turn on %s' % (self.name))
                self.on = True
                self.pending = True
        else:
            if self.idle () and self.on:
                print ('toggle - turn off %s' % (self.name))
                self.on = False
                self.pending = True

        return self.pending

    def apply (self):
        if not self.pending:
            return

        self.pending = False
        try:
            self.activate ()
        except:
            print ('warning - device activation failed')
            pass

    @classmethod
    def ssid (cls, secrets):
        result = None
        for network in wifi.radio.start_scanning_networks ():
            if network.ssid in secrets.networks:
                result = network.ssid
                break

        wifi.radio.stop_scanning_networks ()

        return result

    @classmethod
    def channel (cls, secrets):
        result = None
        for network in wifi.radio.start_scanning_networks ():
            if network.ssid in secrets.networks:
                result = network.channel
                break

        wifi.radio.stop_scanning_networks ()

        if not result:
            result = 3

        return result

    @classmethod
    def synchronize (cls, secrets):
        ssid = cls.ssid (secrets)

        if ssid == None:
            print ('error - no available access point')
            return

        print ("connecting to %s" % (ssid))
        wifi.radio.connect (ssid, secrets.networks[ssid])
        print ("connected to %s" % (ssid))
        print ("local IP address: %s" % (wifi.radio.ipv4_address))

        #
        # apply any state updates to the devices
        #
        for name in cls.items:
            device = cls.items[name]

            if device.enabled:
                device.apply ()

        #
        # disconnect from the access point
        #
        wifi.radio.stop_station ()

class WebHook (Output):
    def __init__ (self, name, limit, urls, enabled):
        super ().__init__ (name, limit, enabled)
        self.urls = urls

    def activate (self):
        print ('%s: %d --> %s' % (self.name, self.on, self.urls[self.on]))

        response = requests.get (self.urls[self.on])
        print (response.text)
        response.close ()

class LED (Output):
    leds = {}

    def __init__ (self, name, limit, pin, enabled):
        super ().__init__ (name, limit, enabled)
        self.pin = pin

        if pin not in self.leds:
            self.leds[self.pin] = digitalio.DigitalInOut (self.pin)
            self.leds[self.pin].direction = digitalio.Direction.OUTPUT

    def activate (self):
        print ('%s: %d --> %s' % (self.name, self.on, self.pin))

        self.leds[self.pin].value = self.on
