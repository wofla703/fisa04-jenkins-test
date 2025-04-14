# flask run --debug --port 5001
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
import datetime
import os
#test1
import config
# flask db init
# flask db migrate
# flask db upgrade 


naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()

def create_app():
    app= Flask(__name__)
    app.config.from_object(config)

    # ORM
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)


   # 커스텀 진자 필터 등록
    from filters import format_datetime, format_datetime2
    app.jinja_env.filters['date_time'] = format_datetime
    app.jinja_env.filters['date_time2'] = format_datetime2

    import logging.config

        # logs 디렉터리 생성
    logs_dir = os.path.join(app.root_path, 'logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    today_date = datetime.datetime.now().strftime("%Y-%m-%d").replace(":", "-")

    # >pip install python-json-logger 
    #     from pythonjsonlogger import jsonlogger  

                #     'json-format': {  # JSON 형식의 로그 포맷터
                #     '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
                #     'format': '%(levelname)s %(asctime)s %(name)s %(message)s',
                # },
    # 로깅 설정
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
                'style': '{',
            },
            'simple': {
                'format': '{levelname} {message}',
                'style': '{',
            },
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
            },
            'file': {
                'level': 'INFO',
                'encoding': 'utf-8',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(logs_dir, f'{today_date}-mysiteLog.log'),
                'formatter': 'verbose',
                'maxBytes': 1024*1024*5,
                'backupCount': 5,
            },
            'errors': {
                'level': 'ERROR',
                'encoding': 'utf-8',
                'class': 'logging.FileHandler',
                'filename': os.path.join(logs_dir, f'{today_date}-mysiteErrorLog.log'),
                'formatter': 'simple',
            },
        },
        'loggers': {
            'flask.app': {
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'flask.request': {
                'handlers': ['errors'],
                'level': 'ERROR',
                'propagate': True,
            },
            'my': {
                'handlers': ['console', 'file', 'errors'],
                'level': 'INFO',
            },
        },
    })

            
    from board.views import main_views, board_views, answer_views, auth_views
    from ml_model import ml_views
    app.register_blueprint(main_views.mbp)
    app.register_blueprint(board_views.cbp)
    app.register_blueprint(answer_views.abp)
    app.register_blueprint(auth_views.auth)
    app.register_blueprint(ml_views.mlbp)

    return app
