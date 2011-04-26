import json

from Products.ZenRRD.CommandParser import CommandParser

class appinstance(CommandParser):
    def processResults(self, cmd, result):
        data = json.loads(cmd.result.output)

        for point in cmd.points:
            component_parts = point.component.split('_')
            app_name = '_'.join(component_parts[:-1])
            instance_index = component_parts[-1]

            instance = None
            for x in data['apps']:
                if x['name'] != app_name:
                    continue

                for y in x['instances']:
                    if str(y['index']) != instance_index:
                        continue

                    instance = y
                    break

                if instance:
                    break
            else:
                # No matching instance found.
                return result

            stats = instance['stats']['stats']
            quotaMemory = stats['mem_quota']
            quotaDisk = stats['disk_quota']
            usageMemory = stats['usage']['mem'] * 1024
            usageDisk = stats['usage']['disk'] * 1024

            if point.id == 'quotaMemory':
                result.values.append((point, quotaMemory))
            elif point.id == 'quotaDisk':
                result.values.append((point, quotaDisk))
            elif point.id == 'usageCPU':
                result.values.append((point, stats['usage']['cpu']))
            elif point.id == 'utilMemory':
                utilMemory = (float(usageMemory) / quotaMemory) * 100.0
                result.values.append((point, utilMemory))
            elif point.id == 'utilDisk':
                utilDisk = (float(usageDisk) / quotaDisk) * 100.0
                result.values.append((point, utilDisk))

        return result

