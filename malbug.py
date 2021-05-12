import os
import json
import base64

from flask import request, Flask
from flask_restful import Api, Resource


class SendFile(Resource):

    def post(self):
        pass

    def get(self):
        pass


class CheckConfig(Resource):

    def post(self):
        pass

    def get(self):
        pass


class PurchaseKey(Resource):

    def post(self):
        pass

    def get(self):
        pass


class Initialize(Resource):

    @staticmethod
    def successfully_initialized():
        return {"success": "initialized"}

    @staticmethod
    def already_initialized():
        return {"error": "already initialized"}

    def post(self):
        data = request.json
        results = init(api_key=data["apikey"], url=data["url"])
        if results[1]:
            return self.already_initialized()
        else:
            return self.successfully_initialized()

    def get(self):
        return {"error": "nothing here"}


class ListNewestDownloads(Resource):

    def post(self):
        pass

    def get(self):
        pass


class LocalFlask(Flask):

    def process_response(self, response):
        response.headers['Server'] = "Malbug API handler"
        response.headers['Contact'] = "For more information email us at contact@penetrum.com"
        response.headers['Hey-There'] = str(base64.b64decode(
            "SGV5IHRoZXJlIGhhY2tlciwgaWYgeW91J3JlIHJlYWRpbmcgdGhpcyB5b3UgcHJ"
            "vYmFibHkgZmlndXJlZCBvdXQgdGhhdCB0aGlzIGlzbid0IGFueXRoaW5nIGltcG9"
            "ydGFudCwgYnV0IG1heWJlIHlvdSBzaG91bGQgYmUgd29ya2luZyBmb3IgdXM/IEZl"
            "ZWwgZnJlZSB0byBzZW5kIHlvdXIgcmVzdW1lIHRvIGNvbnRhY3RAcGVuZXRydW0uY"
            "29t"
        ))
        response.headers['Made-With-Love'] = "Penetrum; Audits, security, and research. Made Simple"
        super(LocalFlask, self).process_response(response)
        return response


def get_downloads_folder():
    if os.name == "nt":
        import winreg

        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
    else:
        location = os.path.join(os.path.expanduser("~"), 'Downloads')
    return location


def init(**kwargs):
    api_key = kwargs.get("api_key", None)
    url = kwargs.get("url", None)
    home = kwargs.get("home", "{}/.malbug".format(os.path.expanduser("~")))
    config = "{}/malbug.json".format(home)

    if not os.path.exists(home):
        os.makedirs(home)
        with open(config, "a+") as f:
            data = {
                "api_key": str(base64.b64encode(api_key.encode())) if api_key is not None else "API-KEY-FILLER",
                "url": str(base64.b64encode(url.encode())) if url is not None else "https://api.penetrum.com/score",
                "downloads_folder": get_downloads_folder()
            }
            json.dump(data, f)
            is_done = False
    else:
        with open(config) as f:
            data = json.load(f)
            is_done = True
    return data, is_done


def main():
    app = LocalFlask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = 35000000
    api = Api(app)
    api.add_resource(SendFile, "/malbugapi/send")
    api.add_resource(CheckConfig, "/malbugapi/config")
    api.add_resource(PurchaseKey, "/malbugapi/purchase")
    api.add_resource(Initialize, "/malbugapi/init")
    app.run(host="127.0.0.1", port=9801)


if __name__ == "__main__":
    main()
