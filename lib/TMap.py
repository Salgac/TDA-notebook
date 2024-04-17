import folium
import ast
import io
from PIL import Image
from datetime import datetime
from folium.plugins import HeatMap
from folium.plugins import MarkerCluster


class TMap:

    def __init__(self, location, zoom):
        self.m = folium.Map(
            prefer_canvas=True,
            height=750,
            width=1000,
            location=location,
            zoom_start=zoom,
        )
        self.n = 0

    def save(self, center):
        # set the zoom to the maximum possible
        if center:
            self.m.fit_bounds(self.m.get_bounds())

        # layer control
        # todo folium.LayerControl().add_to(self.m)

        self.m.save("map.html")

    def save_png(self):
        img_data = self.m._to_png(5)
        img = Image.open(io.BytesIO(img_data))
        img.save(f"data/img/map_{datetime.now().strftime('%Y%m%d-%H%M%S')}.png")

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

    def add_events(self, events):
        # Create a MarkerCluster for events
        event_cluster = MarkerCluster()
        for event in events:
            popup_content = event.get_popup()
            event_cluster.add_child(
                folium.Marker(
                    location=(event.points[-1][0], event.points[-1][1]),
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

    def add_filter_zones(self, zones):
        for z in zones:
            # Add a circle representing the filtered-out area
            folium.Circle(
                location=ast.literal_eval(z["coords"]),
                radius=z["distance"],
                color="transparent",
                fill=True,
                fill_color="red",
                fill_opacity=0.2,
            ).add_to(self.m)
