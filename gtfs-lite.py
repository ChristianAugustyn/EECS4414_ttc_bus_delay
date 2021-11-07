from gtfslite import GTFS
from datetime import date
gtfs = GTFS.load_zip(
    '/Users/jerry/Developer/EECS4414_ttc_bus_delay/opendata_ttc_schedules.zip')
date = date.today()

trips = gtfs.trips
routes = gtfs.routes
stop_times = gtfs.stop_times
stops = gtfs.stops
# print(trips)
# print(routes)
# print(trips['route_id'].dtypes)
# print(routes['route_id'].dtypes)
# trips['route_id'] = trips['route_id'].astype(int)
# routes['route_id'] = routes['route_id'].astype(int)
# print(trips['route_id'].dtypes)
# print(routes['route_id'].dtypes)
# print(trips.join(routes, on="route_id", how="inner",
#                  lsuffix='_left', rsuffix='_right'))

trip_routes = trips.merge(routes, on="route_id", how="inner")
trip_routes_stop_times = trip_routes.merge(
    stop_times, on="trip_id", how="inner")
trip_routes_stop_times_stops = trip_routes_stop_times.merge(
    stops, on="stop_id", how="inner")
# trip_routes_stop_times_stops.to_csv("test.csv", index="False")
# print(trip_routes_stop_times_stops)
filtered = trip_routes_stop_times_stops[[
    "route_id", "trip_id", "direction_id", "stop_id", "stop_sequence"]].sort_values(by=["route_id", "trip_id", "direction_id", "stop_sequence"])
self_joined=filtered.merge(filtered, on=["route_id","trip_id", "direction_id"])
filter2 = self_joined[self_joined["stop_sequence_y"] == self_joined["stop_sequence_x"] + 1]
print(filter2)
