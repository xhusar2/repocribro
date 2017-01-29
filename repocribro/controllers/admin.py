import flask
from ..security import permissions
from ..helpers import ViewTab, Badge
from ..models import UserAccount, User, Role, Repository, db


admin = flask.Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('')
@permissions.admin_role.require(404)
def index():
    accounts = UserAccount.query.all()
    roles = Role.query.all()
    repos = Repository.query.all()
    exts = []  # TODO: gather extensions

    tabs = [
        ViewTab(
            'users', 'Users', 0,
            flask.render_template('admin/tabs/users.html', accounts=accounts),
            octicon='person', badge=Badge(len(accounts))
        ),
        ViewTab(
            'roles', 'Roles', 0,
            flask.render_template('admin/tabs/roles.html', roles=roles),
            octicon='briefcase', badge=Badge(len(roles))
        ),
        ViewTab(
            'repos', 'Repositories', 0,
            flask.render_template('admin/tabs/repos.html', repos=repos),
            octicon='repo', badge=Badge(len(repos))
        ),
        ViewTab(
            'exts', 'Extensions', 0,
            flask.render_template('admin/tabs/exts.html', exts=exts),
            octicon='code', badge=Badge(len(exts))
        ),
    ]

    return flask.render_template('admin/index.html',
                                 tabs=tabs, active_tab='users')


@admin.route('/account/<login>')
@permissions.admin_role.require(404)
def account_detail(login):
    user = User.query.filter_by(login=login).first_or_404()
    return flask.render_template('admin/account.html', user=user)


@admin.route('/account/<login>/ban', methods=['POST'])
@permissions.admin_role.require(404)
def account_ban(login):
    user = User.query.filter_by(login=login).first_or_404()
    ban = flask.request.form.get('active') == '0'
    unban = flask.request.form.get('active') == '1'
    if user.user_account.active and ban:
        user.user_account.active = False
        db.session.commmit()
        flask.flash('User account {} has been disabled.'.format(login),
                    'success')
    elif not user.user_account.active and unban:
        user.user_account.active = True
        db.session.commmit()
        flask.flash('User account {} has been enabled.'.format(login),
                    'success')
    else:
        flask.flash('Nope, no action has been performed', 'info')
    return flask.redirect(
        flask.url_for('admin.account_detail', login=login)
    )


@admin.route('/account/<login>/delete', methods=['POST'])
@permissions.admin_role.require(404)
def account_delete(login):
    user = User.query.filter_by(login=login).first_or_404()
    db.session.delete(user.user_account)
    db.session.commit()
    flask.flash('User account {} with the all related data'
                ' has been deleted'.format(login), 'success')
    return flask.redirect(
        flask.url_for('admin.index', tab='users')
    )


@admin.route('/repository/<login>/<reponame>')
@permissions.admin_role.require(404)
def repo_detail(login, reponame):
    repo = Repository.query.filter_by(
        full_name=Repository.make_full_name(login, reponame)
    ).first_or_404()
    return flask.render_template(
        'admin/repo.html',
        repo=repo, Repository=Repository
    )


@admin.route('/repository/<login>/<reponame>/visibility', methods=['POST'])
@permissions.admin_role.require(404)
def repo_visibility(login, reponame):
    repo = Repository.query.filter_by(
        full_name=Repository.make_full_name(login, reponame)
    ).first_or_404()
    visibility_type = flask.request.form.get('enable', type=int)
    if visibility_type not in (
            Repository.VISIBILITY_HIDDEN,
            Repository.VISIBILITY_PRIVATE,
            Repository.VISIBILITY_PUBLIC
    ):
        flask.flash('You\'ve requested something weird...', 'error')
        return flask.redirect(
            flask.url_for('admin.repo_detail', login=login, reponame=reponame)
        )

    repo.visibility_type = visibility_type
    if repo.visibility_type == Repository.VISIBILITY_HIDDEN:
        repo.generate_secret()
    db.session.commit()
    flask.flash('The visibility of repository {}  has been '
                'updated'.format(repo.full_name), 'success')
    return flask.redirect(
        flask.url_for('admin.repo_detail', login=login, reponame=reponame)
    )


@admin.route('/repository/<login>/<reponame>/delete', methods=['POST'])
@permissions.admin_role.require(404)
def repo_delete(login, reponame):
    repo = Repository.query.filter_by(
        full_name=Repository.make_full_name(login, reponame)
    ).first_or_404()
    db.session.delete(repo)
    db.session.commit()
    flask.flash('Repository {} with the all related data has '
                'been deleted'.format(repo.full_name), 'success')
    return flask.redirect(
        flask.url_for('admin.index', tab='repos')
    )

@admin.route('/role/<name>')
@permissions.admin_role.require(404)
def role_detail(name):
    role = Role.query.filter_by(name=name).first_or_404()
    return flask.render_template('admin/role.html', role=role)
