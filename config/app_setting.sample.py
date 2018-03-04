# coding=utf-8
import os
from datetime import timedelta


class Config:
    # 项目目录
    ROOT_PATH = os.path.abspath('.')
    # 日志目录
    LOG_PATH = ROOT_PATH + '/logs'
    # 日志文件
    APP_LOG_FILE = ROOT_PATH + '/logs/admin.log'
    # 统一标签对应的s3文件目录
    UNITAG_PATH = 's3://datamining.ym/tag/'

    SECRET_KEY = os.environ.get(
        "SECRET_KEY") or "xd9\x85\x9c\xbc\x19\x9b\xe6ch\xdd\x12\x04F\x87%R5\xb3\xa7\xc2P\x93P\xe2"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # 废弃
    SSO_SWITCH = False
    # 是否开启流量预估
    TRAFFIC_PREDICT = False

    CENSOR = False
    # SSO测试账号
    SSO_TEST_ACCOUNT = 'admin@youmi.net'
    # session lifetime
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)

    SESSION_COOKIE_NAME = "auth"
    SESSION_COOKIE_HTTPONLY = False
    SQLALCHEMY_DATABASE_URI = "mysql+cymysql://youmi:iloveUMLife123@172.16.1.50/youmi"
    SQLALCHEMY_BINDS = {
        # "youmi": SQLALCHEMY_DATABASE_URI,
        "admin": "mysql+cymysql://youmi:iloveUMLife123@172.16.1.50/youmi_admin",
        "spot": "mysql+cymysql://youmi:iloveUMLife123@172.16.1.50/youmi_spot",
        "stat": "mysql+cymysql://youmi:iloveUMLife123@172.16.1.50/youmi_stat",
        "data": "mysql+cymysql://youmi:iloveUMLife123@172.16.1.50/youmi_data",
        "rtb_report": "mysql+cymysql://youmi:iloveUMLife123@172.16.1.50/youmi_rtb_report",
        "rtb": "mysql+cymysql://youmi:iloveUMLife123@172.16.1.50/youmi_rtb",
        "app_ad_record": "mysql+cymysql://youmi:iloveUMLife123@172.16.1.50/youmi_app_ad_record",
        "audience": "mysql+cymysql://youmi:iloveUMLife123@172.16.1.50/youmi_app_ad_record"
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    REDSHIFT = "dbname=youmi_stats user=ymserver password=host=youmi-statsdata.cpwyku9ohxzt.cn-north-1.redshift.amazonaws.com.cn port=5439"
    AUDIENCE_REDSHIFT = "dbname=youmi_analyser user=ymserver password=host=youmi-statsdata.cpwyku9ohxzt.cn-north-1.redshift.amazonaws.com.cn port=5439"
    SENTRY_DSN = "http://29e17e66e54747d796a76d10d73d13d3:136a2735eba84f65af8461776eb3d197@sentry.awscn.umlife.net/20"
    RTB_LOG_01 = 'http://censor.y.cn'
    UPLOAD_FOLDED = '/home/zhangtiantao/YouMiCode/operate/tmp'



class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    pass


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}
