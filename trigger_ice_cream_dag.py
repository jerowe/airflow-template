import requests
import json
# Ensure the dag_to_trigger matches your DAG
dag_to_trigger = 'ice_cream_sundae'
uri = 'http://localhost:8080/api/experimental/dags/{}/dag_runs'.format(ice_cream_sundae)
conf = {'cone': 'chocolate_waffle','topping': 'strawberry sauce', 'ice_cream_flavor': 'cheesecake'}
data = {'conf': json.dumps(conf)}
res = requests.post(uri, json=data)
print(res.content)
print(res.status_code)