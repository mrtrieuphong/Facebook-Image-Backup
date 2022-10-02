import json


def getCookie(json_dir):
    data = json.load(open(json_dir, 'r'))
    c_user, xs = "", ""
    for element in data['cookies']:
        if element['name'] == 'c_user':
            c_user = "{}".format(element['value'])
        if element['name'] == 'xs':
            xs = "{}".format(element['value'])
    return c_user, xs
