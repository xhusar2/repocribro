import flask
from flask import jsonify, url_for
from ..models import Repository
from ..tasks import celery
from ..security import permissions

# Exquiro controller blueprint
exquiro_bp = flask.Blueprint('exquiro', __name__, url_prefix='/exquiro')


@permissions.actions.browse_repo.require(403)
@exquiro_bp.route('/add_to_neo4j/<owner>/<repo>', methods=['GET', 'POST'])
def add_to_neo4j(owner, repo):
    task = celery.send_task(name='add_to_db_async', args=[repo, owner])
    flask.flash('Started to parse {}'.format(repo), 'info')
    return jsonify({}), 202, {'Location': url_for('exquiro.taskstatus', owner=owner, repo=repo,
                                                 task_id=task.id)}


@permissions.actions.browse_repo.require(403)
@exquiro_bp.route('/delete_from_neo4j/<owner>/<repo>', methods=['GET', 'POST'])
def delete_from_neo4j(owner, repo):
    task = celery.send_task(name='delete_from_db_async', args=[repo, owner])
    flask.flash('Started to delete models from {}'.format(repo), 'info')
    return jsonify({}), 202, {'Location': url_for('exquiro.taskstatus', owner=owner, repo=repo,
                                                  task_id=task.id)}


@permissions.actions.browse_repo.require(403)
@exquiro_bp.route('/status/<owner>/<repo>/<task_id>')
def taskstatus(owner, repo, task_id):
    task = celery.AsyncResult(task_id)
    db = flask.current_app.container.get('db')
    full_name = owner+'/'+repo
    repo_db = db.session.query(Repository).filter_by(full_name=full_name).first()
    if task.state == 'PENDING':
        # job did not start yet
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
        if repo_db is not None:
            repo_db.update_neo4j_data({'status': "Processing"})
            db.session.commit()
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'models_recognized' in task.info and repo_db is not None:
            response['models_recognized'] = task.info['models_recognized']
            if 'models_added' in task.info:
                response['models_added'] = task.info['models_added']
                repo_db.update_neo4j_data({'status': task.state,
                                           'recognized': task.info['models_recognized'],
                                           'added': task.info['models_added']
                                           })
            if 'models_deleted' in task.info:
                response['models_deleted'] = task.info['models_deleted']
                repo_db.update_neo4j_data({'status': task.state,
                                    'recognized': task.info['models_recognized'],
                                    'deleted': task.info['models_deleted']

                                    })
            db.session.commit()

    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)
