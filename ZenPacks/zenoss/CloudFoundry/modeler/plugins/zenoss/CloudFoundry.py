import logging
log = logging.getLogger('zen.CloudFoundry')

from Products.DataCollector.plugins.CollectorPlugin import PythonPlugin
from Products.DataCollector.plugins.DataMaps import ObjectMap, RelationshipMap
from Products.ZenUtils.Utils import prepId

from ZenPacks.zenoss.CloudFoundry.api import Target

class CloudFoundry(PythonPlugin):
    deviceProperties = PythonPlugin.deviceProperties + (
        'zCloudFoundryTarget',
        'zCloudFoundryEmail',
        'zCloudFoundryPassword',
    )

    def collect(self, device, unused):
        target = Target(
            device.zCloudFoundryTarget,
            device.zCloudFoundryEmail,
            device.zCloudFoundryPassword)

        log.info('Requesting system-wide information')
        results = {
            'info': target.info,
            'apps': target.apps,
            'systemServices': target.systemServices,
            'provisionedServices': target.provisionedServices,
        }

        # app_uris exists under info/limits, but not info/usage. Resolving.
        results['info']['usage']['app_uris'] = 0

        log.info('Requesting app-specific information')
        for app in results['apps']:
            name = app['name']

            # See note about app_uris above.
            results['info']['usage']['app_uris'] += len(app['uris'])

            log.info('  .. instances for {0}'.format(name))
            app['instances'] = target.getAppInstances(name)['instances']

            log.info('  .. stats for {0}'.format(name))
            app_stats = target.getAppStats(name)

            for instance in app['instances']:
                instance['stats'] = app_stats[str(instance['index'])]

        return results

    def process(self, device, results, unused):
        maps = []

        # Endpoint ObjectMap
        info = results['info']
        maps.append(self.objectMap(dict(
            cfName=info['name'],
            cfDescription=info['description'],
            cfVersion=info['version'],
            cfBuild=info['build'],
            cfUser=info['user'],
            cfSupport=info['support'],
            modeled_limitAppURIs=info['limits']['app_uris'],
            modeled_limitApps=info['limits']['apps'],
            modeled_limitMemory=info['limits']['memory'] * 1024 * 1024,
            modeled_limitServices=info['limits']['services'],
            modeled_usageAppURIs=info['usage']['app_uris'],
            modeled_usageApps=info['usage']['apps'],
            modeled_usageMemory=info['usage']['memory'] * 1024 * 1024,
            modeled_usageServices=info['usage']['services'],
        )))

        # Component RelationshipMaps
        maps.extend(self.getAppsRelMaps(results['apps']))
        maps.extend(self.getFrameworksRelMaps(results['info']['frameworks']))
        maps.extend(self.getSystemServicesRelMaps(results['systemServices']))
        maps.extend(self.getProvisionedServicesRelMaps(
            results['provisionedServices']))

        return maps

    def getAppsRelMaps(self, apps):
        obj_maps = []
        rel_maps = []

        for data in apps:
            app_id = prepId(data['name'])
            obj_maps.append(ObjectMap(data=dict(
                id=app_id,
                title=data['name'],
                cfName=data['name'],
                cfVersion=data['version'],
                cfState=data['state'],
                cfMetaCreated=data['meta']['created'],
                cfMetaVersion=data['meta']['version'],
                setCFURIs=data['uris'],
                setCFServices=data['services'],
                cfStagingModel=data['staging']['model'],
                cfStagingStack=data['staging']['stack'],
                modeled_instances=len(data['instances']),
                modeled_runningInstances=data['runningInstances'],
                modeled_resourcesMemory=data['resources']['memory'] * 1048576,
                modeled_resourcesDisk=data['resources']['disk'] * 1048576,
                modeled_resourcesFDS=data['resources']['fds']
            )))

            rel_maps.extend(self.getAppInstancesRelMaps(
                data['instances'], 'cfApps/{0}'.format(app_id)))

        return [RelationshipMap(
            relname='cfApps',
            modname='ZenPacks.zenoss.CloudFoundry.App',
            objmaps=obj_maps)] + rel_maps

    def getAppInstancesRelMaps(self, instances, compname):
        obj_maps = []

        for data in instances:
            instance_id = prepId(str(data['index']))
            stats = data['stats']['stats']
            obj_maps.append(ObjectMap(data=dict(
                id=instance_id,
                title=instance_id,
                cfIndex=data['index'],
                cfState=data['state'],
                cfSince=data['since'],
                cfCores=stats['cores'],
                cfHost=stats['host'],
                cfPort=stats['port'],
                modeled_memoryQuota=stats['mem_quota'],
                modeled_diskQuota=stats['disk_quota'],
                modeled_fdsQuota=stats['fds_quota'],
                modeled_uptime=stats['uptime'],
                modeled_usageCPU=stats['usage']['cpu'],
                modeled_usageMemory=stats['usage']['mem'],
                modeled_usageDisk=stats['usage']['disk'],
            )))

        return [RelationshipMap(
            compname=compname,
            relname='cfAppInstances',
            modname='ZenPacks.zenoss.CloudFoundry.AppInstance',
            objmaps=obj_maps)]

    def getFrameworksRelMaps(self, frameworks):
        rel_maps = []
        obj_maps = []

        for name, data in frameworks.items():
            framework_id = prepId(name)
            obj_maps.append(ObjectMap(data=dict(
                id=framework_id,
                title=name,
                cfName=name,
                setCFDetection=data['detection'],
            )))

            rel_maps.extend(self.getRuntimesRelMaps(
                data['runtimes'], 'cfFrameworks/{0}'.format(framework_id)))

            rel_maps.extend(self.getAppServersRelMaps(
                data['appservers'], 'cfFrameworks/{0}'.format(framework_id)))

        return [RelationshipMap(
            relname='cfFrameworks',
            modname='ZenPacks.zenoss.CloudFoundry.Framework',
            objmaps=obj_maps)] + rel_maps

    def getRuntimesRelMaps(self, runtimes, compname):
        obj_maps = []

        for data in runtimes:
            obj_maps.append(ObjectMap(data=dict(
                id=prepId(data['name']),
                title=data['name'],
                cfName=data['name'],
                cfDescription=data['description'],
                cfVersion=data['version'],
            )))

        return [RelationshipMap(
            compname=compname,
            relname='cfRuntimes',
            modname='ZenPacks.zenoss.CloudFoundry.Runtime',
            objmaps=obj_maps)]

    def getAppServersRelMaps(self, appservers, compname):
        obj_maps = []

        for data in appservers:
            obj_maps.append(ObjectMap(data=dict(
                id=prepId(data['name']),
                title=data['name'],
                cfName=data['name'],
                cfDescription=data['description'],
                cfVersion=data.get('version', ''),
            )))

        return [RelationshipMap(
            compname=compname,
            relname='cfAppServers',
            modname='ZenPacks.zenoss.CloudFoundry.AppServer',
            objmaps=obj_maps)]

    def getSystemServicesRelMaps(self, services):
        obj_maps = []

        for type, type_data in services.items():
            for name, name_data in type_data.items():
                for version, data in name_data.items():
                    obj_maps.append(ObjectMap(data=dict(
                        id=prepId(data['id']),
                        title=name,
                        cfId=data['id'],
                        cfName=name,
                        cfVersion=data['version'],
                        cfDescription=data['description'],
                        cfVendor=data['vendor'],
                        cfType=type,
                        setCFTiers=data['tiers'],
                    )))

        return [RelationshipMap(
            relname='cfSystemServices',
            modname='ZenPacks.zenoss.CloudFoundry.SystemService',
            objmaps=obj_maps)]

    def getProvisionedServicesRelMaps(self, services):
        obj_maps = []

        for data in services:
            obj_maps.append(ObjectMap(data=dict(
                id=prepId(data['name']),
                title=data['name'],
                cfName=data['name'],
                cfVersion=data['version'],
                cfVendor=data['vendor'],
                cfType=data['type'],
                cfTier=data['tier'],
                cfMetaCreated=data['meta']['created'],
                cfMetaUpdated=data['meta']['updated'],
                cfMetaVersion=data['meta']['version'],
                setCFMetaTags=data['meta']['tags'],
                setCFProperties=data['properties'],
            )))

        return [RelationshipMap(
            relname='cfProvisionedServices',
            modname='ZenPacks.zenoss.CloudFoundry.ProvisionedService',
            objmaps=obj_maps)]

