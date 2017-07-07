from flask import Flask
from flask_login import LoginManager

from modelsAdmin import Admin

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'views_blueprint.login'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']='42'
    login_manager.init_app(app)
    from views import views_blueprint
    app.register_blueprint(views_blueprint)

    @login_manager.user_loader
    def load_user(admin_id):
        admin = Admin()
        admin.get_admin_object(admin_id)
        return admin

    return app

app = create_app()

if __name__ == '__main__':
    # app = create_app() # gunicorn方式启动需要把这句话放在外面
    app.run()
