from flask import jsonify, make_response
from flask_restful import Resource
from werkzeug.exceptions import NotFound

from SQL.data import db_session
from SQL.data.jobs import Jobs


class JobsResource(Resource):
    def get(self, job_id):
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        if not job:
            raise NotFound('Работа не найдена!')
        return jsonify(
            {'jobs': [
                job.to_dict(only=(
                    'id', 'job', "team_leader", 'work_size', 'collaborators', 'start_date', 'end_date',
                    'is_finished'))]

            }
        )

    def post(self):
        ...


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
        ...
