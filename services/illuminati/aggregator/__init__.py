from flask import Flask


def create_app(is_unit_test=False):
    app = Flask(__name__)

    if not is_unit_test:
        from dependency_config import container
        # Create a child chain instance when creating a Flask app.
        container.get_aggregator()

    from . import server
    app.register_blueprint(server.api)
    app.register_blueprint(server.aggregator, url_prefix='/aggregator')
    return app
