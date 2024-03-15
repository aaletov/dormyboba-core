import unittest
from unittest.mock import MagicMock
from dormyboba_core.repository import (
    SqlAlchemyDormybobaUserRepository,
    SqlAlchemyDormybobaRoleRepository,
    SqlAlchemyInstituteRepository,
    SqlAlchemyAcademicTypeRepository,
    GsheetDefectRepository,
    SqlAlchemyMailingRepository,
    SqlAlchemyQueueRepository,
    entity,
)
from dormyboba_core.service.dormyboba_servicer import DormybobaCoreServicer
from dormyboba_core.entity.dormyboba_user import DormybobaUser, DormybobaRole
from dormyboba_core.entity.academic_type import AcademicType
from dormyboba_core.entity.institute import Institute 
from dormyboba_api.v1api_pb2 import GenerateTokenRequest, UpdateUserRequest

class TestDormybobaCoreServicer(unittest.TestCase):
    def setUp(self):

        self.user_repository = MagicMock(SqlAlchemyDormybobaUserRepository)
        self.role_repository = MagicMock(SqlAlchemyDormybobaRoleRepository)
        self.institute_repository = MagicMock(SqlAlchemyInstituteRepository)
        self.academic_type_repository = MagicMock(SqlAlchemyAcademicTypeRepository)
        self.sheet_repository = MagicMock(GsheetDefectRepository)
        self.mailing_repository = MagicMock(SqlAlchemyMailingRepository)
        self.queue_repository = MagicMock(SqlAlchemyQueueRepository)
        self.token_converter = MagicMock(entity.TokenConverter)

        self.servicer = DormybobaCoreServicer(
            self.user_repository,
            self.role_repository,
            self.institute_repository,
            self.academic_type_repository,
            self.sheet_repository,
            self.mailing_repository,
            self.queue_repository,
            self.token_converter,
        )

    def test_generate_token(self):
        request = GenerateTokenRequest(role_name="admin")

        mock_token = entity.Token(role="admin", random_id=123456)
        self.token_converter.encode.return_value = "mocked_encoded_token"
        entity.Token.generate = MagicMock(return_value=mock_token)

        response = self.servicer.GenerateToken(request, None)

        self.assertEqual(response.token, "mocked_encoded_token")
        entity.Token.generate.assert_called_once_with("admin")
        self.token_converter.encode.assert_called_once_with(mock_token)

if __name__ == '__main__':
    unittest.main()
