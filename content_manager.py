# -*- coding=utf-8 -*-
from __future__ import unicode_literals
from flask import *
from flask_login import login_user, login_required
from flask_login import LoginManager, current_user
from flask_login import logout_user, UserMixin
import time
import os
app = Flask(__name__)
app.secret_key = os.urandom(24)
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = ''
login_manager.init_app(app=app)
ADMIN='pokmiu'
PASSWORD='6a0e78163a9e2e670cfa57aeb4a22518'

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
	id_rsp = request.values.get('id')
	msg_rsp = request.values.get('msg')
	url_rsp = request.values.get('url')
	type_rsp = request.values.get('type')
	creator_rsp = current_user.username
	createtime_rsp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	print(id_rsp)
	print(msg_rsp)
	print(url_rsp)
	print(type_rsp)
	print(creator_rsp)
	print(createtime_rsp)
	return jsonify({'error_code':'0'})

@app.route('/manager/update/', methods=['GET', 'POST'])
@login_required
def update_content():
	id_rsp = request.values.get('id')
	msg_rsp = request.values.get('msg')
	url_rsp = request.values.get('url')
	type_rsp = request.values.get('type')
	print(id_rsp)
	print(msg_rsp)
	print(url_rsp)
	print(type_rsp)
	return jsonify({'error_code':'0'})

@app.route('/manager/delete/', methods=['GET', 'POST'])
@login_required
def delete_content():
	id_rsp = request.values.get('id')
	msg_rsp = request.values.get('msg')
	url_rsp = request.values.get('url')
	type_rsp = request.values.get('type')
	creator_rsp = request.values.get('creator')
	createtime_rsp = request.values.get('createtime')
	print(id_rsp)
	print(msg_rsp)
	print(url_rsp)
	print(type_rsp)
	print(creator_rsp)
	print(createtime_rsp)
	return jsonify({'error_code':'0'})

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
	record = {'id': '1', 'msg': 'hello_world', 'url': 'baidu.com', 'type':'励志', 'creator': 'Gao', 'createtime': '2018/8/12 21:43'}
	result_list.append(record)
	return jsonify({'error_code':'0','record_list': result_list})

@app.route('/send_login/', methods=['GET', 'POST'])
def login():
	username_rsp = request.values.get('username')
	password_rsp = request.values.get('password')
	if(username_rsp==ADMIN and password_rsp==PASSWORD):
		user = User(username_rsp)
		login_user(user)
		return jsonify({'login_info':'0'});
	return jsonify({'login_info':'登录失败'})

@app.route('/sub_content.html', methods=['GET', 'POST'])
def sub_content():
	return render_template('sub_content.html')

@app.route('/sub_user.html', methods=['GET', 'POST'])
def sub_user():
	return render_template('sub_user.html')

if __name__ == '__main__':
	app.debug = True
	app.run()