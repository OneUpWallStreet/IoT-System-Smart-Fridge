from server.utils.dynamo_utils import *
import json
from server.utils.item_utils import *

#list items in dynmao

items = list_items_expiring_soon('XXXXXX')

print(json.dumps(items, indent=4))

print(get_expiration(item_obj=items[0]))
