from flask import Flask
from api.manga import manga_bp
from api.manhua import manhua_bp
from api.manhwa import manhwa_bp
from api.update_manga import update_manga_bp
from api.update_manhua import update_manhua_bp
from api.update_manhwa import update_manhwa_bp
from api.hot_manga import hot_manga_bp
from api.hot_manhua import hot_manhua_bp
from api.hot_manhwa import hot_manhwa_bp
from api.home import home_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.register_blueprint(manga_bp)
app.register_blueprint(manhua_bp)
app.register_blueprint(manhwa_bp)
app.register_blueprint(update_manga_bp)
app.register_blueprint(update_manhua_bp)
app.register_blueprint(update_manhwa_bp)
app.register_blueprint(hot_manga_bp)
app.register_blueprint(hot_manhua_bp)
app.register_blueprint(hot_manhwa_bp)
app.register_blueprint(home_bp)

if __name__ == "__main__":
    app.run()
