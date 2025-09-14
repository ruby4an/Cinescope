from models.base_models import RegisterUserResponse

class TestUser:
	def test_create_user(self, super_admin, creation_user_data):
		data = creation_user_data()

		response = super_admin.api.user_api.create_user(data).json()

		register_user_response = RegisterUserResponse(**response)

		assert register_user_response.id and response['id'] != '', "ID должен быть не пустым"

	def test_get_user_by_locator(self, super_admin, creation_user_data):
		data = creation_user_data()

		created_user = super_admin.api.user_api.create_user(data).json()
		response_by_id = super_admin.api.user_api.get_user(created_user["id"]).json()
		response_by_email = super_admin.api.user_api.get_user(created_user["email"]).json()

		assert response_by_id == response_by_email, "Содержание ответов должно быть идентичным"
		assert response_by_id.get('id') and response_by_id['id'] != '', "ID должен быть не пустым"

	def test_get_user_by_id_common_user(self, common_user):
		common_user.api.user_api.get_user(common_user.email, expected_status=403)

	def test_admin(self, admin, common_user):
		admin.api.user_api.get_user(admin.email, expected_status=200)

