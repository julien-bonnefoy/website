import sys
from config import basedir
import site
import os

sys.path.insert(0, basedir)
site.addsitedir(os.path.join(basedir, 'venv/lib/python3.8/site-pacjages'))

from autoapp import app as aapplication
