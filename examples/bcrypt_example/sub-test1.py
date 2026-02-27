import unittest
import importlib.metadata
import bcrypt

class TestBcryptLibrary(unittest.TestCase):
    def test_bcrypt_import(self):
        """Check if bcrypt can be imported"""
        try:
            import bcrypt
        except ImportError:
            self.fail("bcrypt is not installed")

    def test_bcrypt_version(self):
        """Verify bcrypt version"""
        version = importlib.metadata.version("bcrypt")
        assert "4.3.0" in version, f"'4.3.0' not found in version string: {version}"

    def test_bcrypt_hash_and_check(self):
        """Use bcrypt to hash and verify a password"""
        password = b"super_secret"
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password, salt)

        # Check that hashed password verifies correctly
        self.assertTrue(bcrypt.checkpw(password, hashed), "Password verification failed")

if __name__ == "__main__":
    unittest.main()  