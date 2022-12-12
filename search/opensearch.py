from opensearchpy import OpenSearch
import click
from flask import current_app, g

def get_os_client():
    if 'opensearch' not in g:
        g.opensearch = OpenSearch(
            current_app.config['OPENSEARCH'],
            use_ssl=True,
            verify_certs=False,
            ssl_show_warn=False
        )

        g.opensearch.close
    return g.opensearch


def close_os_connection(e=None):
    os_conn = g.pop('opensearch', None)

    if os_conn is not None:
        os_conn.close()


def init_os():
    """Check if OpenSearch has schemas populated"""
    os_conn = get_os_client()
    # Popluate schemas


@click.command('init-os')
def init_os_command():
    """Create new tables."""
    init_os()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_os_connection)
    app.cli.add_command(init_os_command)