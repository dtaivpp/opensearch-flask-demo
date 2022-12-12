import logging
from . import util

logger = logging.getLogger('data-loader')

util.init_logging(logger, 'DEBUG')
util.initialize_opensearch_client(
    ["https://admin:admin@localhost:9200"],
    use_ssl=True,
    verify_certs=False,
    ssl_show_warn=False
)
