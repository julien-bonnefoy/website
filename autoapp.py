# -*- coding: utf-8 -*-
"""Create an application instance."""
from app import create_app
from config import DevConfig

conf = DevConfig()
app = create_app(conf)
