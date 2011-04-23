import logging
log = logging.getLogger('zen.CloudFoundryLoader')

from zope.interface import implements

from Products.Zuul import getFacade
from Products.ZenModel.interfaces import IDeviceLoader

class CloudFoundryLoader(object):
    """
    Loader for the CloudFoundry ZenPack.
    """
    implements(IDeviceLoader)

    def load_device(self, dmd, target, email, password, collector):
        return getFacade('cloudfoundry', dmd).addEndpoint(
            target, email, password, collector)

