from zope.component import adapts
from zope.interface import implements

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

class AppInfo(ComponentInfo):
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

class AppInstanceInfo(ComponentInfo):
    implements(IAppInstanceInfo)
    adapts(AppInstance)

class FrameworkInfo(ComponentInfo):
    implements(IFrameworkInfo)
    adapts(Framework)

class RuntimeInfo(ComponentInfo):
    implements(IRuntimeInfo)
    adapts(Runtime)

class AppServerInfo(ComponentInfo):
    implements(IAppServerInfo)
    adapts(AppServer)

class SystemServiceInfo(ComponentInfo):
    implements(ISystemServiceInfo)
    adapts(SystemService)

class ProvisionedServiceInfo(ComponentInfo):
    implements(IProvisionedServiceInfo)
    adapts(ProvisionedService)

