
"""
PHP OPcache Support

"""
import logging

from newrelic_plugin_agent.plugins import base

LOGGER = logging.getLogger(__name__)


class OPC(base.JSONStatsPlugin):

    GUID = 'com.meetme.newrelic_php_opc_agent'

    def add_datapoints(self, stats):
        """Add all of the data points for a node

        :param dict stats: The stats content from OPC as a string

        """
        # OPC Shared Memory Stats
        opc_stats = stats.get('status', dict())
        shared_memory = opc_stats.get('memory_usage', dict())
        self.add_gauge_value('Shared Memory/Available', 'bytes',
                             shared_memory.get('free_memory', 0))
        self.add_gauge_value('Shared Memory/Used', 'bytes',
                             shared_memory.get('used_memory', 0))
        self.add_gauge_value('Shared Memory/Wasted', 'bytes',
                             shared_memory.get('wasted_memory', 0))

        # OPC System Stats
        system_stats = opc_stats.get('opcache_statistics', dict())
        self.add_gauge_value('System Cache/Scripts', 'files',
                             system_stats.get('num_cached_scripts', 0))
        self.add_gauge_value('System Cache/Keys', 'keys',
                             system_stats.get('num_cached_keys', 0),
                             max_val=system_stats.get('max_cached_keys', 0))
        self.add_gauge_value('System Cache/Hitrate', 'percent',
                             system_stats.get('opcache_hit_rate', 0))
        self.add_derive_value('System Cache/Hits', 'files',
                             system_stats.get('hits', 0))
        self.add_derive_value('System Cache/Misses', 'files',
                             system_stats.get('misses', 0))
