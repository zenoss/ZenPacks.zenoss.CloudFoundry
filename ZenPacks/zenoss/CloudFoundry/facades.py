import logging
from zope.interface import implements
from Products.Zuul.facades import ZuulFacade
from Products.Zuul.utils import ZuulMessageFactory as _t
from ZenPacks.zenoss.CloudFoundry.interfaces import ICloudFoundryFacade

CLOUDFOUNDRY_DEVICE_PATH = "/Devices/CloudFoundry"

log = logging.getLogger('zen.CloudFoundryFacade')

class CloudFoundryFacade(ZuulFacade):
    """
    Facade for the CloudFoundry ZenPack.
    """

    implements(ICloudFoundryFacade)

    def addEndpoint(self, target, email, password, collector):
        """
        Handles adding a new CloudFoundry endpoint to the system.
        """

        # Verify that this device does not already exist.
        deviceRoot = self._dmd.getDmdRoot("Devices")
        device = deviceRoot.findDeviceByIdExact(target)
        if device:
            return False, _t("A device named %s already exists." % target)

        # If all is well, submit a discovery job for the new cell to be added
        # as a Zenoss device.
        zProperties = {
            'zCloudFoundryTarget': target,
            'zCloudFoundryEmail': email,
            'zCloudFoundryPassword': password,
            }

        # TODO: allow user to specify the collector?
        perfConf = self._dmd.Monitors.getPerformanceMonitor(collector)
        jobStatus = perfConf.addDeviceCreationJob(deviceName=target,
                devicePath=CLOUDFOUNDRY_DEVICE_PATH,
                performanceMonitor=collector,
                discoverProto='python',
                zProperties=zProperties)

        # Redirect the user to the job status page so that they can view the
        # output of the discovery job immediately.
        return True, jobStatus.id

