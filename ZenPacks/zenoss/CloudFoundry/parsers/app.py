import json

from Products.ZenRRD.CommandParser import CommandParser

class app(CommandParser):
    def processResults(self, cmd, result):
        data = json.loads(cmd.result.output)
        dp_map = dict([(dp.id, dp) for dp in cmd.points])
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
        runningInstances = app['runningInstances']
        resourcesMemory = app['resources']['memory'] * 1024 * 1024
        resourcesDisk = app['resources']['disk'] * 1024 * 1024
        services = len(app['services'])
        uris = len(app['uris'])

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

        if 'instances' in dp_map:
            result.values.append((dp_map['instances'], instances))

        if 'runningInstances' in dp_map:
            result.values.append((
                dp_map['runningInstances'], runningInstances))

        if 'resourcesMemory' in dp_map:
            result.values.append((dp_map['resourcesMemory'], resourcesMemory))

        if 'resourcesDisk' in dp_map:
            result.values.append((dp_map['resourcesDisk'], resourcesDisk))

        if 'services' in dp_map:
            result.values.append((dp_map['services'], services))

        if 'uris' in dp_map:
            result.values.append((dp_map['uris'], uris))

        if 'uptimeAverage' in dp_map:
            result.values.append((dp_map['uptimeAverage'], uptimeAverage))

        if 'usageCPUAverage' in dp_map:
            result.values.append((dp_map['usageCPUAverage'], usageCPUAverage))

        if 'usageMemory' in dp_map:
            result.values.append((dp_map['usageMemory'], usageMemory))

        if 'usageDisk' in dp_map:
            result.values.append((dp_map['usageDisk'], usageDisk))

        if 'utilMemory' in dp_map:
            result.values.append((dp_map['utilMemory'], utilMemory))

        if 'utilDisk' in dp_map:
            result.values.append((dp_map['utilDisk'], utilDisk))

        return result

