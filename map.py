from wsgiref.simple_server import WSGIServer

import dash
import dash_auth
import pandas as pd
import plotly.express as px
import plotly.offline as pyo
import plotly.graph_objs as go


USERNAME_PASSWORD_PAIRS = [
    ['NatalieAndrade', '001'], ['username', 'password']
]


app = dash.Dash()
auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)
server = app.server

cov_data = pd.read_csv("data.csv")
print(cov_data)


fig = px.scatter_mapbox(cov_data, lat="Lat", lon="Long_", hover_name="Country_Region", hover_data=["Confirmed"],
                        color_discrete_sequence=["fuchsia"], zoom=3, height=300)

fig.update_layout(
    mapbox_style="white-bg",
    mapbox_layers=[
        {
            "below": 'traces',
            "sourcetype": "raster",
            "source": [
                "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
            ],

        }
    ],
)
fig.update_layout(height=1400, margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.show()

if __name__ == '__main__':
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
