from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask_migrate import Migrate
from models import db
from pedidos.routes import pedidos
from ventas.routes import ventas

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

app.register_blueprint(pedidos)
app.register_blueprint(ventas)

db.init_app(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route("/", methods=['GET'])
@app.route("/index")
def index():
    return render_template("index.html")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)