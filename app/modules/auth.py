import sys
import json
import requests


def authenticate(username, apikey, region):
    """Authenticates user using apikey"""
    region = region.upper()
    user_data = {}
    url = 'https://identity.api.rackspacecloud.com/v2.0/tokens'
    #print 'Initializing token for {}....'.format(username),
    try:
        jsonreq = {
            'auth': {'RAX-KSKEY:apiKeyCredentials': {'username': username,
                                                     'apiKey': apikey}}}
        auth_headers = {'content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(jsonreq), headers=auth_headers)
        if r.status_code == 401:
            user_data["msg"] = "Apikey did not work for {}!".format(username)
            return user_data
        if r.status_code == 200:
            jsonresp = json.loads(r.text)
            tenant = str(jsonresp['access']['token']['tenant']['id'])
            token = str(jsonresp['access']['token']['id'])
            user_data, endpoint = get_link(jsonresp, username, region, user_data) 
            user_data["tenant"] = tenant
            user_data["token"] = token
            user_data["endpoint"] = endpoint
            #if not user_data.get("msg", None):
             #   user_data["msg"] = ("Success in authentication!"
              #                      " Performing final step...")
    except requests.exceptions.ConnectionError:
        if hasatrr(r, "status_code"):
            user_data["msg"] = "Connection Error! Http status Code {}".format(r.status_code)
        else:
            user_data["msg"] = "Connection Error! Http status Code Unkown"
    except requests.exceptions.RequestException:
        if hasatrr(r, "status_code"):
            user_data["msg"] = "Ambiguous Error! Http status Code {}".format(r.status_code)
        else:
            user_data["msg"] = "Ambiguous Error! Http status Code Unkown"

    return user_data

def get_link(jsonresp, username, region, user_data):
    """Gets the endpoints for Cloud files depending on region"""
    foo = jsonresp["access"]["serviceCatalog"]
    index_save = None
    for i in foo:
        if i["name"] == "cloudImages":
            for index, value in enumerate(i["endpoints"]): 
                if str(value["region"]) == region:
                    bar = i
                    index_save = index
    try:
        region = str(bar["endpoints"][index_save]["publicURL"])
    except NameError:
        user_data["msg"] = "\nThere's no image endpoint for {}!".format(username)
        return user_data, None
    region = region + "/images"
    return user_data, region

