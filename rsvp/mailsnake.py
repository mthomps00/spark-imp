import urllib2
import json

class MailSnake(object):
    dc = 'us1'
    base_api_url = 'https://%(dc)s.api.mailchimp.com/1.3/?method=%(method)s&output=%(format)s'

    def __init__(self, apikey = '', extra_params = {}):
        """
            Cache API key and address.
        """
        self.apikey = apikey

        self.default_params = {'apikey':apikey}
        self.default_params.update(extra_params)

        if '-' in self.apikey:
            self.dc = self.apikey.split('-')[1]

    def call(self, method, params = {}):
        url = self.base_api_url % {'dc':self.dc, 'format':'json', 'method':method}
        params.update(self.default_params)

        post_data = json.dumps(params)
        headers = {'Content-Type': 'application/json'}
        request = urllib2.Request(url, post_data, headers)
        response = urllib2.urlopen(request)

        return json.loads(response.read())

    def __getattr__(self, method_name):

        def get(self, *args, **kwargs):
            params = dict((i,j) for (i,j) in enumerate(args))
            params.update(kwargs)
            return self.call(method_name, params)

        return get.__get__(self)

class MailSnakeSTS(MailSnake):
    base_api_url_template = 'https://%(dc)s.sts.mailchimp.com/1.0/%(method)s%(format)s/'
