import sys
from autoapp import app
from config import basedir

sys.path.insert(0, basedir)
application = app
