__author__ = 'Spencer Thomas'

import csv
import re

class Route():

    REPLACEMENTS = (
        ('Line', ''),
        ('IB', ' Inbound'),
        ('WB', ' Westbound'),
        ('SB', ' Southbound')
    )

    def __init__(self, array):
        self.headsigns = []
        self.number_trips = 0
        self.route_id = array[0]
        self.agency_id = array[1]
        self.route_short_name = array[2].replace('Line', '') # "B Line" -> "B"
        self.route_long_name = array[3]
        self.route_desc = array[4]
        self.route_type = array[5]
        try: # not important
            self.route_url = array[6]
            self.route_color = array[7]
            self.route_text_color = array[8]
        except:
            pass
        self.headsigns = set()
        self.number_trips = 0

    def add_trip(self, trip):
        for headsign in trip.trip_headsign.split(','):
            self.headsigns.add(re.sub("[^A-z\s]", "", headsign).strip().lstrip())

        self.number_trips += 1

    def __str__(self):
        return "route=" + self.route_short_name + ", numtrips=" + str(self.number_trips) + ", headsign=" \
               + str(self.headsigns)


class Trip():

    def __init__(self, array):
        self.route_id = array[0]
        self.service_id = array[1]
        self.trip_id = array[2]
        self.trip_headsign = array[3]
        self.trip_short_name = array[4]
        self.direction_id = array[5]
        try: # not important
            self.block_id = array[6]
            self.shape_id = array[7]
        except:
            pass


class TransitAgency():

    __route_numbers = {}

    def __init__(self, directory):
        self.directory = directory
        self.routes_filename = directory + "/routes.txt"
        self.trips_filename = directory + "/trips.txt"
        routes = self.__get_routes(self.routes_filename)
        trips = self.__get_trips(self.trips_filename)
        self.__add_headsigns_to_routes(routes, trips)
        self.__create_route_lookup(routes)

    def get_routes(self):
        """
        :rtype: list of Route
        """
        return self.__route_numbers.values()

    def __get_routes(self, csv_file):
        routes = []
        with open(csv_file, 'rU') as lines:
            csv_lines = csv.reader(lines)
            for csv_line in csv_lines:
                route = Route(csv_line)
                routes.append(route)
        return routes

    def __get_trips(self, csv_file):
        trips = []
        with open(csv_file, 'rU') as lines:
            csv_lines = csv.reader(lines)
            for csv_line in csv_lines:
                trip = Trip(csv_line)
                trips.append(trip)
        return trips

    def __create_route_lookup(self, routes):
        for route in routes:
            self.__route_numbers[route.route_short_name] = route

    def __add_headsigns_to_routes(self, routes, trips):
        route_id_to_route = {}
        for route in routes:
            route_id_to_route[route.route_id] = route

        for trip in trips:
            route_id_to_route[trip.route_id].add_trip(trip)
