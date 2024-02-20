import unittest
from dormyboba_core.config import PostgresConfig, GsheetConfig, DormybobaConfig, parse_config
from pathlib import Path

class TestPostgresConfig(unittest.TestCase):
    def test_parse(self):
        yaml_config = {"user": "user", "password": "password", "host": "localhost", "db": "database"}
        postgres_config = PostgresConfig.parse(yaml_config)
        self.assertEqual(postgres_config.db_url, "postgresql+psycopg2://user:password@localhost/database")

class TestGsheetConfig(unittest.TestCase):
    def test_parse(self):
        yaml_config = {"defect_sheet_id": "your_sheet_id"}
        gsheet_config = GsheetConfig.parse(yaml_config)
        self.assertEqual(gsheet_config.defect_sheet_id, "your_sheet_id")

class TestDormybobaConfig(unittest.TestCase):
    def test_parse(self):
        yaml_config = {
            "domain": "your_domain",
            "private_key": "your_private_key",
            "postgres": {"user": "user", "password": "password", "host": "localhost", "db": "database"},
            "gc": {"defect_sheet_id": "your_sheet_id"}
        }
        dormyboba_config = DormybobaConfig.parse(yaml_config)
        self.assertEqual(dormyboba_config.domain, "your_domain")
        self.assertEqual(dormyboba_config.private_key, "your_private_key")
        self.assertIsInstance(dormyboba_config.pg_config, PostgresConfig)
        self.assertIsInstance(dormyboba_config.gsheet_config, GsheetConfig)
        self.assertEqual(dormyboba_config.pg_config.db_url, "postgresql+psycopg2://user:password@localhost/database")
        self.assertEqual(dormyboba_config.gsheet_config.defect_sheet_id, "your_sheet_id")

class TestParseConfig(unittest.TestCase):
    def test_parse_config(self):
        yaml_content = """
        dormyboba:
          domain: "your_domain"
          private_key: "your_private_key"
          postgres:
            user: "user"
            password: "password"
            host: "localhost"
            db: "database"
          gc:
            defect_sheet_id: "your_sheet_id"
        """
        yaml_path = Path("test_config.yaml")
        with open(yaml_path, "w") as yamlfile:
            yamlfile.write(yaml_content)

        dormyboba_config = parse_config(yaml_path)
        self.assertEqual(dormyboba_config.domain, "your_domain")
        self.assertEqual(dormyboba_config.private_key, "your_private_key")
        self.assertIsInstance(dormyboba_config.pg_config, PostgresConfig)
        self.assertIsInstance(dormyboba_config.gsheet_config, GsheetConfig)
        self.assertEqual(dormyboba_config.pg_config.db_url, "postgresql+psycopg2://user:password@localhost/database")
        self.assertEqual(dormyboba_config.gsheet_config.defect_sheet_id, "your_sheet_id")

        # Clean up the test file
        yaml_path.unlink()

if __name__ == '__main__':
    unittest.main()
