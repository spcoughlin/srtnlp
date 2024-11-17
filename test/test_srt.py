import unittest
from src import srt
import os

class TestSRT(unittest.TestCase):
    def setUp(self):
        self.test_srt_file = 'test_example.srt'
        with open(self.test_srt_file, 'w') as f:
            f.write("""1
00:00:01,000 --> 00:00:04,000
Hello, world!
""")

    def tearDown(self):
        os.remove(self.test_srt_file)

    def test_srt_text_to_string(self):
        srt_string = srt.srt_text_to_string(self.test_srt_file)
        expected_string = "Hello, world!"
        self.assertEqual(srt_string.strip(), expected_string.strip())

if __name__ == '__main__':
    unittest.main()

