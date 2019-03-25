#!/usr/bin/env python3
#
# Copyright (c) 2019, CESAR. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0

import os
import sys
import logging
import dbus

logging.basicConfig(format='[%(levelname)s] %(funcName)s: %(message)s\n',
                    stream=sys.stderr, level=logging.INFO)


BLUEZ_SERVICE_NAME = 'org.bluez'
DBUS_OM_IFACE = 'org.freedesktop.DBus.ObjectManager'
DBUS_PROP_IFACE = 'org.freedesktop.DBus.Properties'


LE_ADVERTISING_MANAGER_IFACE = 'org.bluez.LEAdvertisingManager1'


wpantun = None


class Ble(object):
    bus = None

    def __init__(self, wpan):
        global wpantun

        self.bus = dbus.SystemBus()
        wpantun = wpan

        self.ad_adapter = find_adapter(self.bus, LE_ADVERTISING_MANAGER_IFACE)
        if not self.ad_adapter:
            logging.error("LEAdvertiseManager1 interface not found")

        self.ad_adapter_props = dbus.Interface(
            self.bus.get_object(BLUEZ_SERVICE_NAME, self.ad_adapter),
            "org.freedesktop.DBus.Properties")

        self.ad_adapter_props.Set("org.bluez.Adapter1",
                                  "Powered", dbus.Boolean(1))


def find_adapter(bus, iface):
    remote_om = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, '/'),
                               DBUS_OM_IFACE)
    objects = remote_om.GetManagedObjects()

    for o, props in objects.items():
        if iface in props.keys():
            return o

    return None
