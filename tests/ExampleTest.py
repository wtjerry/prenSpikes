import unittest


class ExampleTest(unittest.TestCase):
    def test_true_equals_true(self):
        self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.main()
