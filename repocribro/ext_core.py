import flask
import flask_bower
import flask_login
import flask_migrate

from .extending import Extension
from .extending.helpers import ViewTab, Badge
from .models import Push, Release, Repository


def gh_webhook_push(db, repo, data, delivery_id):
    """Process push webhook msg

    :todo: deal with limit of commits in webhook msg (20)
    """
    push = Push.create_from_dict(data['push'], data['sender'], repo)
    db.session.add(push)
    for commit in push.commits:
        db.session.add(commit)


def gh_webhook_release(db, repo, data, delivery_id):
    """Process release webhook msg"""
    release = Release.create_from_dict(data['release'], data['sender'], repo)
    db.session.add(release)


def gh_webhook_repository(db, repo, data, delivery_id):
    """Process repository webhook msg

    This can be one of "created", "deleted", "publicized", or "privatized".

    :todo: find out where is "updated" action
    """
    action = data['action']
    if action == 'privatized':
        repo.private = True
        repo.visibility_type = Repository.VISIBILITY_PRIVATE
    elif action == 'publicized':
        repo.private = False
        repo.visibility_type = Repository.VISIBILITY_PUBLIC
    elif action == 'deleted':
        # TODO: consider some signalization of not being @GitHub anymore
        repo.webhook_id = None
        repo.visibility_type = Repository.VISIBILITY_PRIVATE


# AWESOME EVENTS ARE DIFFERENT THAN WEBHOOK MSGS!!
def gh_event_push(db, repo, payload):
    """Process push event msg

    :todo: implement
    """
    pass


def gh_event_release(db, repo, payload):
    """Process release event msg

    :todo: implement
    """
    pass


def gh_event_repository(db, repo, payload):
    """Process repository event msg

    This can be one of "created", "deleted", "publicized", or "privatized".

    :todo: implement
    """
    pass


