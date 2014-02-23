from app import app
import json
from flask.views import MethodView

from flask import request
from flask import url_for

from modules.auth import authenticate
from modules.actions import member_list, member_add, image_list_detail, list_all_images, images_custom_list, image_share, status_set

@app.route('/')
def index():
        return app.send_static_file('index.html')


class Authentication(object):
    def __init__(self, request):
        form_data = request.form
        #print form_data;
        self.producer_data = {}
        self.consumer_data = {}
        self.args = {}
        if form_data.get('producer_apikey', None):
            self.producer_data = authenticate(
                form_data['producer_username'], form_data['producer_apikey'], form_data['region'])
        if form_data.get('consumer_apikey', None):
            self.consumer_data = authenticate(
                form_data['consumer_username'], form_data['consumer_apikey'], form_data['region'])
        if form_data.get('region', None):
            self.region = form_data['region']
        if form_data.get('consumer_tenantid', None):
            self.args['consumer_tenantid'] = form_data['consumer_tenantid']
        if form_data.get('image_uuid', None):
            self.args["uuid"] = form_data['image_uuid']
        if form_data.get('member_status', None):
            self.args['member_status'] = form_data['member_status']

    def check_auth(self):
        if self.producer_data.get("msg", None):
            return json.dumps(
                    { "message" : self.producer_data["msg"] })
        if self.consumer_data.get("msg", None):
            return json.dumps(
                    { "message" : self.consumer_data["msg"] })

     

class ImageShareForm(MethodView, Authentication):
    def __init__(self):
        Authentication.__init__(self, request)

    def get(self):
        pass
    
    def post(self):
        response = self.check_auth()
        if response:
            return response
        response = image_share(self.args, self.producer_data, 
                        self.consumer_data)
        if response:
             return response
app.add_url_rule('/imageshareform', view_func=ImageShareForm.as_view('imageshareform'))

class SetStatusForm(MethodView, Authentication):
    def __init__(self):
        Authentication.__init__(self, request)

    def get(self):
        pass
    
    def post(self):
        response = self.check_auth()
        if response:
            return response
        response = status_set(self.args,
                self.consumer_data,
                self.region)
        if response:
             return response
app.add_url_rule('/setstatusform', view_func=SetStatusForm.as_view('setstatusform'))

class ListCustomImagesForm(MethodView, Authentication):
    def __init__(self):
        Authentication.__init__(self, request)

    def get(self):
        pass
    
    def post(self):
        response = self.check_auth()
        if response:
            return response
        response = images_custom_list(self.args,
                self.producer_data)
        if response:
            return response
app.add_url_rule('/listcustomimagesform', view_func=ListCustomImagesForm.as_view('listcustomimagesform'))

class ListAllImagesForm(MethodView, Authentication):
    def __init__(self):
        Authentication.__init__(self, request)

    def get(self):
        pass
    
    def post(self):
        response = self.check_auth()
        if response:
            return response
        response = list_all_images(self.args,
                self.producer_data)
        if response:
            return response
app.add_url_rule('/listallimagesform', view_func=ListAllImagesForm.as_view('listallimagesform'))

class ImageDetailForm(MethodView, Authentication):
    def __init__(self):
        Authentication.__init__(self, request)

    def get(self):
        pass
    
    def post(self):
        response = self.check_auth()
        if response:
            return response
        response = image_list_detail(self.args,
                self.producer_data)
        if response:
            return response
app.add_url_rule('/imagedetailform', view_func=ImageDetailForm.as_view('imagedetailform'))

class AddMemberForm(MethodView, Authentication):
    def __init__(self):
        Authentication.__init__(self, request)

    def get(self):
        pass
    
    def post(self):
        response = self.check_auth()
        if response:
            return response
        response = member_add(self.args,
                self.producer_data)
        if response:
            return response
app.add_url_rule('/addmemberform', view_func=AddMemberForm.as_view('addmemberform'))


class RemoveMemberForm(MethodView, Authentication):
    def __init__(self):
        Authentication.__init__(self, request)

    def get(self):
        pass
    
    def post(self):
        response = self.check_auth()
        if response:
            return response
        response = member_add(self.args,
                self.producer_data, 
                remove=True)
        if response:
            return response
app.add_url_rule('/removememberform', view_func=RemoveMemberForm.as_view('removememberform'))

class MemberListForm(MethodView, Authentication):
    def __init__(self):
        Authentication.__init__(self, request)

    def get(self):
        pass
    
    def post(self):
        response = self.check_auth()
        if response:
            return response
        response = member_list(self.args,
                self.producer_data)
        if response:
            return response
app.add_url_rule('/memberlistform', view_func=MemberListForm.as_view('memberlistform'))



