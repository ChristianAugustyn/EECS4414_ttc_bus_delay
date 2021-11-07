import partridge as ptg
inpath = '/Users/jerry/Developer/EECS4414_ttc_bus_delay/opendata_ttc_schedules.zip'
service_ids = ptg.read_busiest_date(inpath)[1]
view = {'trips.txt': {'service_id': service_ids}}

feed = ptg.load_geo_feed(inpath, view)

print(feed.shapes.head())
