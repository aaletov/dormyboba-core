import unittest
from dormyboba_core.entity.token import Token, TokenConverter

class TestToken(unittest.TestCase):
    def test_generate(self):
        role = "admin"
        generated_token = Token.generate(role)
        self.assertEqual(generated_token.role, role)
        self.assertTrue(100000 <= generated_token.random_id <= 999999)

class TestTokenConverter(unittest.TestCase):
    def setUp(self):
        # Replace with your actual private key content
        self.private_key = "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDOlvneslguiNNh\n0FklBNyte58DyOTY1Lmjjeq0/kzE1c/pBhdAz96Qu2Q+SMwIZvqih/fBxUeoZiLC\nd3cPrOTKOin8gp8uVX+Nnj7pixh+KQwzJv2FKa3+6e1tESnQ+BuvvMm0ToGda5oW\nMl8QWPtERcHaF6bvUzp41rx+vogzJBEBAcF/N7i2gJ+OpRqCZim/nzT/iGDXdDvX\n01juYJC9KV/0E9x+dqSze6gjBftUCkhTyzTVUfZHyxDbyjTX+0hj8O3zwiVKpV/X\nMCKNrEaBsyI79odysvccDvAImJu/askVHc2mp4ieSksvCml0eU/hs3mb4fPB5HZN\nxHZFHIQ5AgMBAAECggEAAyltPnR4Ygjgh1a/wbp0OLdeRuaV2twcN+hv5yKDgQH7\nh4fH5pgShocD9T9pYM8kiiLfmVzYxCYjOqdxnzdt1Nv7O6igh8sLQ58+O9p6kg2a\n16DpLDTOQ/XP23rpVY/te8AsX1L8q9tqxWjuaqvvTNHU5WY+q/06Rk4M633xf4Au\nzfQIYCWovQiueuSvAqVraCi7f2f+FNHzQgmltZOSjlbt6meJVGQ/HVpp+QfbDhkT\nDUDHvvKbiNcF4h0oGQqHUcRt3DKKX8erV+7LhtASDZcX37ImtSc6+Z98o+XNGkeZ\n5Ob7p7IICCtpcrdpRS0rkDZ+3nqwXOCXqBMnISN62wKBgQDompQfKOK2fYPS5JXK\nno1PzkHmQtQCn9L7TlMeVd9BJPmj1nqethxHllfnHCjIdqqYQi2C2q5cOq7lGBYo\nnE8ChVgqsC3bsNc9YYvMVMf8kuB882+ozC65+zghv+38LnjtHjoteFpg35mab3o1\nMUIWHsq3LEV8RkQq/KZWqdpaowKBgQDjXoyepECNQR/FNakcN1lt19cjS9z8dD8Z\nDFqUYMtCMSn+w3KzuUz9AR34hL4f1AZlp6wOY6JDGcWGPbmgMCWiZf+nf0SUSHzZ\nA3YKaw2Ik0l6vWwhMfiDLsIzkeWw5HQkRN3RRCtQV7IFhu45Z31x8wv6Dl0mx9bp\nkuDinBTPcwKBgHTQlMzlSp5dgKOcGsIMSGmo6x2JuFGtFFcTKdkVRS7BNAIdB63H\nRYKKNZEiajTqq5gVvCd4TZKSAh2ZsB8rCN76OqINoqovMJlp8LxoY5sr5EO8Ofpq\nuJi8Wp9QdWNtr1teD9egFruJ7+lITPaDy22yfxnoyOi1nSx9f8gMO1XDAoGAZE/o\nlm09FZTv4WAFVi+NQwsBHc9wlejrla9/nwr9YhyyvHWae3R7ZPxDLsvR3dT7ZYoO\nPOL0Scpq/QjqhqP3VqjNnCZoKUu52TzPrVUByYnB12cO965GSAovH/V0cxC3tPC1\nNIhw26d1IT8ghy8Dh2yFkjMYIe31AWQN16yo+cUCgYEAjog1Rg3zx9fEqjykcce0\nUiaAJMDv8iKp2FMcSrRS+d0tVke8KlHNOjFzrMSfsT1DyOL2mER6q03xejjD4wWy\nb6Tfo8uOa9w4j9t/BQKad/0SaxJiPjABKtqHLbffSKGfw+sg115ivQH2bzDUIgfo\nzx7PasDEkgYHa3Qv7/yAAkc=\n-----END PRIVATE KEY-----\n"

        self.token_converter = TokenConverter(private_key=self.private_key)

    def test_encode_decode(self):
        role = "admin"
        original_token = Token.generate(role)
        
        encoded_token = self.token_converter.encode(original_token)
        decoded_token = self.token_converter.decode(encoded_token)

        self.assertEqual(decoded_token.role, original_token.role)
        self.assertEqual(decoded_token.random_id, original_token.random_id)

if __name__ == '__main__':
    unittest.main()
