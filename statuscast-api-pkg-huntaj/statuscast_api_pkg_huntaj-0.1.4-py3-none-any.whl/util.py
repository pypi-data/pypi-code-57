import json
# Method for hitting an API endpoint and printing the output 
# Returns: - 
def hit_endpoint(endpoint,method,data=None):
    if method.lower() == "get": 
        requests.
    elif method.lower() == "post":
        if data is None:
            print("Cannot POST nothing to endpoint {}".format(endpoint))
            sys.exit(1)
        else: 
            data = json.dumps(data)
            r = requests.post(endpoint,data)
            print(r.content)
            sys.exit(0)