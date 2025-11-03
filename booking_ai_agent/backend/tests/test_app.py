import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

class TestBasicFunctionality(unittest.TestCase):
    
    def test_imports(self):
        """Test that required modules can be imported"""
        try:
            import flask
            self.assertTrue(True)
        except ImportError:
            self.fail("Flask import failed")
    
    def test_environment(self):
        """Test basic environment"""
        self.assertTrue(True)
    
    def test_python_version(self):
        """Test Python version compatibility"""
        version = sys.version_info
        self.assertGreaterEqual(version.major, 3)
        self.assertGreaterEqual(version.minor, 8)

if __name__ == '__main__':
    unittest.main()