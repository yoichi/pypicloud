""" Backend that defers to another server for access control """
from .base import IAccessBackend


class RemoteAccessBackend(IAccessBackend):

    """
    This backend allows you to defer all user auth and permissions to a remote
    server. It requires the ``requests`` package.

    """

    @classmethod
    def configure(cls, settings):
        super(RemoteAccessBackend, cls).configure(settings)
        cls._settings = settings
        cls.server = settings['auth.backend_server']
        cls.auth = None
        user = settings.get('auth.user')
        if user is not None:
            password = settings.get('auth.password')
            cls.auth = (user, password)

    def _req(self, uri, params=None):
        """ Hit a server endpoint and return the json response """
        import requests
        response = requests.get(self.server + uri, params=params,
                                auth=self.auth)
        response.raise_for_status()
        return response.json()

    def verify_user(self, username, password):
        uri = self._settings.get('auth.uri.verify', '/verify')
        params = {'username': username, 'password': password}
        return self._req(uri, params)

    def _get_password_hash(self, username):
        # We don't have to do anything here because we overrode 'verify_user'
        pass

    def groups(self, username=None):
        uri = self._settings.get('auth.uri.groups', '/groups')
        params = {}
        if username is not None:
            params['username'] = username
        return self._req(uri, params)

    def group_members(self, group):
        uri = self._settings.get('auth.uri.group_members', '/group_members')
        params = {'group': group}
        return self._req(uri, params)

    def is_admin(self, username):
        uri = self._settings.get('auth.uri.admin', '/admin')
        params = {'username': username}
        return self._req(uri, params)

    def group_permissions(self, package, group=None):
        uri = self._settings.get('auth.uri.group_permissions',
                                 '/group_permissions')
        params = {'package': package}
        if group is not None:
            params['group'] = group
        return self._req(uri, params)

    def user_permissions(self, package, username=None):
        uri = self._settings.get('auth.uri.user_permissions',
                                 '/user_permissions')
        params = {'package': package}
        if username is not None:
            params['username'] = username
        return self._req(uri, params)

    def user_package_permissions(self, username):
        uri = self._settings.get('auth.uri.user_package_permissions',
                                 '/user_package_permissions')
        params = {'username': username}
        return self._req(uri, params)

    def group_package_permissions(self, group):
        uri = self._settings.get('auth.uri.group_package_permissions',
                                 '/group_package_permissions')
        params = {'group': group}
        return self._req(uri, params)

    def user_data(self, username=None):
        uri = self._settings.get('auth.uri.user_data',
                                 '/user_data')
        params = None
        if username is not None:
            params = {'username': username}
        return self._req(uri, params)