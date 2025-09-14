import pytest
from base_models import TestUser
from constants.roles import Roles
import logging as logger
from pydantic import ValidationError

pytestmark = pytest.mark.skip(reason="No need to run these tests now")

def test_registered_user(test_user):
	data = test_user.copy()
	user = TestUser(**data)
	assert user.email == data['email']
	assert Roles.USER in user.roles

	json_data = user.model_dump_json(exclude_unset=True)
	logger.info(f'json_data: {json_data}')

def test_creation_user_data(creation_user_data):
	data = creation_user_data().copy()
	user = TestUser(**data)
	assert user.email == data['email']
	assert Roles.USER in user.roles

	json_data = user.model_dump_json()
	logger.info(f'json_data: {json_data}')


def test_unmatched_password(test_user):
	data = test_user.copy()
	data.update({'password': 'zalupa228'})
	try:
		user = TestUser(**data)
	except ValidationError as e:
		logger.info(f'Validation error: {e}')
