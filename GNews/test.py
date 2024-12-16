p = None
print(f"p={p}")


str = '''
{
    "isRelated": false,
    "isNational": true,
    "city": null,
    "state": null,
    "location": []
}
'''

import json

j = json.loads(str)

print(j)