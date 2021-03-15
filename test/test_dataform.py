import unittest
from data.dataform import populate_directions, populate_stops, \
    extract_departure_time, init_dict_routes, populate_routes
from datetime import datetime


class TestPopulateRoutes(unittest.TestCase):
    def setUp(self):
        res1 = init_dict_routes()
        if not res1[0]:
            return False, res1[1]
        self.route_names = []
        res1 = populate_routes()
        self.route_names = res1

    def test_populate_routes(self):
        routes = ['Red Line', 'Mattapan Trolley', 'Orange Line', 'Green Line B',
                  'Green Line C', 'Green Line D', 'Green Line E', 'Blue Line']
        self.assertEqual(self.route_names, routes)


class TestPopulateStops(unittest.TestCase):
    def setUp(self):
        init_dict_routes()

    def test_populate_stops(self):
        route_name = 'Red Line'
        res = populate_stops(route_name)
        self.assertEqual(len(res[2]), 22)
        stops = ['Alewife', 'Davis', 'Porter', 'Harvard', 'Central',
                 'Kendall/MIT', 'Charles/MGH', 'Park Street', 'Downtown Crossing',
                 'South Station', 'Broadway', 'Andrew', 'JFK/UMass',
                 'Savin Hill', 'Fields Corner', 'Shawmut', 'Ashmont',
                 'North Quincy', 'Wollaston', 'Quincy Center', 'Quincy Adams', 'Braintree']
        self.assertEqual(res[2], stops)

        # bad route
        route_name = 'aaaa'
        res = populate_stops(route_name)
        self.assertEqual(len(res[2]), 0)
        self.assertEqual(res[2], [])


class TestPopulateDirections(unittest.TestCase):
    def setUp(self):
        init_dict_routes()

    def test_populate_directions(self):
        # regular stop
        route_name = 'Red Line'
        stop_name = 'Harvard'
        res = populate_directions(route_name, stop_name)
        self.assertEqual(res[2], ['Ashmont/Braintree', 'Alewife'])

        # wrong stop and/or route
        route_name = 'Red Line'
        stop_name = 'Forest Hills'
        res = populate_directions(route_name, stop_name)
        self.assertEqual(res[2], [])

        # end stop
        route_name = 'Red Line'
        stop_name = 'Ashmont'
        res = populate_directions(route_name, stop_name)
        self.assertEqual(res[2], ['Alewife'])

        # other end stop
        route_name = 'Red Line'
        stop_name = 'Alewife'
        res = populate_directions(route_name, stop_name)
        self.assertEqual(res[2], ['Ashmont/Braintree'])


class TestExtractDepartureTime(unittest.TestCase):
    def setUp(self):
        init_dict_routes()

    def test_extract_departure_time(self):
        # checks of predicted departure time is greater
        # than current time
        route_name = 'Red Line'
        stop_name = 'Alewife'
        direction_name = 'Ashmont/Braintree'
        now = datetime.now()
        ret = extract_departure_time(route_name, stop_name, direction_name)
        self.assertGreaterEqual(ret[2], now.strftime("%Y-%m-%dT%H:%M:%S"))

        # bad data in direction (or any other input)
        route_name = 'Red Line'
        stop_name = 'Alewife'
        direction_name = 'aaaaa'
        ret = extract_departure_time(route_name, stop_name, direction_name)
        self.assertEqual(ret[2], "")


if __name__ == "__main__":
    unittest.main()
