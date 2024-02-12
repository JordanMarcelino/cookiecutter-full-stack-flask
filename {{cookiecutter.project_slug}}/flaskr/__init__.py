from flask import Flask


def create_app(config) -> Flask:
    app = Flask(__name__)
    app.mapping.from_object(config)

    with app.context():
        pass

    return app
