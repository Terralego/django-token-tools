from django.test import TestCase

from token_tools.generator import TokenGenerator


class TokenGeneratorTestCase(TestCase):
    def setup(self):
        self.generator = TokenGenerator()

    def test_fake(self):
        # just test if module is loaded
        self.assertTrue(True)
