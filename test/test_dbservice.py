import time
import unittest
from unittest.mock import patch

from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound

from src.database import Paste, page_limit, service, token_generate


class TestDBService(unittest.TestCase):
    def dict_compare_common(self, d1, d2):
        for k in d1.keys() & d2.keys():
            self.assertEqual(d1[k], d2[k])

    def test_token(self):
        s = set()
        n = 1000
        for _ in range(n):
            s.add(token_generate())
        self.assertEqual(len(s), n)

    def test_add_get_expire(self):
        dic = {
            'ip': '1.2.3.4',
            'poster': 'test',
            'language': 'c',
            'content': 'main(){printf("helloworld");}',
            'expire': 0.5,
            'secret': False
        }
        paste = Paste(dic)
        token = service.add(paste)
        check = service.get(token)
        self.assertEqual(len(check), 6)
        self.assertEqual(type(check['token']), str)
        self.assertGreaterEqual(len(check['token']), 6)
        self.dict_compare_common(check, paste._toDict())
        time.sleep(0.5)
        self.assertRaises(NotFound, service.get, token)

    @patch('src.database.token_generate')
    def test_duplicate_token(self, mock_token_generate):
        mock_token_generate.side_effect = [
            '1111111',
            '1111111', '1111111',
            '1111111', '2222222'
        ]
        dic = {
            'none': 'none',
            'ip': '1.2.3.4',
            'content': 'main(){printf("helloworld");}'
        }
        token = service.add(Paste(dic))
        self.assertEqual(token, '1111111')
        self.assertRaises(IntegrityError, service.add, Paste(dic))
        token = service.add(Paste(dic))
        self.assertEqual(token, '2222222')
        self.assertEqual(mock_token_generate.call_count, 5)

    def test_add_page_trim_expire(self):
        import werkzeug
        self.assertRaises(werkzeug.exceptions.NotFound, service.page, 0)
        dic = {
            'ip': '1.2.3.4',
            'poster': 'test',
            'language': 'c',
            'content': 'main(){printf("helloworld");}',
            'expire': 0.5,
            'secret': False
        }
        n = 15
        self.assertGreater(n, page_limit)
        self.assertLessEqual(n, page_limit * 2)
        for _ in range(n):
            service.add(Paste(dic))
        p1 = service.page(1)
        self.assertEqual(len(p1['items'][0]), 6)
        self.assertEqual(len(p1['items']), page_limit)
        self.assertEqual(p1['pagination']['current'], 1)
        p2 = service.page(2)
        self.assertEqual(p2['pagination']['current'], 2)
        self.assertGreaterEqual(p2['pagination']['sum'], 2)
        self.assertEqual(p1['pagination']['sum'], p2['pagination']['sum'])
        p1 = p1['items']
        p2 = p2['items']
        p2 = p2[:n - page_limit]
        for i in p1 + p2:
            self.assertEqual(len(i), 6)
            for k in i.keys() & dic.keys():
                self.assertEqual(i[k], dic[k])

        # expire
        time.sleep(0.5)
        after = service.page(1)['items']
        for i in after:
            self.assertNotEqual(i['token'], p1[0]['token'])

        # trim
        token = p1[0]['token']
        check1 = service._get_obj(token)
        self.assertEqual(type(check1), Paste)
        self.assertEqual(check1.content, dic['content'])
        oldsize = len(Paste.query.all())
        service.trim()
        check2 = service._get_obj(token)
        self.assertEqual(check2, None)
        newsize = len(Paste.query.all())
        self.assertLessEqual(newsize, oldsize - n)

    def test_trim_counter(self):
        dic = {
            'ip': '1.2.3.4',
            'poster': 'test',
            'language': 'c',
            'content': 'main(){printf("helloworld");}',
            'expire': -1,
            'secret': False
        }
        token = service.add(Paste(dic))
        time.sleep(0.5)
        service.trim()
        check = service.get(token)
        self.assertEqual(check['content'], dic['content'])

    def test_page_outofrange(self):
        self.assertRaises(NotFound, service.page, 0)
        self.assertRaises(NotFound, service.page, 900)
