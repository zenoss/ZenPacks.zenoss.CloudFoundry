import json

from Products.ZenRRD.CommandParser import CommandParser

class app(CommandParser):
    def processResults(self, cmd, result):
        data = json.loads(cmd.result.output)

        for point in cmd.points:
            component = cmd.points[0].component

            app = None
            for x in data['apps']:
                if x['name'] == component:
                    app = x
                    break
            else:
                # No matching app found.
                return result

            instances = len(app['instances'])
            resourcesMemory = app['resources']['memory'] * 1024 * 1024
            resourcesDisk = app['resources']['disk'] * 1024 * 1024

            uptimeAverage = 0.0
            usageCPUAverage = 0.0
            usageMemory = 0
            usageDisk = 0

            for instance in app['instances']:
                stats = instance['stats']['stats']
                uptimeAverage += stats['uptime']
                usageCPUAverage += stats['usage']['cpu']
                usageMemory += (stats['usage']['mem'] * 1024)
                usageDisk += (stats['usage']['disk'] * 1024)

            uptimeAverage = uptimeAverage / instances
            usageCPUAverage = usageCPUAverage / instances

            utilMemory = (float(usageMemory) / resourcesMemory) * 100.0
            utilDisk = (float(usageDisk) / resourcesDisk) * 100.0

            if point.id == 'instances':
                result.values.append((point, instances))
            elif point.id == 'runningInstances':
                result.values.append((point, app['runningInstances']))
            elif point.id == 'resourcesMemory':
                result.values.append((point, resourcesMemory))
            elif point.id == 'resourcesDisk':
                result.values.append((point, resourcesDisk))
            elif point.id == 'services':
                result.values.append((point, len(app['services'])))
            elif point.id == 'uris':
                result.values.append((point, len(app['uris'])))
            elif point.id == 'uptimeAverage':
                result.values.append((point, uptimeAverage))
            elif point.id == 'usageCPUAverage':
                result.values.append((point, usageCPUAverage))
            elif point.id == 'usageMemory':
                result.values.append((point, usageMemory))
            elif point.id == 'usageDisk':
                result.values.append((point, usageDisk))
            elif point.id == 'utilMemory':
                result.values.append((point, utilMemory))
            elif point.id == 'utilDisk':
                result.values.append((point, utilDisk))

        return result

