import requests
import json
import data.constants as c


def load_routes():
    """ Loads route ids and names for particular route types"""
    dict_rts_stps_dirs = {}
    msg = ""
    api_query = c.API_KEY + "routes"
    if len(c.ROUTE_TYPES) > 0:
        api_query = c.API_KEY + "routes?type=" + ",".join(map(str, c.ROUTE_TYPES))

    cnt = 0
    js = {}
    b_done = False
    while cnt < c.CNT_ATTEMPTS and not b_done:
        try:
            routes = requests.get(api_query)
            js = json.loads(routes.text)
            b_done = True
        except Exception as e:
            cnt += 1
            pass

    if not b_done:
        msg = f"Error loading JSON file {api_query}"
        return False, msg, dict_rts_stps_dirs

    for dic1 in js["data"]:
        id_1 = dic1['id']
        name = dic1['attributes']['long_name']
        directions = dic1['attributes']['direction_destinations']
        stops_api_query = c.API_KEY + "stops?route=" + id_1
        res = load_stops(stops_api_query, directions)
        if not res[0]:
            return False, res[1], dict_rts_stps_dirs
        lst_stop_names = res[2]
        lst_stop_ids = res[3]
        direction_index = res[4]
        d_temp = {'id': id_1,
                  'directions': directions,
                  'stop_names': lst_stop_names,
                  'stop_id': lst_stop_ids,
                  'stop_direction': direction_index}
        dict_rts_stps_dirs[name] = d_temp
    return True, msg, dict_rts_stps_dirs


def load_stops(api_query, directions):
    """ Loads route ids and names for particular route types
        Updates direction of stops per each route
    """
    msg = ""
    lst_stop_names = []
    lst_stop_ids = []
    direction_index = []
    cnt = 0
    js = {}
    b_done = False
    while cnt < c.CNT_ATTEMPTS and not b_done:
        try:
            stops = requests.get(api_query)
            js = json.loads(stops.text)
            b_done = True
        except Exception as e:
            cnt += 1
            pass

    if not b_done:
        msg = f"Could not load JSON file {api_query}"
        return False, msg, lst_stop_names, lst_stop_ids, direction_index

    i = 0
    for dict1 in js['data']:
        stop_name = dict1['attributes']['name']
        stop_id = dict1['id']
        if i == 0:
            i = 1
            res = find_index(stop_name, directions)
            if not res[0]:
                return False, res[1], lst_stop_names, lst_stop_ids, direction_index
            else:
                direction_index = res[2]
        lst_stop_names.append(stop_name)
        lst_stop_ids.append(stop_id)
    return True, msg, lst_stop_names, lst_stop_ids, direction_index


def find_index(stop_name, lst_destinations):
    """Finds direction of stops with respect to route directions"""
    msg = ""
    direction_index = []
    if stop_name in lst_destinations[0]:
        direction_index = [0, 1]
        return True, msg, direction_index
    elif stop_name in lst_destinations[1]:
        direction_index = [1, 0]
        return True, msg, direction_index
    else:
        msg = f"Could not find stop in destinations: {stop_name}, {lst_destinations}"
        return False, msg, direction_index
