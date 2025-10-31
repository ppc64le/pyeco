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
        self.assertEqual(version, "4.3.0", f"Expected bcrypt 4.3.0, got {version}")

    def test_bcrypt_hash_and_check(self):
        """Use bcrypt to hash and verify a password"""
        password = b"super_secret"
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password, salt)

        # Check that hashed password verifies correctly
        self.assertTrue(bcrypt.checkpw(password, hashed), "Password verification failed")

if __name__ == "__main__":
    unittest.main()  