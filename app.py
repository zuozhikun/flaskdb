from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_,or_,not_
from flask_script import Manager
from flask_migrate import Migrate

# import pymysql
# pymysql.install_as_MySQLdb()

app = Flask(__name__)



# 配置信息
class Config(object):
    # 连接数据库
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1:3306/flask_db?charset=utf8'

    # 设置sqlalchemy自动更跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 查询时会显示原始SQL语句
    app.config['SQLALCHEMY_ECHO'] = True

    # 禁止自动提交数据处理
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# 读取配置
app.config.from_object(Config)

# 创建数据库sqlalchemy工具对象
db = SQLAlchemy(app)


# 让迁移时app和db建立联系
Migrate(app,db)



# 创建数据库类
# 角色模型类
class Role(db.Model):
    #定义表名
    __tablename__ = 'roles'

    # 定义字段
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    # 反推与role关联的多个User模型对象
    us = db.relationship('User',backref='role')

    def __str__(self):
        return self.name
# 用户模型类
class User(db.Model):
    # 定义表名
    __tablename__ = 'users'

    # 定义字段
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    email = db.Column(db.String(64),unique=True)
    pwd = db.Column(db.String(20))
    #定义外键
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))

    def __str__(self):
        return self.name

# 多对多联系表
registrations = db.Table('registrations',
                         db.Column('student_id', db.Integer, db.ForeignKey('students.id')),
                         db.Column('class_id', db.Integer, db.ForeignKey('classes.id'))
                         )

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    classes = db.relationship('Class', secondary=registrations,
                          backref=db.backref('students', lazy='dynamic'),
                          lazy='dynamic')

class Class(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))


# # 删除表
# db.drop_all()
# # 创建表
# db.create_all()

# # 添加数据
# r1 = Role(name='zuozhikun')
# db.session.add(r1)
# db.session.commit()

# r2 = Role(name='songxia')
# r3 = Role(name='xiaosongxiao')
# db.session.add_all([r2,r3])
# db.session.commit()

# ret = Role.query.all()
# print(ret)




# 查询用户的角色      User.role
# 查询角色对应那些用户  roles.us

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()


