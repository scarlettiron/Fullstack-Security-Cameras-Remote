from devices.models import device, local_server


def find_device_pk(data):
    devices = {}
    servers = {}

    if isinstance(data, list):
        for dict in data:
            if 'device' in dict:
                if dict['device'] not in devices:
                    unit_id = dict['device']
                    d = device.objects.get(unit_id = unit_id)
                    devices[unit_id] = d.pk
                    dict['device'] = d.pk
                dict['device'] = devices[unit_id]
            if 'server' in dict:
                if dict['server'] not in servers:
                    unit_id = dict['server']
                    s = local_server.objects.get(unit_id = unit_id)
                    servers[unit_id] = s.pk
                    dict['server'] = s.pk
                dict['server'] = servers[unit_id]
        
    else:
        if 'device' in data:
            d = device.objects.get(unit_id = data['unit_id'])
            data['device'] = d.pk
        if 'server' in data:
            s = local_server.objects.get(unit_id = data['unit_id'])
            data['server'] = s.pk

    return data