#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os import path
from pydm import Display

class DeviceMenu(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(DeviceMenu, self).__init__(parent=parent, args=args, macros=macros)

    def ui_filename(self):
        return '../ui/latest/confirmation_message.ui'

    def ui_filepath(self):
        return path.join(path.dirname(path.realpath(__file__)), self.ui_filename())
