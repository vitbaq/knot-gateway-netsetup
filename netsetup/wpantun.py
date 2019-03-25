#!/usr/bin/env python3
#
# Copyright (c) 2019, CESAR. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0

import os
import sys
import logging
import dbus
import dbus.mainloop.glib
from gi.repository import GObject

logging.basicConfig(format='[%(levelname)s] %(funcName)s: %(message)s\n',
                    stream=sys.stderr, level=logging.INFO)

INTERFACE_SERVICE_DBUS = "com.nestlabs.WPANTunnelDriver"
INTERFACE_DBUS = "org.wpantund.v1"
INTERFACE_DBUS_PATH = "/org/wpantund/wpan0"


class Singleton(type):
    """
    Singleton class to guarantee that a single instance will be used for
    its inhereted classes
    """
    __instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super(Singleton,
                                         cls).__call__(*args, **kwargs)
        return cls.__instances[cls]


class Wpantun(metaclass=Singleton):
    bus = None
    iface = None
    iface_state = None

    state = ""
    node_type = ""
    network_name = ""
    pan_id = 0
    channel = 0
    xpan_id = ""
    mesh_ipv6 = ""
    masterkey = ""

    def __init__(self):
        self.bus = dbus.SystemBus()
        self.iface = self.bus.get_object(
            INTERFACE_SERVICE_DBUS,
            INTERFACE_DBUS_PATH)

        self.iface_state = self.bus.get_object(
            INTERFACE_SERVICE_DBUS,
            "/com/nestlabs/WPANTunnelDriver/wpan0/Properties/NCP/State")

        self.refresh_values()
        self._register_signals_listener()

    def _register_signals_listener(self):
        self.iface_state.connect_to_signal(
            "PropertyChanged", self._state_signal_cb)

    def _state_signal_cb(self):
        self.refresh_values()

    def refresh_values(self):
        status = self.iface.Status(dbus_interface=INTERFACE_DBUS)

        self.state = status.get("NCP:State")

        if self.state == "associated":
            self.node_type = status.get("Network:NodeType")
            self.network_name = status.get("Network:Name")
            self.pan_id = status.get("Network:PANID")
            self.channel = status.get("NCP:Channel")
            self.xpan_id = status.get("Network:XPANID")
            self.mesh_ipv6 = status.get("IPv6:MeshLocalAddress")

            mkey = self.iface.PropGet(
                "Network:Key", dbus_interface=INTERFACE_DBUS)[1]

            self.masterkey = ":".join(['%02x' % item for item in mkey])
