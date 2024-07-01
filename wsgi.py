import sys
import site
import os

basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, basedir)
site.addsitedir(os.path.join(basedir, 'venv/lib/python3.8/site-packages'))

from autoapp import app as application