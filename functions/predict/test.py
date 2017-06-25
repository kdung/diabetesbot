# -*- coding: utf-8 -*-

import main
import json

with open('event.json') as f:
    event = json.load(f)
    print(main.handle(event, None))