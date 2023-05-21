#!/usr/bin/env python

import binascii
import gc
import sys
import time
import wifi

from output import Output, WebHook, LED
from beacon import Beacon

import secrets

def raw_to_hex (macid):
    output = binascii.hexlify (macid, ':')
    return output.decode ('utf-8')

TICK_IDLE = (1 - 1)

if __name__ == '__main__':
    print ()
    channel = Output.channel (secrets)
    print ('listening on channel: %d' % (channel))

    while True:
        pending = False
        monitor = wifi.Monitor (channel=channel)
        tick = time.monotonic_ns ()

        while not pending:
            packet = monitor.packet ()
            if len (packet):
                raw = packet[wifi.Packet.RAW]
                address = {}
                address['addr1'] = raw_to_hex (raw[4:(4+6)])
                address['addr2'] = raw_to_hex (raw[10:(10+6)])
                address['addr3'] = raw_to_hex (raw[16:(16+6)])

                for macid in Beacon.items:
                    beacon = Beacon.items[macid]

                    if not beacon.enabled:
                        continue

                    for region in address:
                        if macid in address[region]:
                            print ('trigger - %s (%s) found in %s' % (
                                    beacon.macid, beacon.name, region
                                )
                            )

                            for name in beacon.devices:
                                device = Output.items[name]
                                pending = device.toggle (True)
            else:
                time.sleep (0.001)

            for name in Output.items:
                device = Output.items[name]

                if device.idle ():
                    pending = device.toggle (False)

            if max (0, (time.monotonic_ns () - tick)) > 1E9:
                print (time.monotonic_ns ()/1.0E9)
                Output.status ()
                tick = time.monotonic_ns ()

            gc.collect ()

        monitor.deinit ()

        #
        # synchronize the output state with the devices
        #
        Output.synchronize (secrets)

    #
    # probably should not have gotten here...
    #
    sys.exit (0)
