from data.dataform import populate_routes, populate_directions, populate_stops, \
    extract_departure_time, init_dict_routes


def run():
    """Add the code here to connect forms with data"""
    pass


def load_data():
    """Loads route names on initial page load

    Returns tuple with 3 elements:
        1st - Success | Failure
        2nd - Error Message (if failure above)
        3rd - Route Names to be loaded on form
    """
    msg = ""
    route_names = []
    res = init_dict_routes()
    if not res[0]:
        return False, res[1], route_names
    route_names = populate_routes()
    return True, msg, route_names


def show_stops(route_name):
    """Loads stops for selected route

    Returns tuple with 3 elements:
        1st - Success | Failure
        2nd - Error Message (if failure)
        3rd - List of Stops (empty if failure)
    """
    return populate_stops(route_name)


def show_directions(route_name, stop_name):
    """Loads available directions for select route and stop

        - Checks direction of stops
        - Checks if stop is end stop

    Returns tuple with 3 elements
        1st - Success | Failure
        2nd - Error Message (if failure)
        3rd - List of available directions
    """
    return populate_directions(route_name, stop_name)


def show_departure_time(route_name, stop_name, direction_name):
    """Returns predictive departure time for route, stop, and selected direction

    Returns tuple with 3 elements
        1st - Success | Failure
        2nd - Error Message (if failure)
        3rd - Value of Predicted Departure Time (empty string if error)
    """
    return extract_departure_time(route_name, stop_name, direction_name)


if __name__ == "__main__":
    """Example how to run the code"""
    res1 = load_data()
    if res1[0]:
        print(f"Available Routes {res1[2]}")
        res2 = show_stops('Red Line')
        if res2[0]:
            print(f"Available Stops {res2[2]}")
            res3 = show_directions('Red Line', 'Ashmont')
            if res3[0]:
                print(f"Available Directions {res3[2]}")
                res4 = extract_departure_time('Red Line', 'Ashmont', 'Alewife')
                print(res4[2])
