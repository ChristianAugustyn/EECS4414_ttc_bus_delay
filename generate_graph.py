from gtfslite import GTFS
from datetime import date
import networkx as nx
from pyvis.network import Network

gtfs = GTFS.load_zip(
    '/Users/jerry/Developer/EECS4414_ttc_bus_delay/opendata_ttc_schedules.zip')
date = date.today()

trips = gtfs.trips
routes = gtfs.routes
stop_times = gtfs.stop_times
stops = gtfs.stops
trip_routes = trips.merge(routes, on="route_id", how="inner")
trip_routes_stop_times = trip_routes.merge(
    stop_times, on="trip_id", how="inner")
trip_routes_stop_times_stops = trip_routes_stop_times.merge(
    stops, on="stop_id", how="inner")
filtered_columns_sorted = trip_routes_stop_times_stops[[
    # FIRST ROW ATTRIBUTES ARE NECESSARY; OTHERS ARE OPTIONAL
    "route_id", "trip_id", "direction_id", "stop_id", "stop_sequence",
    "shape_dist_traveled", "trip_headsign", "route_type"
]]

only_bus_routes = filtered_columns_sorted[filtered_columns_sorted["route_type"] == 3]

self_join = only_bus_routes.merge(
    only_bus_routes, on=["route_id", "trip_id", "direction_id", "trip_headsign", "route_type"])
filtered_rows = self_join[self_join["stop_sequence_y"]
                          == self_join["stop_sequence_x"] + 1]
remove_trip_id = filtered_rows.drop(columns=["trip_id"])
remove_duplicates = remove_trip_id.drop_duplicates()
remove_duplicates.reset_index(drop=True, inplace=True)
final = remove_duplicates.sort_values(
    by=["route_id", "direction_id", "stop_sequence_x", "stop_sequence_y"])
final["shape_dist_traveled_x"] = final["shape_dist_traveled_x"].fillna(0)
final["distance"] = final.apply(
    lambda row: round(row["shape_dist_traveled_y"] - row["shape_dist_traveled_x"], 2), axis=1)
final["route_num"] = final.apply(
    lambda row: row["trip_headsign"].split()[2], axis=1)
pd_for_graph_generation = final.merge(routes, on="route_id", how="inner")
pd_for_graph_generation = pd_for_graph_generation[[
    "route_id", "direction_id", "stop_id_x", "stop_id_y",
    "distance", "trip_headsign", "route_short_name",
    "route_long_name", "route_type_x", "route_num"
]]
# pd_for_graph_generation = pd_for_graph_generation.astype({
#     "direction_id": int,
#     "distance": float,
#     "route_type": int,
# })

print(final)
final.to_csv("edge_list.csv", index="False")

# ----------- GRAPH GENERATION -----------

G = nx.from_pandas_edgelist(pd_for_graph_generation,
                            "stop_id_x", "stop_id_y", edge_attr=True, create_using=nx.MultiDiGraph())

# add node attributes
stop_node_attr = stops[[
    "stop_id", "stop_code", "stop_name", "stop_lat", "stop_lon"
]]
stop_node_attr.set_index("stop_id", inplace=True)
stops_dict = stop_node_attr.to_dict("index")
nx.set_node_attributes(G, stops_dict)

nx.write_gpickle(G, "transit_graph.gpickle")

# net = Network(notebook=True)
# net.from_nx(G)
# net.show("graph.html")
