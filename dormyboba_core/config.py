# from typing import Any
# from dataclasses import dataclass
# import yaml
# from pathlib import Path

# @dataclass
# class PostgresConfig:
#     db_url: str

#     @staticmethod
#     def parse(yaml_config: Any) -> 'PostgresConfig':
#         user=yaml_config["user"]
#         password=yaml_config["password"]
#         host=yaml_config["host"]
#         db=yaml_config["db"]

#         return PostgresConfig(
#             db_url=f"postgresql+psycopg2://{user}:{password}@{host}/{db}"
#         )

# @dataclass
# class GsheetConfig:
#     defect_sheet_id: str

#     @staticmethod
#     def parse(yaml_config: Any) -> 'GsheetConfig':
#         return GsheetConfig(
#             defect_sheet_id=yaml_config["defect_sheet_id"]
#         )

# @dataclass
# class DormybobaConfig:
#     domain: str
#     private_key: str
#     pg_config: PostgresConfig
#     gsheet_config: GsheetConfig

#     @staticmethod
#     def parse(yaml_config: Any) -> 'DormybobaConfig':
#         return DormybobaConfig(
#             domain=yaml_config["domain"],
#             private_key=yaml_config["private_key"],
#             pg_config=PostgresConfig.parse(yaml_config["postgres"]),
#             gsheet_config=GsheetConfig.parse(yaml_config["gc"]),
#         )

# def parse_config(path: str | Path) -> DormybobaConfig:
#     with open(path, "r") as yamlfile:
#         yaml_config = yaml.load(yamlfile, Loader=yaml.FullLoader)["dormyboba"]
#         return DormybobaConfig.parse(yaml_config)
