import unittest
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

class TestBasicFunctionality(unittest.TestCase):
    
    def test_flask_import(self):
        \"\"\"Test that Flask can be imported\"\"\"
        try:
            import flask
            self.assertTrue(True)
        except ImportError:
            self.fail(\"Failed to import Flask\")
    
    def test_basic_math(self):
        \"\"\"Basic test to verify testing works\"\"\"
        self.assertEqual(1 + 1, 2)
    
    def test_environment(self):
        \"\"\"Test Python environment\"\"\"
        import sys
        self.assertGreaterEqual(sys.version_info[0], 3)

if __name__ == '__main__':
    unittest.main()
