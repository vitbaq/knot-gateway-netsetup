#!/usr/bin/env python3
#
# Copyright (c) 2019, CESAR. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0

import os
import sys
import signal
import lockfile
import functools
import logging
import dbus
import dbus.service
import dbus.mainloop.glib
from gi.repository import GObject

import daemon
from wpantun import Wpantun
from ble import *

mainloop = None

logging.basicConfig(format='[%(levelname)s] %(funcName)s: %(message)s\n',
                    stream=sys.stderr, level=logging.INFO)


def quit_cb(signal_number, stack_frame):
    logging.info("Terminate with signal %d" % signal_number)
    mainloop.quit()


def register_ad_cb():
    print('Advertisement registered')


def register_ad_error_cb(error):
    print('Failed to register advertisement: ' + str(error))
    mainloop.quit()


context = daemon.DaemonContext(
    working_directory='/home/vitorbarros/newLora/knot-gatt-service',
    umask=0o002,
    detach_process=False,
    pidfile=lockfile.FileLock(
        '/home/vitorbarros/newLora/knot-gatt-service/pid.pid'),
    signal_map={signal.SIGTERM: quit_cb, signal.SIGINT: quit_cb},
    stdout=sys.stdout,
    stderr=sys.stderr,
)


with context:
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    wpan = Wpantun()
    bluetooth = Ble(wpan)

    mainloop = GObject.MainLoop()

    bluetooth.ad_manager.RegisterAdvertisement(
        bluetooth.ad_knot.get_path(), {},
        reply_handler=register_ad_cb,
        error_handler=register_ad_error_cb)

    mainloop.run()

    bluetooth.ad_manager.UnregisterAdvertisement(bluetooth.ad_knot)
    dbus.service.Object.remove_from_connection(bluetooth.ad_knot)
