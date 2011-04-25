from zope.component import adapts
from zope.interface import implements

from Products.Zuul.decorators import info
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.component import ComponentInfo
from Products.Zuul.infos.device import DeviceInfo

from ZenPacks.zenoss.CloudFoundry.Endpoint import Endpoint
from ZenPacks.zenoss.CloudFoundry.App import App
from ZenPacks.zenoss.CloudFoundry.AppInstance import AppInstance
from ZenPacks.zenoss.CloudFoundry.Framework import Framework
from ZenPacks.zenoss.CloudFoundry.Runtime import Runtime
from ZenPacks.zenoss.CloudFoundry.AppServer import AppServer
from ZenPacks.zenoss.CloudFoundry.SystemService import SystemService
from ZenPacks.zenoss.CloudFoundry.ProvisionedService import ProvisionedService

from ZenPacks.zenoss.CloudFoundry.interfaces import (
    IEndpointInfo, IAppInfo, IAppInstanceInfo, IFrameworkInfo, IRuntimeInfo,
    IAppServerInfo, ISystemServiceInfo, IProvisionedServiceInfo
)

from ZenPacks.zenoss.CloudFoundry.util import CollectedOrModeledProperty

class EndpointInfo(DeviceInfo):
    implements(IEndpointInfo)
    adapts(Endpoint)

    cfName = ProxyProperty('cfName')
    cfDescription = ProxyProperty('cfDescription')
    cfVersion = ProxyProperty('cfVersion')
    cfBuild = ProxyProperty('cfBuild')
    cfUser = ProxyProperty('cfUser')
    cfSupport = ProxyProperty('cfSupport')
    limitAppURIs = CollectedOrModeledProperty('limitAppURIs')
    limitApps = CollectedOrModeledProperty('limitApps')
    limitMemory = CollectedOrModeledProperty('limitMemory')
    limitServices = CollectedOrModeledProperty('limitServices')
    usageApps = CollectedOrModeledProperty('usageApps')
    usageMemory = CollectedOrModeledProperty('usageMemory')
    usageServices = CollectedOrModeledProperty('usageServices')

    @property
    def utilAppURIs(self):
        return "{0} / {1}".format('?', self.limitAppURIs)

    @property
    def utilApps(self):
        return "{0} / {1}".format(self.usageApps, self.limitApps)

    @property
    def utilMemory(self):
        return "{0} / {1}".format(self.usageMemory, self.limitMemory)

    @property
    def utilServices(self):
        return "{0} / {1}".format(self.usageServices, self.limitServices)

class CloudFoundryComponentInfo(ComponentInfo):
    @property
    def entity(self):
        return {
            'uid': self._object.getPrimaryUrlPath(),
            'name': self._object.titleOrId(),
            }

class AppInfo(CloudFoundryComponentInfo):
    implements(IAppInfo)
    adapts(App)

    cfName = ProxyProperty('cfName')
    cfVersion = ProxyProperty('cfVersion')
    cfState = ProxyProperty('cfState')
    cfMetaCreated = ProxyProperty('cfMetaCreated')
    cfMetaVersion = ProxyProperty('cfMetaVersion')
    cfURIs = ProxyProperty('cfURIs')
    cfServices = ProxyProperty('cfServices')

    instances = CollectedOrModeledProperty('instances')
    runningInstances = CollectedOrModeledProperty('runningInstances')
    resourcesMemory = CollectedOrModeledProperty('resourcesMemory')
    resourcesDisk = CollectedOrModeledProperty('resourcesDisk')
    resourcesFDS = CollectedOrModeledProperty('resourcesFDS')

class AppInstanceInfo(CloudFoundryComponentInfo):
    implements(IAppInstanceInfo)
    adapts(AppInstance)

    cfIndex = ProxyProperty("cfIndex")
    cfState = ProxyProperty("cfState")
    cfSince = ProxyProperty("cfSince")

    @property
    @info
    def cfApp(self):
        return self._object.cfApp()

class FrameworkInfo(CloudFoundryComponentInfo):
    implements(IFrameworkInfo)
    adapts(Framework)

    cfName = ProxyProperty("cfName")
    cfDetection = ProxyProperty("cfDetection")

    @property
    def cfDetection(self):
        detections = []
        for detection in self._object.cfDetection:
            glob, rule = detection.items()[0]
            if rule == True:
                detections.append(glob)
            elif rule == False:
                detections.append("!{0}".format(glob))
            else:
                detections.append("{0} ({1})".format(glob, rule))

        return detections

    @property
    def cfRuntimeCount(self):
        return len(self._object.cfRuntimes.objectIds())

    @property
    def cfAppServerCount(self):
        return len(self._object.cfAppServers.objectIds())

class RuntimeInfo(CloudFoundryComponentInfo):
    implements(IRuntimeInfo)
    adapts(Runtime)

    cfName = ProxyProperty("cfName")
    cfDescription = ProxyProperty("cfDescription")
    cfVersion = ProxyProperty("cfVersion")

    @property
    @info
    def cfFramework(self):
        return self._object.cfFramework()

class AppServerInfo(CloudFoundryComponentInfo):
    implements(IAppServerInfo)
    adapts(AppServer)

    cfName = ProxyProperty("cfName")
    cfDescription = ProxyProperty("cfDescription")
    cfVersion = ProxyProperty("cfVersion")

    @property
    @info
    def cfFramework(self):
        return self._object.cfFramework()

class SystemServiceInfo(CloudFoundryComponentInfo):
    implements(ISystemServiceInfo)
    adapts(SystemService)

    cfId = ProxyProperty("cfId")
    cfName = ProxyProperty("cfName")
    cfDescription = ProxyProperty("cfDescription")
    cfVersion = ProxyProperty("cfVersion")
    cfVendor = ProxyProperty("cfVendor")
    cfType = ProxyProperty("cfType")
    cfTiers = ProxyProperty("cfTiers")

    @property
    def cfProvisionedCount(self):
        count = 0
        for service in self._object.cfEndpoint().cfProvisionedServices():
            if service.cfType == self._object.cfType \
                and service.cfVendor == self._object.cfVendor \
                and service.cfVersion == self._object.cfVersion:
                count += 1

        return count

class ProvisionedServiceInfo(CloudFoundryComponentInfo):
    implements(IProvisionedServiceInfo)
    adapts(ProvisionedService)

    cfName = ProxyProperty("cfName")
    cfVersion = ProxyProperty("cfVersion")
    cfVendor = ProxyProperty("cfVendor")
    cfType = ProxyProperty("cfType")
    cfTier = ProxyProperty("cfTier")
    cfMetaCreated = ProxyProperty("cfMetaCreated")
    cfMetaUpdated = ProxyProperty("cfMetaUpdated")
    cfMetaVersion = ProxyProperty("cfMetaVersion")
    cfMetaTags = ProxyProperty("cfMetaTags")
    cfProperties = ProxyProperty("cfProperties")

    @property
    @info
    def cfSystemService(self):
        for service in self._object.cfEndpoint().cfSystemServices():
            if service.cfType == self._object.cfType \
                and service.cfVendor == self._object.cfVendor \
                and service.cfVersion == self._object.cfVersion:
                return service

        return None

