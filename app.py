from flask import Flask
from extensions import mysql
import controllers

app = Flask(__name__, template_folder='views')
app.config.from_object('config')
mysql.init_app(app)

app.register_blueprint(controllers.main)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=3000, debug=True)
