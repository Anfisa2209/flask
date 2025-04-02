from flask import jsonify
from flask_restful import Resource
from werkzeug.exceptions import NotFound

from SQL.data import db_session
from SQL.data.jobs import Jobs
from api_v2.reqparse_job import parser


class JobsResource(Resource):
    def get(self, job_id):
        session = db_session.create_session()
        job = session.get(Jobs, job_id)
        if not job:
            raise NotFound('Работа не найдена!')
        return jsonify(
            {'jobs': [
                job.to_dict(only=(
                    'id', 'job', "team_leader", 'work_size', 'collaborators', 'start_date', 'end_date',
                    'is_finished'))]

            }
        )

    def delete(self, job_id):
        db_sess = db_session.create_session()
        job = db_sess.get(Jobs, job_id)
        if not job:
            raise NotFound('Работа не найдена!')
        db_sess.delete(job)
        db_sess.commit()
        return jsonify({'success': 'OK'})

    def put(self, job_id):
        args = parser.parse_args()
        session = db_session.create_session()

        job = session.get(Jobs, job_id)
        if not job:
            raise NotFound('Работа не найдена!')

        job.job = args['job']
        job.team_leader = args['team_leader']
        job.work_size = args['work_size']
        job.collaborators = args['collaborators']
        job.is_finished = args['is_finished']
        session.commit()
        return jsonify({'job': job.to_dict(only=('id', 'job', 'team_leader', 'work_size', 'collaborators', 'is_finished'
                                                 ))})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify(
            {'jobs': (
                [item.to_dict(only=(
                    'id', 'job', 'team_leader', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished'))
                    for
                    item in jobs])

            }
        )

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        job = Jobs(job=args['job'],
                   collaborators=args['collaborators'],
                   team_leader=args['team_leader'],
                   work_size=args['work_size'],
                   is_finished=args['is_finished'])
        session.add(job)
        session.commit()
        return jsonify({'job': job.to_dict(only=('id', 'job', 'team_leader', 'work_size', 'collaborators', 'is_finished'
                                                 ))})
