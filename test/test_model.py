import unittest
import datetime
from src.database import Paste, endless


class TestModel(unittest.TestCase):
    def dict_compare_common(self, d1, d2):
        for k in d1.keys() & d2.keys():
            self.assertEqual(d1[k], d2[k])

    def test_endless(self):
        self.assertEqual(endless.year, 9999)

    def test_init_str_toDict_outputDict(self):
        dic = {
            'ip': '1.2.3.4',
            'poster': 'test',
            'language': 'c',
            'content': 'main(){printf("helloworld");}',
            'expire': 2592000,
            'secret': False
        }
        paste = Paste(dic)
        _ = paste.__str__()  # test toString method

        pasteDict = paste._toDict()
        self.assertEqual(len(pasteDict), 9)
        self.assertEqual(pasteDict['id'], None)
        self.assertEqual(pasteDict['token'], None)
        self.assertLess(datetime.datetime.now() - datetime.datetime.fromtimestamp(pasteDict['paste_time']),
                        datetime.timedelta(seconds=1))
        self.assertEqual(pasteDict['expire_time'], pasteDict['paste_time'] + dic['expire'])
        self.dict_compare_common(pasteDict, dic)

        outputDict = paste.outputDict()
        self.assertEqual(len(outputDict), 6)
        self.dict_compare_common(outputDict, pasteDict)

    def test_init_default_toDict_outputDict(self):
        dic = {
            'none': 'none',
            'ip': '1.2.3.4',
            'content': 'main(){printf("helloworld");}'
        }
        paste = Paste(dic)

        pasteDict = paste._toDict()
        self.assertEqual(len(pasteDict), 9)
        self.assertEqual(pasteDict['id'], None)
        self.assertEqual(pasteDict['token'], None)
        self.assertEqual(pasteDict['poster'], '')
        self.assertEqual(pasteDict['language'], '')
        self.assertEqual(pasteDict['secret'], False)
        self.assertLess(datetime.datetime.now() - datetime.datetime.fromtimestamp(pasteDict['paste_time']),
                        datetime.timedelta(seconds=1))
        self.assertEqual(pasteDict['expire_time'],
                         pasteDict['paste_time'] + datetime.timedelta(weeks=1).total_seconds())
        self.dict_compare_common(pasteDict, dic)

        outputDict = paste.outputDict()
        self.assertEqual(len(outputDict), 6)
        self.dict_compare_common(outputDict, pasteDict)

    def test_init_toDict_incomplete(self):
        dic = {
            'ip': '1.2.3.4',
            'poster': 'test',
            'language': 'c',
            'expire': 2592000,
            'secret': False
        }
        try:
            paste = Paste(dic)
        except KeyError:
            return
        self.fail('Missing necessary field but no exception')

    def test_content_empty(self):
        dic = {
            'none': 'none',
            'ip': '1.2.3.4',
            'content': ''
        }
        try:
            paste = Paste(dic)
        except RuntimeError:
            return
        self.fail('content can be empty')