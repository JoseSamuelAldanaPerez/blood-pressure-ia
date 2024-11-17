from flask import Flask
from .database.db import init_db, close_connection
from .routes import BloodPressureRoutes, IndexRoutes

app = Flask(__name__)


def init_app(config):
    app.config.from_object(config)
    init_db()

    @app.teardown_appcontext
    def teardown_db(exception):
        close_connection(exception)

    app.register_blueprint(IndexRoutes.main, url_prefix='/api')
    app.register_blueprint(
        BloodPressureRoutes.main, url_prefix='/api/blood_pressure')

    return app
