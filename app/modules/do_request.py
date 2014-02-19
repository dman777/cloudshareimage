import sys
import json
import requests


def do_raw_request(url, token, json_data=None,
                   mode="get"):
    """Uploads a file. """
    header_collection = {"X-Auth-Token": token}
    if json_data is not None:
        header_collection['Content-Type'] = 'application/json'
    try:
        if mode == "delete":
            # this looks ugly, but there is absolutely no way to
            # get requests to do DELETE when there is a blank JSON
            # included
            r = requests.delete(url, headers=header_collection, timeout=10)
        else:
            r = getattr(requests, mode)(url, data=json.dumps(json_data),
                                        headers=header_collection, timeout=10)
        #todo return  this in calling function instead
        if r.status_code == 200:
            return r
        else:
            print "HTTP code: " + str(r.status_code)
            return r

    except requests.exceptions.ConnectionError:
        print "Connection Error! Http status Code {}"
    except (requests.exceptions.RequestException,
            requests.exceptions.HTTPError):
        print "Ambiguous Error! Http status Code {}"


def do_request(url, token, json_data=None,
               mode="get"):
    r = do_raw_request(url, token, json_data, mode)
    try:
        return (json.dumps(r.json(),
                           indent=2), r.status_code)
    except ValueError:
        return r.text, r.status_code
