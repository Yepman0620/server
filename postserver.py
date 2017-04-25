import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.autoreload
import json
import os
import shutil
import urllib
import sys
import glob
import subprocess
import re

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        #img_list_json = json.loads(imagelist)
    def post(self):
        img_list_json = json.loads(self.request.body)
        keys = img_list_json.keys()
        print(keys)
        for key in keys:
            value = img_list_json[key]
            print(value)
        '''
        get url from json
        '''
        image_listNo = img_list_json.get('imagelist')
        dict2 = dict()
        for i in range(0,len(image_listNo)):
            batch_listNo = image_listNo[i].get('batchNo')
            file_listNo = image_listNo[i].get('fileList')
            for j in range(0,len(file_listNo)):
                file_Id = file_listNo[j].get('fileId')
                file_Num = file_listNo[j].get('fileNo')
                img_url_list ='http://localhost:8000/PAVR/imagelist/' + batch_listNo + '/' + file_Id    #nas
                print img_url_list
            print "VR processing"
            print "Upload vr jpg"
            result = 'Succeed'
            debug_filename = 'dbvr***.jpg'
            #upload_path = os.path.join(os.path.dirname(__file__), 'dbvr***.jpg')
            callback_url = 'http://localhost:8000/PAVR/imagelist/' + batch_listNo + '/' + 'dbvr***.jpg'
            print callback_url
            dict1 = {"batchNo":batch_listNo,"result":result,"file_Id":debug_filename}
            dict2.setdefault("imageList",[]).append(dict1)
        self.write(json.dumps(dict2))

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/PAVR", IndexHandler)])   #Path
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
