import flask
import flask_migrate

from .extending import Extension
from .extending.helpers import ViewTab, Badge


class ExquiroExtension(Extension):
    #: Name of core extension
    NAME = 'exquiro'
    #: Category of core extension
    CATEGORY = 'basic'
    #: Author of core extension
    AUTHOR = 'Richard Husar'
    #: GitHub URL of core extension
    GH_URL = 'to be specified'
    #: Priority of core extension
    PRIORITY = 1

    def __init__(self, master, app, db):
        super().__init__(master, app, db)
        self.migrate = flask_migrate.Migrate(self.app, self.db)

    def view_core_search_tabs(self, query, tabs_dict):
        """Prepare tabs for search view of core controller

        :param query: Fulltext query for the search
        :type query: str
        :param tabs_dict: Target dictionary for tabs
        :type tabs_dict: dict of str: ``repocribro.extending.helpers.ViewTab``
        """
        from .models import Repository
        if query == '':
            repos = self.db.session.query(Repository).all()
        else:
            repos = Repository.fulltext_query(
                query, self.db.session.query(Repository)
            ).all()

        tabs_dict['exquiro'] = ViewTab(
            'exquiro', 'Exquiro', 4,
            flask.render_template('exquiro/search/exquiro_tab.html', repos=repos),
            octicon='squirrel-16', badge=Badge(len(repos))
        )

        tabs_dict['neovis'] = ViewTab(
            'neovis', 'Neovis', 5,
            flask.render_template('exquiro/search/neovis_test.html'),
            octicon='repo-forked', badge=Badge(len(repos))
        )


def make_extension(*args, **kwargs):
    """Alias for instantiating the extension

    Actually not needed, just example that here can be something
    more complex to do before creating the extension.
    """
    return ExquiroExtension(*args, **kwargs)
