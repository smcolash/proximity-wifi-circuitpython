import board

from output import WebHook, LED
from beacon import Beacon

# This is an example and is _NOT_ used by the code.
# - Create a copy of this file as 'secrets.py' with appropriate settings in
#   the 'network' dictionary to connect to any required or useful WiFi
#   networks.
# - Define any relevant MACIDs to look for as Beacons.
# - Define any useful outputs as LED(s) or WebHook(s) objects.
# - Make sure the Beacon definitions refer to correctly named LED or WebHook
#   items.

# Concepts:
# - Devices are independent from the beacons.
# - Devices are used/referenced by their names
# - A device may be associated with any number of beacons
# - A beacon may be defined to trigger any number of devices
# - Beacons are seen only on the WiFi channel of the access point being
#   defined and used
# - Specific instances of a device or a beacon are not needed elsewhere in the
#   code, they are created here and then maintained/managed as class-level
#   data

#
# any number of WiFi SSID --> password pairs may be specified here
#
networks = {
    'myhomewifinetwork': 'myhomewifinetworkpassword',
    'myworkwifinetwork': 'myworkwifinetworkpassword'
}

#
# any number of WebHook-based devices/actions may be specified here
#
WebHook ('office lights', 15 * 60, {
    True: 'https://maker.ifttt.com/trigger/OFFICE_LIGHTS_WEBHOOK_ON_NAME/with/key/YOUR_WEBHOOK_API_KEY',
    False: 'https://maker.ifttt.com/trigger/OFFICE_LIGHTS_WEBHOOK_OFF_NAME/with/key/YOUR_WEBHOOK_API_KEY'
}, True)

WebHook ('hallway lights', 5 * 60, {
    True: 'https://maker.ifttt.com/trigger/OFFICE_LIGHTS_WEBHOOK_ON_NAME/with/key/YOUR_WEBHOOK_API_KEY',
    False: 'https://maker.ifttt.com/trigger/OFFICE_LIGHTS_WEBHOOK_OFF_NAME/with/key/YOUR_WEBHOOK_API_KEY'
}, True)

#
# any number of pin-based LEDs (or other digital outputs) may be specified here
#
LED ('blue LED', 15 * 60, board.D2, True)

#
# any number of MACID-based beacons may be specified here, the beacons will be
# seen only on the WiFi channel of the network that is used, per the settings
# in 'networks' defined above (currently there is no channel hopping).
#
Beacon ('00:11:22:33:44:55', 'phone MACID #1', ['office lights', 'blue LED'], True)
Beacon ('11:22:33:44:55:66', 'phone MACID #2', ['office lights', 'blue LED'], True)
Beacon ('22:33:44:55:66:77', 'phone MACID #3', ['office lights', 'blue LED'], True)
Beacon ('33:44:55:66:77:88', 'laptop MACID #1', ['blue LED'], True)
Beacon ('44:55:66:77:88:99', 'laptop MACID #1', ['blue LED'], True)
