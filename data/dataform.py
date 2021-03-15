import requests
import json
from data.datamodel import load_routes
import data.constants as c

# global variable
dict_routes_stops_directions = {}


def init_dict_routes():
    """Initializes data dictionary for routes, stops, and directions"""
    global dict_routes_stops_directions
    msg = ""
    if dict_routes_stops_directions == {}:
        res = load_routes()
        if not res[0]:
            return False, res[1]
        else:
            dict_routes_stops_directions = res[2]
    return True, msg


def populate_routes():
    """Data for Routes drop-down options"""
    route_names = []
    for name in dict_routes_stops_directions.keys():
        route_names.append(name)
    return route_names


def populate_stops(route_name):
    """Data for Stops drop-down options"""
    msg = ""
    if route_name not in dict_routes_stops_directions.keys():
        msg = "Invalid route name"
        return False, msg, []
    return True, msg, dict_routes_stops_directions[route_name]['stop_names']


def populate_directions(route_name, stop_name):
    """ Populates available directions for route and stop
        Special case for end stops - these should offer only one direction
    """
    ind = 0
    msg = ""
    try:
        ind = dict_routes_stops_directions[route_name]['stop_names'].index(stop_name)
    except:
        msg = "Invalid route name or stop " + route_name + " " + stop_name
        return False, msg, []

    if ind == 0:
        direct_indexes = dict_routes_stops_directions[route_name]['stop_direction']
        ind1 = direct_indexes.index(1)
        return True, msg, [dict_routes_stops_directions[route_name]['directions'][ind1]]
    elif ind == len(dict_routes_stops_directions[route_name]['stop_names']) - 1 or \
            is_name_in_directions(route_name, stop_name):
        direct_indexes = dict_routes_stops_directions[route_name]['stop_direction']
        ind1 = direct_indexes.index(0)
        return True, msg, [dict_routes_stops_directions[route_name]['directions'][ind1]]
    else:
        return True, msg, dict_routes_stops_directions[route_name]['directions']


def is_name_in_directions(route_name, stop_name):
    for el in dict_routes_stops_directions[route_name]['directions']:
        if stop_name in el:
            return True
    return False


def extract_departure_time(route_name, stop_name, direction_name):
    """Extracts Predicted Departure Time

    Tries several iterations (up to 100) to get departure time
    """

    msg = ""
    try:
        route_id = dict_routes_stops_directions[route_name]['id']
        ind1 = dict_routes_stops_directions[route_name]['stop_names'].index(stop_name)
        stop_id = dict_routes_stops_directions[route_name]['stop_id'][ind1]
        direction_id = dict_routes_stops_directions[route_name]['directions'].index(direction_name)
    except:
        msg = "Invalid route name, stop name, or direction: " + \
              route_name + ", " + stop_name + ", " + direction_name
        return False, msg, ""

    api_query = c.API_KEY + "predictions?" + "route=" + route_id + "&stop=" \
                + stop_id + "&direction_id=" + str(direction_id)

    cnt = 0
    while cnt < c.CNT_ATTEMPTS:
        try:
            schedules = requests.get(api_query)
            js = json.loads(schedules.text)
            return True, msg, str(js['data'][0]['attributes']['departure_time'])
        except:
            cnt += 1
            pass

    msg = "Could not retrieve predicted departure time"
    return False, msg, ""
