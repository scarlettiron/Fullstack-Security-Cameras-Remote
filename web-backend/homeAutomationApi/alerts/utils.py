from devices.models import device


def find_device_pk(data):
    devices = {}

    if isinstance(data, list):
        for dict in data:
            unit_id = dict['unit_id']
            if unit_id not in devices:
                d = device.objects.get(unit_id = unit_id)
                devices[unit_id] = d.pk
                dict['device'] = d.pk
            dict['device'] = devices[unit_id]
        
    else:
        d = device.objects.get(unit_id = data['unit_id'])
        data['device'] = d.pk

    return data
                
                
                