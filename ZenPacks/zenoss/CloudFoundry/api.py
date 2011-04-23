import json
import urllib2

class Target(object):
    _target = None
    _email = None
    _password = None
    _token = None

    def __init__(self, target, email, password):
        self._target = target
        self._email = email
        self._password = password

    def _request(self, path, data=None):
        if data and not isinstance(data, basestring):
            data = json.dumps(data)

        req = urllib2.Request(
            url='http://{0}/{1}'.format(self._target, path),
            data=data)

        req.add_header('User-Agent', 'ZenPacks.zenoss.CloudFoundry')
        req.add_header('Content-Type', 'application/json')
        req.add_header('Accept', 'application/json')

        if self._token:
            req.add_header('Authorization', self._token)

        return json.load(urllib2.urlopen(req))

    def _login(self, email=None, password=None):
        if email:
            self._email = email
            self._token = None

        if password:
            self._password = password
            self._token = None

        if self._token:
            return

        self._token = self._request(
            '/users/{0}/tokens'.format(self._email),
            {'password': self._password})['token']

    @property
    def info(self):
        self._login()
        return self._request('/info')

    @property
    def apps(self):
        self._login()
        return self._request('/apps')

    @property
    def systemServices(self):
        self._login()
        return self._request('/info/services')

    @property
    def provisionedServices(self):
        self._login()
        return self._request('/services')

    def getAppInstances(self, app):
        self._login()
        return self._request('/apps/{0}/instances'.format(app))

    def getAppStats(self, app):
        self._login()
        return self._request('/apps/{0}/stats'.format(app))

if __name__ == '__main__':
    import sys
    target = Target(*sys.argv[1:])
    import pdb; pdb.set_trace()
    print "Done."

