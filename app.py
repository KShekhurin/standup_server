from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import DATABASE_URL

app = Flask(__name__)
engine = create_engine(DATABASE_URL)
Session = sessionmaker(engine)


def init_app():
    from src.db_api import bp as db_api_blueprint
    from src.client import bp as client_blueprint

    app.register_blueprint(db_api_blueprint, url_prefix="/api")
    app.register_blueprint(client_blueprint, url_prefix="/client")

    app.run(debug=True, port="9000")


if __name__ == "__main__":
    init_app()
