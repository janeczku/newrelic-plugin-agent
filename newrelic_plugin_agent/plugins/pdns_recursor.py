"""
PowerDNS Recursor  - pdns_recursor.PdnsRecursor
"""
import logging
import requests

from newrelic_plugin_agent.plugins import base

LOGGER = logging.getLogger(__name__)

class PdnsRecursor(base.JSONStatsPlugin):

    DEFAULT_HOST = 'localhost'
    DEFAULT_PATH = '/servers/localhost/statistics'
    DEFAULT_PORT = 8082

    GUID = 'com.meetme.newrelic_pdnsrecursor_agent'

    def add_datapoints(self, data):
        """Add the data points for Component/Indices
        :param dict stats: The stats to process for the values
        """
        # transpose to simple dict
        try:
          stats = dict([(r['name'], int(r['value'])) for r in data])
        except Exception as error:
          LOGGER.error('Error transposing stats to simple dict: %r', error)

        self.add_derive_value('Queries/Totals/Outgoing-Queries', 'queries',
                             stats.get('all-outqueries', 0))
        self.add_derive_value('Queries/Totals/Outgoing-Queries-TCP', 'queries',
                              stats.get('tcp-outqueries', 0))
        self.add_derive_value('Queries/Totals/Incoming-Queries', 'queries',
                              stats.get('questions', 0))
        self.add_derive_value('Queries/Totals/Incoming-Queries-TCP', 'queries',
                              stats.get('tcp-questions', 0))

        self.add_derive_value('Answers/Totals/0-1ms', 'answers',
                              stats.get('answers0-1', 0))
        self.add_derive_value('Answers/Totals/100-1000ms', 'answers',
                              stats.get('answers100-1000', 0))
        self.add_derive_value('Answers/Totals/10-100ms', 'answers',
                              stats.get('answers10-100', 0))
        self.add_derive_value('Answers/Totals/1-10ms', 'answers',
                              stats.get('answers1-10', 0))
        self.add_derive_value('Answers/Totals/Slow', 'answers',
                              stats.get('answers-slow', 0))

        self.add_derive_value('Answers/Result/NORMAL', 'answers',
                              stats.get('noerror-answers', 0))
        self.add_derive_value('Answers/Result/NXDOMAIN', 'answers',
                              stats.get('nxdomain-answers', 0))
        self.add_derive_value('Answers/Result/SERVFAIL', 'answers',
                              stats.get('servfail-answers', 0))

        self.add_gauge_value('Queries/Concurrent-Queries', 'queries',
                             stats.get('concurrent-queries', 0))

        self.add_gauge_value('Queries/Average-Latency', 'ms',
                             stats.get('concurrent-queries', 0)/1000)

        self.add_derive_value('Queries/Drops/Policy-Drops', 'queries',
                              stats.get('policy-drops', 0))
        self.add_derive_value('Queries/Drops/Spoof-Prevents', 'queries',
                              stats.get('spoof-prevents', 0))
        self.add_derive_value('Queries/Drops/TCP-Client-Overflow', 'queries',
                              stats.get('tcp-client-overflow', 0))
        self.add_derive_value('Queries/Drops/Concurrent-Query-Limit', 'queries',
                              stats.get('over-capacity-drops', 0))

        self.add_derive_value('Queries/Throttled/Throttled-Map-Entries', 'items',
                              stats.get('throttle-entries', 0))
        self.add_derive_value('Queries/Throttled/Throttled-Outgoing-Queries', 'queries',
                              stats.get('throttled-outqueries', 0))
        self.add_derive_value('Queries/Throttled/Resource-Limit-Fails', 'queries',
                              stats.get('resource-limits', 0))

        self.add_derive_value('Queries/Errors/Client-Parse-Errors', 'errors',
                              stats.get('client-parse-errors', 0))
        self.add_derive_value('Queries/Errors/Server-Parse-Errors', 'errors',
                              stats.get('server-parse-errors', 0))
        self.add_derive_value('Queries/Errors/Resource-Limits-Fails', 'errors',
                              stats.get('resource-limits', 0))
        self.add_derive_value('Queries/Errors/Outgoing-Timeouts', 'errors',
                              stats.get('outgoing-timeouts', 0))

        self.add_gauge_value('CacheSize/Cache-Entries', 'items',
                             stats.get('cache-entries', 0))
        self.add_gauge_value('CacheSize/Packetcache-Entries', 'items',
                             stats.get('packetcache-entries', 0))

        self.add_derive_value('Load/User-CPU', '%',
                             float(stats.get('user-msec', 0))/10.0)
        self.add_derive_value('Load/System-CPU', '%',
                             float(stats.get('sys-msec', 0))/10.0)

        self.cache_hit_ratio('Cache', stats)
        self.cache_hit_ratio('Packetcache', stats)

    def cache_hit_ratio(self, name, stats):
        """Calculate cache hit ratio and add gauge values
        :param str name: The cache type ("Cache" or "Packetcache")
        :param dict stats: The stats dict
        """
        total = stats.get('%s-hits' % name.lower(), 0) + stats.get('%s-misses' % name.lower(), 0)
        if total > 0:
            ratio = (float(stats.get('%s-hits' % name.lower(), 0)) / float(total)) * 100
        else:
            ratio = 0
        self.add_gauge_value('CachesHitRatio/%s' % name, '%', ratio)

    """Override base class methods
    """
    def http_get(self):
        """Fetch the data from the stats URL
        :rtype: requests.models.Response
        """
        LOGGER.debug('Polling %s Stats at %s',
                     self.__class__.__name__, self.stats_url)
        req_kwargs = self.request_kwargs
        if 'password' in self.config:
          headers = {'X-API-Key': self.config['password']}
          req_kwargs['headers'] = headers
        try:
            response = requests.get(**req_kwargs)
        except requests.ConnectionError as error:
            LOGGER.error('Error polling stats: %s', error)
            return ''

        if response.status_code >= 300:
            LOGGER.error('Error response from %s (%s): %s', self.stats_url,
                         response.status_code, response.content)
            return None
        return response
