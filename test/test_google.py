import unittest

from Translator import GoogleTranslator

class TestGoogleTranslator(unittest.TestCase):

    def setUp(self):
        self.translator = GoogleTranslator()

    def test_translation(self):
        result = self.translator.translate("Hello, world!", src='en', dst='zh-tw')
        self.assertEqual(result, "你好世界！")

if __name__ == '__main__':
    unittest.main()