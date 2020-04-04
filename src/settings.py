import json
from collections import defaultdict

try:
    with open('data/settings.json', 'r') as settings_file:
        settings = defaultdict(str, json.load(settings_file))
except FileNotFoundError:
    settings = defaultdict(str)
