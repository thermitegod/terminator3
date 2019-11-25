#!/usr/bin/env python3
# Terminator by Chris Jones <cmsj@tenshu.net>
# GPL v2 only
"""Simple management of Gtk Widget signal handlers"""

from terminatorlib.util import dbg, err


class Signalman(object):
    """Class providing glib signal tracking and management"""

    cnxids = None

    def __init__(self):
        """Class initialiser"""
        self.cnxids = {}

    def __del__(self):
        """Class destructor. This is only used to check for stray signals"""
        if len(self.cnxids.keys()) > 0:
            dbg(f'Remaining signals: {self.cnxids}')

    def new(self, widget, signal, handler, *args):
        """Register a new signal on a widget"""
        if widget not in self.cnxids:
            dbg(f'creating new bucket for {type(widget)}')
            self.cnxids[widget] = {}

        if signal in self.cnxids[widget]:
            err(f'{id(widget)} already has a handler for {signal}')

        self.cnxids[widget][signal] = widget.connect(signal, handler, *args)
        dbg(f'connected {type(widget)}::{signal} to {handler}')
        return self.cnxids[widget][signal]

    def remove_signal(self, widget, signal):
        """Remove a signal handler"""
        if widget not in self.cnxids:
            dbg(f'{widget} is not registered')
            return
        if signal not in self.cnxids[widget]:
            dbg(f'{signal} not registered for {type(widget)}')
            return
        dbg(f'removing {type(widget)}::{signal}')
        widget.disconnect(self.cnxids[widget][signal])
        del self.cnxids[widget][signal]
        if len(self.cnxids[widget].keys()) == 0:
            dbg('no more signals for widget')
            del self.cnxids[widget]

    def remove_widget(self, widget):
        """Remove all signal handlers for a widget"""
        if widget not in self.cnxids:
            dbg(f'{widget} not registered')
            return
        signals = tuple(self.cnxids[widget].keys())
        for signal in signals:
            self.remove_signal(widget, signal)

    def remove_all(self):
        """Remove all signal handlers for all widgets"""
        widgets = tuple(self.cnxids.keys())
        for widget in widgets:
            self.remove_widget(widget)
