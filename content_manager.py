# -*- coding=utf-8 -*-
from __future__ import unicode_literals
from flask import *
from flask_login import login_user, login_required
from flask_login import LoginManager, current_user
from flask_login import logout_user, UserMixin
import pymysql.cursors
import time
import os
app = Flask(__name__)
app.secret_key = os.urandom(24)
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = ''
login_manager.init_app(app=app)
db_connection = pymysql.connect(host='0.tcp.ngrok.io',port=14765,user='root',password='123456',db='gxy_test')
cursor = db_connection.cursor()

SRC_PATH = './templates/src'
JS_PATH = './templates/js'

class User(UserMixin):
	def __init__(self, username):
		self.username = username

	def get_id(self):
		return self.username


@login_manager.user_loader
def load_user(user_id):
        return User(user_id)

@app.route('/', methods=['GET', 'POST'])
def main():
	return render_template('login.html')

@app.route('/manager', methods=['GET', 'POST'])
@login_required
def manager_main_page():
	return render_template('manager.html')

@app.route('/manager/add/', methods=['GET', 'POST'])
@login_required
def add_content():
	msg_rsp = request.values.get('msg')
	url_rsp = request.values.get('url')
	type_rsp = request.values.get('type')
	creator_rsp = current_user.username
	createtime_rsp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	try:
		sql = 'INSERT INTO mini_answer(msg, url, type, creator, createtime) VALUES(%s, %s, %s, %s, %s)'
		cursor.execute(sql,(msg_rsp, url_rsp, type_rsp, creator_rsp, createtime_rsp))
		db_connection.commit()
		return jsonify({'error_code':'0'})
	except:
		db_connection.rollback()
		return jsonify({'error_code':'数据库错误，请联系管理员'})

@app.route('/manager/update/', methods=['GET', 'POST'])
@login_required
def update_content():
	id_rsp = request.values.get('id')
	msg_rsp = request.values.get('msg')
	url_rsp = request.values.get('url')
	type_rsp = request.values.get('type')
	if(len(id_rsp) == 0 or len(msg_rsp + url_rsp + type_rsp) == 0):
		return jsonify({'error_code':'数据为空,修改失败'})
	try:
		sql = 'UPDATE mini_answer SET '
		args_list = []
		if(len(msg_rsp)):
			args_list.append('msg=\''+msg_rsp +'\'')
		if(len(url_rsp)):
			args_list.append('url=\''+url_rsp +'\'')
		if(len(type_rsp)):
			args_list.append('type=\''+type_rsp + '\'')
		temp_str = ','
		sql = sql + temp_str.join(args_list) + ' WHERE id=' + id_rsp;
		cursor.execute(sql)
		db_connection.commit()
		return jsonify({'error_code':'0'})
	except:
		db_connection.rollback()
		return jsonify({'error_code':'数据库错误，请联系管理员'})

@app.route('/manager/delete/', methods=['GET', 'POST'])
@login_required
def delete_content():
	id_rsp = request.values.get('id')
	if(len(id_rsp) == 0):
		return jsonify({'error_code':'数据为空,删除失败'})
	try:
		sql = 'DELETE FROM mini_answer WHERE id=%s'
		cursor.execute(sql, (id_rsp))
		db_connection.commit()
		return jsonify({'error_code':'0'})
	except:
		db_connection.rollback()
		return jsonify({'error_code':'数据库错误，请联系管理员'})

@app.route('/manager/select/', methods=['GET', 'POST'])
@login_required
def select_content():
	id_rsp = request.values.get('id')
	msg_rsp = request.values.get('msg')
	url_rsp = request.values.get('url')
	type_rsp = request.values.get('type')
	creator_rsp = request.values.get('creator')
	createtime_rsp = request.values.get('createtime')
	result_list = []
	# record = {'id': '1', 'msg': 'hello_world', 'url': 'baidu.com', 'type':'励志', 'creator': 'Gao', 'createtime': '2018/8/12 21:43'}
	# result_list.append(record)
	try:
		sql = 'SELECT * FROM mini_answer'
		if(len(id_rsp + msg_rsp + url_rsp + type_rsp + type_rsp + creator_rsp + createtime_rsp) != 0):
			sql = sql + " WHERE ";
			args_list = []
			if(len(msg_rsp)):
				args_list.append('msg=\''+msg_rsp +'\'')
			if(len(url_rsp)):
				args_list.append('url=\''+url_rsp +'\'')
			if(len(type_rsp)):
				args_list.append('type=\''+type_rsp + '\'')
			if(len(id_rsp)):
				args_list.append('id=\''+id_rsp +'\'')
			if(len(creator_rsp)):
				args_list.append('creator=\''+creator_rsp +'\'')
			temp_str = ' AND '
			sql = sql + temp_str.join(args_list)
		print(sql)
		cursor.execute(sql)
		results = cursor.fetchall()
		db_connection.commit()
		for row in results:
			record = {'id': row[0], 'msg': row[1], 'url': row[2], 'type': row[3], 'creator': row[4], 'createtime': row[5].strftime("%Y/%m/%d %H:%M:%S")}
			result_list.append(record)
		return jsonify({'error_code':'0','record_list': result_list})
	except:
		db_connection.rollback()
		# return jsonify({'error_code':'0','record_list': result_list})
		return jsonify({'error_code':'数据库错误，请联系管理员'})

	result_list.append(record)
	return jsonify({'error_code':'0','record_list': result_list})

@app.route('/send_login/', methods=['GET', 'POST'])
def login():
	username_rsp = request.values.get('username')
	password_rsp = request.values.get('password')
	try:
		sql = 'SELECT count(*) FROM mini_admin where username=%s and password=%s'
		cursor.execute(sql,(username_rsp, password_rsp))
		result = cursor.fetchone()
		db_connection.commit()
		if(result[0] == 1):
			user = User(username_rsp)
			login_user(user)
			return jsonify({'login_info':'0'});
		else:
			return jsonify({'login_info':'登录失败'})
	except:
		return jsonify({'login_info':'数据库错误，请联系管理员'})

@app.route('/sub_content.html', methods=['GET', 'POST'])
def sub_content():
	return render_template('sub_content.html')

@app.route('/sub_user.html', methods=['GET', 'POST'])
def sub_user():
	return render_template('sub_user.html')

if __name__ == '__main__':
	app.debug = True
	app.run()