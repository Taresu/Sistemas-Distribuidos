from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_sse import sse
from routes import setup_routes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/stream')

db = SQLAlchemy(app)

setup_routes(app, db)

if __name__ == '__main__':
    app.run(debug=True)