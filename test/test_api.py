import unittest
import json
from flask.wrappers import Response
from src import application
from src.database import service


class TestApi(unittest.TestCase):
    def dict_compare_common(self, d1, d2):
        for k in d1.keys() & d2.keys():
            self.assertEqual(d1[k], d2[k])

    def setUp(self):
        self.client = application.test_client()
        application.app_context().push()

    def test_paste_page(self):
        dic = {
            'ip': '1.2.3.4',
            'poster': 'test',
            'language': 'c',
            'content': 'main(){printf("helloworld");}',
            'expire': 5,
            'secret': False
        }
        ret_post: Response = self.client.post('/paste', data=json.dumps(dic))
        self.assertEqual(ret_post.status_code, 200)
        token = json.loads(ret_post.get_data())['token']

        ret_get: Response = self.client.get('/paste/' + token)
        self.assertEqual(ret_get.status_code, 200)
        getdic = json.loads(ret_get.get_data())
        self.assertEqual(len(getdic), 6)
        self.dict_compare_common(dic, getdic)

        ip = service._get_obj(token).ip
        self.assertEqual(ip, '127.0.0.1')

        ret_get_page: Response = self.client.get('/page/1')
        self.assertEqual(ret_get_page.status_code, 200)
        items = json.loads(ret_get_page.get_data())['items']
        self.assertEqual(items[0], getdic)

    def test_raw(self):
        s = "fsdafewrwefdsc"
        ret_post: Response = self.client.post('/raw', data=s)
        self.assertEqual(ret_post.status_code, 200)
        token = ret_post.get_data().decode()

        ret_get: Response = self.client.get('/raw/' + token)
        self.assertEqual(s, ret_get.get_data().decode())

    def test_default_and_realip_of_paste(self):
        dic = {
            'content': 'main(){printf("helloworld");}'
        }
        ret_post: Response = self.client.post('/paste', data=json.dumps(dic), headers={'X-Real-IP': '8.8.8.8'})
        self.assertEqual(ret_post.status_code, 200)
        token = json.loads(ret_post.get_data())['token']
        ip = service._get_obj(token).ip
        self.assertEqual(ip, '8.8.8.8')

    def test_realip_of_raw(self):
        ret_post: Response = self.client.post('/raw', data='dsadfsadsa', headers={'X-Real-IP': '9.9.9.9'})
        self.assertEqual(ret_post.status_code, 200)
        token = ret_post.get_data().decode()
        ip = service._get_obj(token).ip
        self.assertEqual(ip, '9.9.9.9')
