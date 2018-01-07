# Install
```pip install historio```

# Build Protoc (optional)
```
# We already have it in historio/definition
python -m grpc_tools.protoc -I=. --grpc_python_out=../ api.proto --python_out=../
```

# Run Service by Docker
```
docker-compose up -d
```
# Run Service by command line
```
# For sure you have installed
python -m historio
```
# Test
```py.test --cov historio --cov-report=html  tests/ --cov-fail-under=100```


# Configuration
```python
client.historio(server='grpc_address', port=5505, soft_handler=True)
```
* server(str): refers to historio Server
* port(int): PORT
* soft_handler(bool): Default `True`. if it's `False`,  client will raise error in case something goes wrong
# Usage
+ **You can return any particular class for decorator(NOT RECOMMEND)**
```python
from historio import client

#Inject client.historio as decorator on target function which must return a dictionary

@client.historio(source='assignment', source_id='source_id', user_id='id_of_user_who_change')
def function_will_save_my_model_and_return_updated():
    model = DynamoDBModel()
    """
    Whatever you do, just return it and decorator will do the rest
    """
    return model

```
+ **Your model can be any class or dictionary(NOT RECOMMEND)**
```python
from historio import client

client.historio(server='grpc_address', port=5505)

def somewhere_else_in_your_application():
    user = get_current_user() #Get current user
    assignment = DynamoDBModel() #your source model
    #time to push
    client.historio().push(source='assignment', source_id=assignment.id, user_id=user.id, data=model)
```

+ **In case your model implement historio.Model, your code would be easier(RECOMMEND)**

```python
from historio import Model, client
class YourDynamoDBModel(Model):
    def __init__(self, id):
        self.id = id

    def source(self):
        return 'assignment'

    def get_data(self):
        return {'name': 'Paul', 'age': 32}

    def source_id(self):
        return self.id

    def user_id(self):
        return 'paulaan_id'

#In your controller
def your_controller_action():
    data = YourDynamoDBModel() #from somewhere else
    client.historio().push(data)
```
