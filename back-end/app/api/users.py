import re

from flask import request, jsonify, url_for, json

from api.auth import token_auth
from app.api.error import bad_request
from app import db
from app.api import bp
from app.models.user import User


@bp.route('/users', methods=['POST'])
def create_user():
    data = json.loads(request.get_data())
    if not data:
        return bad_request("请求错误")
    msg = {}
    if 'username' not in data or not data.get('username', None):
        msg['username'] = "请输入用户名"

    pattern = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
    if 'email' not in data or not re.match(pattern, data.get('email', None)):
        msg['email'] = 'Please provide a valid email address.'
    if 'password' not in data or not data.get('password', None):
        msg['password'] = 'Please provide a valid password.'

    if User.query.filter_by(username=data.get('username', None)).first():
        msg['username'] = 'Please use a different username.'
    if User.query.filter_by(email=data.get('email', None)).first():
        msg['email'] = 'Please use a different email address.'
    if msg:
        return bad_request(msg)
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    # user=user.to_dict()
    resp = jsonify({'status': True})
    resp.status_code = 201
    resp.headers['Location'] = url_for('api.get_user', id=user.id)
    return resp


@bp.route('/get_users', methods=['GET'])
@token_auth.login_required
def get_users():
    # page=request.args.get('page',1,type=int)
    # per_page=min(request.args.get("per_page",10,type=int),100)
    data = json.loads(request.get_data())
    page = 1 if (data.get('page', None) is None) else data.get('page', None)
    per_page = 10 if (data.get('page', None) is None) else data.get('per_page', None)
    user = User.to_collection_dict(User.query, page, per_page, 'api.get_users')
    # user['page']=page
    return jsonify(user)


@bp.route('/get_user', methods=['GET'])
@token_auth.login_required
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())


@bp.route('/update_user', methods=['PUT'])
@token_auth.login_required
def update_user():
    data = json.loads(request.get_data())
    user = User.query.filter_by(id=data['id']).first()
    if not data:
        return bad_request("请求错误")
    msg = {}

    pattern = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
    if 'email' not in data or not re.match(pattern, data.get('email', None)):
        msg['email'] = 'Please provide a valid email address.'
    if User.query.filter_by(username=data.get('name', None)).first():
        if User.query.filter_by(username=data.get('name', None)).first().id != user.id:
            msg['username'] = 'Please use a different username.'
    if User.query.filter_by(email=data.get('email', None)).first():
        if User.query.filter_by(email=data.get('email', None)).first().email != user.email:
            msg['email'] = 'Please use a different email address.'
    if msg:
        return bad_request(msg)
    user.from_dict(data, new_user=False)
    db.session.commit()
    resp = jsonify(user.to_dict())
    resp.status_code = 201
    return resp


@bp.route('/delete_user', methods=['PUT'])
@token_auth.login_required
def delete_user():
    data = json.loads(request.get_data())
    username = data['username']
    user = User.query.filter_by(username=username).first()
    user1 = user.to_dict()
    #
    try:
        db.session.delete(user)
        db.session.commit()

        return jsonify(user1)
    except Exception as e:
        return jsonify({"status": "false"})


@bp.route('/modify_password', methods=['PUT'])
@token_auth.login_required
def modify_password():
    data = json.loads(request.get_data())
    user = User.query.filter_by(id=data['id']).first()
    user.set_password(data['password'])
    db.session.commit()
    return jsonify({"status": True})


@bp.route('/check_password', methods=['GET'])
@token_auth.login_required
def check_password():
    data = json.loads(request.get_data())
    user = User.query.filter_by(id=data['id']).first()
    if user.check_password_hash(data['password']):
        return jsonify({"status": True})
    else:
        return jsonify({"status": False})