from functools import wraps
import json
from operator import itemgetter
from .do_request import do_request, do_raw_request


def mutate_url_servers_endpoint(producer_data):
    return (producer_data['tenant'], 
            producer_data['token'],
            producer_data['endpoint'].replace(".images",
                ".servers"))


def images_custom_list(args, producer_data):
    tenant, token, url = mutate_url_servers_endpoint(producer_data)

    url = url + '/' + 'detail'
    r = do_raw_request(url, token)
    if r.status_code == 200:
        output = r.json()["images"]
        custom_images_list = [custom_images for custom_images in output
                              if custom_images["metadata"].get('user_id', None)]
        temp_image_list = []
        for image in custom_images_list:
            image_temp = ({"status": image["status"],
                           "links": image["links"][0]["href"],
                           "id": image["id"], "name": image["name"]})
            temp_image_list.append(image_temp)
        if len(temp_image_list):
            return json.dumps(
                    { "custom-images": temp_image_list }, indent=2)
    elif r.status_code:
        message = "Error! Http status code {}".format(r.status_code)
             

def image_list_detail(args, producer_data):
    tenant, token, url = mutate_url_servers_endpoint(producer_data)

    uuid = args['uuid']
    url = url + "/" + uuid
    r = do_raw_request(url, token)
    if r.status_code == 200:
        return json.dumps(
                { "image-detail": r.json() }, indent=2)
    elif r.status_code:
        message = "Error! Http status code {}".format(r.status_code)
    return json.dumps({ "message" : message })



def member_add(args, producer_data,
               remove=False, consumer_tenant=None,
               manual=True):
    # if called from command line instead of image_share()
    #if producer_data.get('consumer_tenantid', None):
    consumer_tenant = args['consumer_tenantid']

    producer_tenant, producer_token, producer_url = itemgetter('tenant',
            'token', 'endpoint')(producer_data)

    uuid = args['uuid']
    url = producer_url + "/" + uuid + "/members"
    json_data = {"member": consumer_tenant}

    if remove:
        print("\nAttempting to remove consumer {}"
              " as member to image {}...".format(consumer_tenant, uuid))
        url = url + "/" + consumer_tenant
        # remove/delete API does not return body
        # so do raw request
        r = do_raw_request(url, producer_token, mode="delete")
        if r.status_code == 204:
            # Delete API does not return anything
            message = "Success"
        elif r.status_code == 404:
            message = ("User {} doesn't exist"
                  " as a member").format(consumer_tenant)
    else:
        print("\nAttempting to add consumer {}"
              " as member to image {}...".format(consumer_tenant, uuid))
        body, status_code = do_request(
            url, producer_token, json_data, mode="post")
        if status_code == 409:
             message = "Member already exists!"
        else:
            message = "Error! Http status code: "+ str(status_code)

    if manual:
        return json.dumps({ "message" : message })
    else:
        return status_code

def image_share(args, producer_data, consumer_data):
    producer_tenant, producer_token, producer_url = itemgetter('tenant',
            'token', 'endpoint')(producer_data)
    consumer_tenant, consumer_token, consumer_url = itemgetter('tenant',
            'token', 'endpoint')(consumer_data)

    status_code = member_add(args, producer_data,
               consumer_tenant=consumer_tenant,
               manual=False)
    args['member_status'] = 'accepted'
    if status_code == 200 or status_code == 409:
        status_code = status_set(args, consumer_data,
                manual=False)
    if status_code == 200:
        message = "Success!"
    else:
        message = "Error! Http status code {}".format(r.status_code)
    return json.dumps({ "message" : message })

def raw_list(function):
    @wraps(function)
    def wrapper(args, producer_data):
        original_function = function(args, producer_data)
        tenant, token, url = itemgetter('tenant',
                'token', 'endpoint')(producer_data)
        print url
        r = do_raw_request(url, token)
        if r.status_code == 200:
            return json.dumps(
                    { "list-all-images": r.json() }, indent=2)
        elif r.status_code:
            message = "Error! Http status code {}".format(r.status_code)
        return json.dumps({ "message" : message })
        return original_function
    return wrapper

@raw_list
def member_list(args, producer_data):
    # in argparse, consumer or producer data can be used because
    # consumer is aliased to producer.
    uuid = args['uuid']
    producer_data[2] = producer_data[2] + "/" + uuid + "/members"

@raw_list
def list_all_images(args, producer_data):
    pass
    #url = producer_data['endpoint']
    #url_query = {}
    #for key, value in args.iteritems():
     #   if key == 'visibility' or key == 'owner'\
      #          or key == 'member_status':
       #             if value is not None:
        #                url_query[key] = value
    #if len(url_query) > 0:
     #   url = url + "?"
      #  for key, value in url_query.iteritems():
       #     url = url + key + '=' + value[0] + "&"
    #producer_data['endpoint'] = url.rstrip("&")
    #todo error correction
 
def status_set(args, consumer_data,
        region=None, manual=True):
    consumer_tenant, consumer_token, consumer_url = itemgetter('tenant',
            'token', 'endpoint')(consumer_data)
    uuid = args['uuid']
    url = consumer_url + "/" + uuid + "/members/" + consumer_tenant
    status = args['member_status']
    json_data = {"status": status}
    status_code = "Unknown"

    print ("\nAttempting to set status to "
           "{} for member {}...".format(status, consumer_tenant))
    body, status_code = do_request(url, consumer_token, json_data, mode="put")

    if status_code == 404:
        message = ("Error....Http Code 404 returned."
                   " Hint: Make sure {} is the consumer"
                   " and the image is originally"
                   " from {} ".format(consumer_tenant,
                       region))
    elif status_code == 200:
        message = ("Success! Status is now"
                   " set to {}.".format(status))
    else:
        message = ("Oh no! Http Error"
                   " Code {}".format(r.status_code))
    if manual:
        return json.dumps({ "message" : message })
    else:
        return status_code
    
