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
import run_test

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)
EXEC = './image-stitching'
debug_url = 'https://www.baidu.com/img/baidu_jgylogo3.gif'
#local_path = '/Users/YiwenMac/VR_Project/PAVR/src/imagelist/'
local_path = os.path.join(os.path.dirname(__file__),'imagelist')
'''
json example
localhost:8000/PAVR?imagelist={"imagelist":[{"batchNo": "0001","fileList":["abcd_0_0.jpg","abcd_0_1.jpg","abcd_0_2.jpg"]},{"batchNo": "0002","fileList":["abcd_0_0.jpg","abcd_0_1.jpg","abcd_0_2.jpg"]}]}
    
'''
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        '''
         get json
        '''
        imagelist = self.get_argument('imagelist')
        img_list_json = json.loads(imagelist)
        keys = img_list_json.keys()
        print(keys)
        for key in keys:
            value = img_list_json[key]
            print(value)
        self.write(imagelist)                                #write on website
        '''
        get url from json
        '''
        image_listNo = img_list_json.get('imagelist')
        for i in range(0,len(image_listNo)):
            batch_listNo = image_listNo[i].get('batchNo')
            file_listNo = image_listNo[i].get('fileList')
            for j in range(0,len(file_listNo)):
                img_url_list ='http://localhost:8000/PAVR/imagelist/' + batch_listNo + '/' + file_listNo[j]    #nas
                if not os.path.exists(os.path.join(local_path,batch_listNo)):
                      os.makedirs(os.path.join(local_path,batch_listNo))
                local = os.path.join(local_path,batch_listNo,file_listNo[j])
                urllib.urlretrieve(debug_url, local)         #debug_url for debuging, image_url_list for running
            print ('downloading')
            image_globs = 'imagelist/' + batch_listNo + '/*'
            debug_image_globs = 'example-data/test_b/*'         #use to debug
            run_test.test_final_size(debug_image_globs)       #image_globs for running
            newname = 'dbd_vr'+ batch_listNo +'.jpg'
            if os.path.isfile('out.jpg'):
                Info = "Succeed"
                os.rename("out.jpg",newname)
                shutil.move(newname,os.path.join(local_path,batch_listNo))
            else:
                Info = "Failed"




if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/PAVR", IndexHandler)])   #Path
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
