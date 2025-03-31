import flask
from flask import request, make_response, jsonify

from SQL.data import db_session
from SQL.data.jobs import Jobs

jobs_bp = flask.Blueprint('jobs_api', __name__)


@jobs_bp.route('/jobs')
def get_all_jobs():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return jsonify(
        {'jobs': (
            [item.to_dict(only=(
                'id', 'job', 'team_leader', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished')) for
                item in jobs])

        }
    )


@jobs_bp.route('/jobs/<int:job_id>', methods=['GET'])
def get_one_job(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if job:
        return jsonify(
            {'jobs': [
                job.to_dict(only=(
                    'id', 'job', "team_leader", 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished'))]

            }
        )
    return make_response(jsonify({'error': 'Not found'}), 404)


@jobs_bp.route('/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@jobs_bp.route('/jobs', methods=['POST'])
def create_one_job():
    job = request.json
    if not job:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in job for key in ["collaborators", "is_finished", "job", "team_leader", "work_size"]):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    new_job = Jobs(
        job=job['job'],
        collaborators=job['collaborators'],
        team_leader=job['team_leader'],
        work_size=job['work_size'],
        is_finished=job['is_finished']
    )
    db_sess.add(new_job)
    db_sess.commit()
    return jsonify({'id': new_job.id})


@jobs_bp.route('/jobs/<int:job_id>', methods=['PUT'])
def edit_one_job(job_id):
    job_info = request.json
    if not job_info:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in job_info for key in ["collaborators", "is_finished", "job", "team_leader", "work_size"]):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()

    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)

    job.job = job_info['job']
    job.team_leader = job_info['team_leader']
    job.work_size = job_info['work_size']
    job.collaborators = job_info['collaborators']
    job.is_finished = job_info['is_finished']
    db_sess.commit()
    return jsonify({'job': job.to_dict(only=(
        'id', 'job', 'team_leader', 'work_size',
        'collaborators', 'start_date', 'end_date',
        'is_finished'
    ))})
