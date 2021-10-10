import os
from mgz import header, body, model
import json

with open("replay1.aoe2record", "rb") as data:
    match = model.parse_match(data)
    print(json.dumps(model.serialize(match), indent=2))

# with open("replay1.aoe2record", "rb") as data: