# Simple REST API server to test Ansible Dynamic Inventory
# Adapted from:
#   https://stoplight.io/blog/python-rest-api/
#   https://flask-httpauth.readthedocs.io/en/latest/

# Dependencies:
#   pip install flask flask_httpauth
# Start service:
#   python restapi_server.py

from flask import Flask, json
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

my_host = 'localhost'
my_route = '/SolarWinds/InformationService/v3/Json/Query'
my_port = 17778
my_users = {
    "john": generate_password_hash("password"),
    "susan": generate_password_hash("password"),
    "guest": generate_password_hash("orion")
}

# SolarWinds - conform this REST API emulator with SolarWinds "Swagger" API results
# http://solarwinds.github.io/OrionSDK/swagger-ui/
my_inventory = {
    "results": [
        {"SysName": "server1.example.com", "DNS": "server1.example.com", "ip_address": "192.168.0.10", "MachineType": "Linux"},
        {"SysName": "server2.example.com", "DNS": "server2.example.com", "ip_address": "192.168.0.20", "MachineType": "Windows"},
    ]
}

app = Flask(__name__)
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    if username in my_users and \
            check_password_hash(my_users.get(username), password):
        return username

@app.route(my_route, methods=['GET'])
@auth.login_required
def get_companies():
  return json.dumps(my_inventory)

if __name__ == '__main__':
    # Start HTTPS rest api service
    app.run(host=my_host, port=my_port, debug=True, ssl_context='adhoc')