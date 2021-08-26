from flask import Flask , flash , request,redirect,url_for

UPLOAD_FOLDER = 'website\ExcelFiles'
def create_app():
    app= Flask(__name__)
    app.config['SECRET_KEY']='AnySecretKey'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    from .views import views
    from .search import search
    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(search,url_prefix='/')
    return app