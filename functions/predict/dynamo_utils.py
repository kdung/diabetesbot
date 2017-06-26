# -*- coding: utf-8 -*-

def convert_json_to_dynamo(json_obj):
    result = dict()
    for k in json_obj:
        v = json_obj[k]
        result[k] = build_dynamo_json(v)
    return result

def build_dynamo_json(value):
    if isinstance(value, str):
        return {'S': value}
    if isinstance(value, bool):
        return {'B': value}
    if isinstance(value, (int, float)):
        return {'N': str(value)}
    if isinstance(value, dict):
        return {'M': convert_json_to_dynamo(value)}
    return {'NULL': True}

if __name__ == '__main__':
    print(convert_json_to_dynamo({
        'uuid': '1234',
        'slots': {
            'A':'a',
            'B':1,
            'C': True
        },
        'result': 1
    }))