class CoreExtension(Extension):
    #: Name of core extension
    NAME = 'core'
    #: Category of core extension
    CATEGORY = 'basic'
    #: Author of core extension
    AUTHOR = 'Marek Suchánek'
    #: GitHub URL of core extension
    GH_URL = 'https://github.com/MarekSuchanek/repocribro'

    def __init__(self, master, app, db, *args, **kwargs):
        super().__init__(master, app, db)
        self.bower = flask_bower.Bower(self.app)
        self.migrate = flask_migrate.Migrate(self.app, self.db)

    @staticmethod
    def provide_models():
        from .models import all_models
        return all_models

    @staticmethod
    def provide_blueprints():
        from .controllers import all_blueprints
        return all_blueprints

    @staticmethod
    def provide_filters():
        from .filters import all_filters
        return all_filters

    @staticmethod
    def get_gh_webhook_processors(*args, **kwargs):
        """"""
        return {
            'push': [gh_webhook_push],
            'release': [gh_webhook_release],
            'repository': [gh_webhook_repository],
        }

    @staticmethod
    def get_gh_event_processors(*args, **kwargs):
        """"""
        return {
            'push': [gh_event_push],
            'release': [gh_event_release],
            'repository': [gh_event_repository],
        }

    def init_business(self, *args, **kwargs):
        """Init business layer (other extensions, what is needed)

        :param args: not used
        :param kwargs: not used
        """
        from .security import init_login_manager
        login_manager, principals = init_login_manager(self.db)
        login_manager.init_app(self.app)
        principals.init_app(self.app)

    def init_post_injector(self, *args, **kwargs):
        """Init what needs to be done after setting up injector

        :param args: not used
        :param kwargs: not used

        :todo: flask_restless is not compatible with flask_injector!
        """
        from .api import create_api
        api_manager = create_api(self.app, self.db)

    def view_core_search_tabs(self, *args, **kwargs):
        """Prepare tabs for search view of core controller

        :param args: not used
        :param kwargs: Must contain ``query`` and ``tabs_dict``
        """
        query = kwargs.get('query', '')
        tabs_dict = kwargs.get('tabs_dict')

        from .models import User, Organization, Repository
        users = User.fulltext_query(
            query, self.db.session.query(User)
        ).all()
        orgs = Organization.fulltext_query(
            query, self.db.session.query(Organization)
        ).all()
        repos = Repository.fulltext_query(
            query, self.db.session.query(Repository)
        ).all()

        tabs_dict['repositories'] = ViewTab(
            'repositories', 'Repositories', 0,
            flask.render_template('core/search/repos_tab.html', repos=repos),
            octicon='repo', badge=Badge(len(repos))
        )
        tabs_dict['users'] = ViewTab(
            'users', 'Users', 1,
            flask.render_template('core/search/users_tab.html', users=users),
            octicon='person', badge=Badge(len(users))
        )
        tabs_dict['orgs'] = ViewTab(
            'orgs', 'Organizations', 2,
            flask.render_template('core/search/orgs_tab.html', orgs=orgs),
            octicon='organization', badge=Badge(len(orgs))
        )

    def view_core_user_detail_tabs(self, *args, **kwargs):
        """Prepare tabs for user detail view of core controller

        :param args: not used
        :param kwargs: Must contain target ``tabs_dict`` and ``user``
        """
        user = kwargs.get('user')
        tabs_dict = kwargs.get('tabs_dict')

        tabs_dict['details'] = ViewTab(
            'details', 'Details', 0,
            flask.render_template('core/user/details_tab.html', user=user),
            octicon='person'
        )
        tabs_dict['repositories'] = ViewTab(
            'repositories', 'Repositories', 1,
            flask.render_template(
                'core/repo_owner/repositories_tab.html', owner=user
            ),
            octicon='repo', badge=Badge(len(user.repositories))
        )

    def view_core_org_detail_tabs(self, *args, **kwargs):
        """Prepare tabs for org detail view of core controller

        :param args: not used
        :param kwargs: Must contain target ``tabs_dict`` and ``org``
        """
        org = kwargs.get('org')
        tabs_dict = kwargs.get('tabs_dict')

        tabs_dict['details'] = ViewTab(
            'details', 'Details', 0,
            flask.render_template('core/org/details_tab.html', org=org),
            octicon='person'
        )
        tabs_dict['repositories'] = ViewTab(
            'repositories', 'Repositories', 1,
            flask.render_template(
                'core/repo_owner/repositories_tab.html', owner=org
            ),
            octicon='repo', badge=Badge(len(org.repositories))
        )

    def view_core_repo_detail_tabs(self, *args, **kwargs):
        """Prepare tabs for repo detail view of core controller

        :param args: not used
        :param kwargs: Must contain target ``tabs_dict`` and ``repo``
        """
        repo = kwargs.get('repo')
        tabs_dict = kwargs.get('tabs_dict')

        tabs_dict['details'] = ViewTab(
            'details', 'Details', 0,
            flask.render_template('core/repo/details_tab.html', repo=repo),
            octicon='repo'
        )
        tabs_dict['releases'] = ViewTab(
            'releases', 'Releases', 1,
            flask.render_template('core/repo/releases_tab.html', repo=repo),
            octicon='tag', badge=Badge(len(repo.releases))
        )
        tabs_dict['updates'] = ViewTab(
            'updates', 'Updates', 2,
            flask.render_template('core/repo/updates_tab.html', repo=repo),
            octicon='git-commit', badge=Badge(len(repo.pushes))
        )

    def view_admin_index_tabs(self, *args, **kwargs):
        """Prepare tabs for index view of admin controller

        :param args: not used
        :param kwargs: Must contain target ``tabs_dict``
        """
        tabs_dict = kwargs.get('tabs_dict')

        from .models import Repository, Role, UserAccount
        accounts = self.db.session.query(UserAccount).all()
        roles = self.db.session.query(Role).all()
        repos = self.db.session.query(Repository).all()
        exts = [e for e in self.master.call('view_admin_extensions', None)
                if e is not None]

        tabs_dict['users'] = ViewTab(
            'users', 'Users', 0,
            flask.render_template('admin/tabs/users.html', accounts=accounts),
            octicon='person', badge=Badge(len(accounts))
        )
        tabs_dict['roles'] = ViewTab(
            'roles', 'Roles', 1,
            flask.render_template('admin/tabs/roles.html', roles=roles),
            octicon='briefcase', badge=Badge(len(roles))
        )
        tabs_dict['repositories'] = ViewTab(
            'repositories', 'Repositories', 2,
            flask.render_template('admin/tabs/repos.html', repos=repos),
            octicon='repo', badge=Badge(len(repos))
        )
        tabs_dict['extensions'] = ViewTab(
            'extensions', 'Extensions', 3,
            flask.render_template('admin/tabs/exts.html', exts=exts),
            octicon='code', badge=Badge(len(exts))
        )

    def view_manage_dashboard_tabs(self, *args, **kwargs):
        """Prepare tabs for dashboard view of manage controller

        :param args: not used
        :param kwargs: Must contain target ``tabs_dict`` and ``gh_api``
        """
        tabs_dict = kwargs.get('tabs_dict')
        gh_api = kwargs.get('gh_api')

        repos = flask_login.current_user.github_user.repositories

        tabs_dict['repositories'] = ViewTab(
            'repositories', 'Repositories', 0,
            flask.render_template(
                'manage/dashboard/repos_tab.html',
                repos=repos
            ),
            octicon='repo', badge=Badge(len(repos))
        )
        tabs_dict['profile'] = ViewTab(
            'profile', 'Profile', 1,
            flask.render_template(
                'manage/dashboard/profile_tab.html',
                user=flask_login.current_user.github_user
            ),
            octicon='person'
        )
        tabs_dict['session'] = ViewTab(
            'session', 'Session', 2,
            flask.render_template(
                'manage/dashboard/session_tab.html',
                token=gh_api.get_token(),
                scopes=gh_api.get_scope()
            ),
            octicon='mark-github'
        )


def make_extension(*args, **kwargs):
    """Alias for instantiating the extension

    Actually not needed, just example that here can be something
    more complex to do before creating the extension.
    """
    return CoreExtension(*args, **kwargs)
