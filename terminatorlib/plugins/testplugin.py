#!/usr/bin/env python3
import terminatorlib.plugin as plugin

# AVAILABLE must contain a list of all the classes that you want exposed
AVAILABLE = ['TestPlugin']


class TestPlugin(plugin.Plugin):
    capabilities = ['test']

    @staticmethod
    def do_test():
        return 'TestPluginWin'
