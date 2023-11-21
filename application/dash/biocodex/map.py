




"""
load_dotenv(os.path.join(basedir, '.env'))
DATABASE_URL=os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://')
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    df = pd.read_sql('SELECT * FROM identities', con=conn)

with open("assets/pharmas_geojson.json", "r") as pharma_json:
    pharma_geojson = json.loads(pharma_json.read())

with open("assets/target_geojson.json", "r") as cible_json:
    target_geojson = json.loads(cible_json.read())

with open("assets/untarget_geojson.json", "r") as cible_json:
    untarget_geojson = json.loads(cible_json.read())

target_layer = dl.GeoJSON(
    data=target_geojson,
    hideout=dict(ugas_selected=[], spes_selected=[]),
    filter=ns('geojson_filter'),
    zoomToBounds=True,
    pointToLayer=ns('cible_icon'),
    id="target-geojson"
)

untarget_layer = dl.GeoJSON(
    data=untarget_geojson,
    hideout=dict(ugas_selected=[], spes_selected=[]),
    filter=ns('geojson_filter'),
    zoomToBounds=True,
    pointToLayer=ns('cible_icon'),
    id="untarget-geojson"
)
"""