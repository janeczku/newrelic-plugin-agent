"""
Plugins are responsible for fetching and parsing the stats from the service
being profiled.

"""
available = {
    'apache_httpd': 'newrelic_plugin_agent.plugins.apache_httpd.ApacheHTTPD',
    'couchdb': 'newrelic_plugin_agent.plugins.couchdb.CouchDB',
    'edgecast': 'newrelic_plugin_agent.plugins.edgecast.Edgecast',
    'elasticsearch':
        'newrelic_plugin_agent.plugins.elasticsearch.ElasticSearch',
    'haproxy': 'newrelic_plugin_agent.plugins.haproxy.HAProxy',
    'memcached': 'newrelic_plugin_agent.plugins.memcached.Memcached',
    'mongodb': 'newrelic_plugin_agent.plugins.mongodb.MongoDB',
    'nginx': 'newrelic_plugin_agent.plugins.nginx.Nginx',
    'pdns_recursor': 'newrelic_plugin_agent.plugins.pdns_recursor.PdnsRecursor',
    'pgbouncer': 'newrelic_plugin_agent.plugins.pgbouncer.PgBouncer',
    'php_apc': 'newrelic_plugin_agent.plugins.php_apc.APC',
    'php_fpm': 'newrelic_plugin_agent.plugins.php_fpm.FPM',
    'php_opc': 'newrelic_plugin_agent.plugins.php_opc.OPC',
    'postgresql': 'newrelic_plugin_agent.plugins.postgresql.PostgreSQL',
    'rabbitmq': 'newrelic_plugin_agent.plugins.rabbitmq.RabbitMQ',
    'redis': 'newrelic_plugin_agent.plugins.redis.Redis',
    'riak': 'newrelic_plugin_agent.plugins.riak.Riak',
    'uwsgi': 'newrelic_plugin_agent.plugins.uwsgi.uWSGI'}
