import folium
from folium.plugins import HeatMap
from folium.plugins import MarkerCluster


class TMap:
    def __init__(self):
        self.m = folium.Map(prefer_canvas=True)
        self.n = 0

    def save(self):
        # set the zoom to the maximum possible
        self.m.fit_bounds(self.m.get_bounds())

        # layer control
        # todo folium.LayerControl().add_to(self.m)

        self.m.save("map.html")

    ####################
    # adders
    def add_data(self, data):
        locations = []
        popups = []
        n = 0

        # extract data into arrays
        for d in data:
            locations += d.get_lat_lons()
            popups += d.get_popups()
            n += len(d.rows_filtered)

        # plot data
        HeatMap(locations, name="HeatMap").add_to(self.m)
        MarkerCluster(locations, popups, name="Cluster").add_to(self.m)

        self.n = n

    def add_events(self, events, T_Depo):
        # Create a MarkerCluster for events
        event_cluster = MarkerCluster()
        for event in events:
            popup_content = f"Start: {event.start_time.strftime('%H:%M:%S')}, End: {event.end_time.strftime('%H:%M:%S')}"
            event_cluster.add_child(
                folium.Marker(
                    location=(event.points[0][0], event.points[0][1]),
                    popup=popup_content,
                )
            )
        self.m.add_child(event_cluster)

        self.n = len(events)

        # Extract latitude and longitude for heatmap
        heatmap_data = [
            [point[0], point[1]] for event in events for point in event.points
        ]
        HeatMap(heatmap_data).add_to(self.m)

        # Add a circle representing the filtered-out area
        folium.Circle(
            location=T_Depo["c"],
            radius=T_Depo["d"],
            color="transparent",
            fill=True,
            fill_color="red",
            fill_opacity=0.2,
        ).add_to(self.m)
