# https://towardsdatascience.com/flask-an-easy-access-door-to-api-development-2147ae694ceb
# Flask: An Easy Access Door to API development
"""a get and post call to show the working of Flask API
GET call recieves data from a file present in server and
POST call saves a file sent to the server"""

__author__ = "Tushar SEth"
__email__  = "tusharseth93@gmail.com"

import os
from flask import request
from flask import json
from flask import Response
from flask_cors import CORS
from flask_api import FlaskAPI

APP = FlaskAPI(__name__)
CORS(APP)

STATUS = "STATUS"
ERROR_FILES_LIST = "ERROR_FILES_LIST"
FILES_RECEIVED_LIST = "FILES_LIST"
LABELS_MAPPING = "labels_mapping"

@APP.route("/getJsonFromFile/<filename>", methods=['GET'])
def get_json_response(filename):
    """sends json as a response for the file which contains name to number
    mapping and returns"""
    labels_dict = {}
    response_dict = {}
    try:
        with open(filename, 'r') as labels:
            labels_dict = json.load(labels)
        print(labels_dict)
        print("\n---------------------labels_dict---------------------\n")
        response_dict[STATUS] = "true"
        response_dict["LABELS_MAPPING"] = labels_dict
        print("response_dict is: ", response_dict)
        js_dump = json.dumps(response_dict)
        resp = Response(js_dump,
                        status=200,
                        mimetype='application/json')

    except FileNotFoundError as err:
        print("FileNotFoundError in downloadLabel", err)
        response_dict[STATUS] = "false"
        response_dict = {'error': 'file not found in server'}
        js_dump = json.dumps(response_dict)
        resp = Response(js_dump,
                        status=500,
                        mimetype='application/json')
        print("sending error response")
    except RuntimeError as err:
        print("RuntimeError error in downloadLabel", err)
        response_dict[STATUS] = "false"
        response_dict = {'error': 'error occured on server side. Please try again'}
        js_dump = json.dumps(response_dict)
        resp = Response(js_dump,
                        status=500,
                        mimetype='application/json')
    return resp


@APP.route("/uploadFiles", methods=['POST'])
def upload_files():
    """uploads file to the server. This will save file to the
        directory where server is running"""
    response_dict = {}
    error_files = ""
    dir_name = "."
    try:
        dir_name = request.form['DIR_NAME']
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        recieved_files = request.files.getlist(FILES_RECEIVED_LIST)
        print(len(recieved_files))
        for each_file in recieved_files:
            each_file_name = each_file.filename
            print(each_file_name)
            try:
                each_file.save(os.path.join(".", dir_name, each_file.filename.replace(" ", "_")))
                print("file saved")
            except RuntimeError as err:
                print("\nError in saving file: %s :: %s", each_file.filename, err)
                error_files = error_files + "," + each_file.filename
        response_dict[STATUS] = "true"
        response_dict[ERROR_FILES_LIST] = error_files
        js_dump = json.dumps(response_dict)
        resp = Response(js_dump,
                        status=200,
                        mimetype='application/json')

    except RuntimeError as err:
        print("RuntimeError error in downloadLabel", err)
        response_dict = {'error': 'error occured on server side. Please try again'}
        response_dict[STATUS] = "false"
        js_dump = json.dumps(response_dict)
        resp = Response(js_dump,
                        status=500,
                        mimetype='application/json')
    return resp

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=5000)