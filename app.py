from flask import Flask
from extensions import mysql
import controllers

app = Flask(__name__, template_folder='views')
app.config.from_object('config')
mysql.init_app(app)

app.register_blueprint(controllers.main)
app.register_blueprint(controllers.user)
app.register_blueprint(controllers.post_create)
app.register_blueprint(controllers.post_view)
app.register_blueprint(controllers.comment)
app.register_blueprint(controllers.userlist)
app.register_blueprint(controllers.admin_user_profile)
app.register_blueprint(controllers.reportlist)
app.register_blueprint(controllers.categorylist)
app.register_blueprint(controllers.pillar_request)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=3000, debug=True)
