import requests
import json
from app.api import get_topology
from flask import Flask, render_template, redirect, url_for, current_app
from . import topology


@topology.route('/')
def index():
    topo = json.dumps(get_topology())
    return render_template('topology.html', topo_json=topo)
