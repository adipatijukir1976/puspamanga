from flask import Flask
from api.manga import manga_bp
from api.manhua import manhua_bp
from api.manhwa import manhwa_bp
from api.home import home_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.register_blueprint(manga_bp)
app.register_blueprint(manhua_bp)
app.register_blueprint(manhwa_bp)
app.register_blueprint(home_bp)

if __name__ == "__main__":
    app.run()
