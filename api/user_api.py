import flask
from flask import request, make_response, jsonify

from SQL.data import db_session
from SQL.data.users import User
from maps.utiles import get_object, get_ll_spn, get_static_api_image

user_bp = flask.Blueprint('users_api', __name__)


@user_bp.route('/users')
def get_all_users():
    session = db_session.create_session()
    users = session.query(User).all()
    return jsonify(
        {'users': (
            [item.to_dict(only=(
                'id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email'
            )) for
                item in users])

        }
    )


@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if user:
        return jsonify(
            {'users': [
                user.to_dict(only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email'))]

            }
        )
    return make_response(jsonify({'error': 'Not found'}), 404)


@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@user_bp.route('/users', methods=['POST'])
def create_one_user():
    user = request.json
    if not user:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in user for key in ['surname', 'name', 'age', 'position', 'speciality', 'address', 'email',
                                         'password']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    new_user = User(surname=user['surname'],
                    name=user['name'],
                    age=user['age'],
                    position=user['surname'],
                    speciality=user['speciality'],
                    address=user['address'],
                    email=user['email'])
    new_user.set_password(user['password'])
    db_sess.add(new_user)
    db_sess.commit()
    return jsonify({'id': new_user.id})


@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def edit_one_user(user_id):
    user_info = request.json
    if not user_info:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(
            key in user_info for key in
            ['surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'password']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()

    user = db_sess.query(User).get(user_id)
    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)

    user.name = user_info['name']
    user.surname = user_info['surname']
    user.address = user_info['address']
    user.email = user_info['email']
    user.position = user_info['position']
    user.speciality = user_info['speciality']
    user.age = user_info['age']
    user.password = user_info['password']
    db_sess.commit()
    return jsonify(
        {'user': user.to_dict(only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email'))})


@user_bp.route('/users_show/<int:user_id>', methods=['GET'])
def users_show(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return make_response(jsonify({'error': "Access denied"}), 403)
    toponym = get_object(user.city_from)
    ll, spn = get_ll_spn(toponym)
    content = get_static_api_image(ll)
    with open('static/img/map.png', mode='wb') as file:
        file.write(content)
    return make_response(jsonify({'users': [
                user.to_dict(only=('surname', 'name', 'city_from'))]}))