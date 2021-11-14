from flask import Flask


app = Flask(__name__, instance_relative_config=True)
app.config.from_object("config.Config")
with app.app_context():
    from . import routes
    from .dash_apps import demo, iris_kmeans, crossfilter_example

    app = demo.init_dash(app)
    app = iris_kmeans.init_dash(app)
    app = crossfilter_example.init_dash(app)

