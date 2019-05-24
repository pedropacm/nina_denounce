import falcon

from .denounce import DenounceApi, DenounceWithAuth
from nina_denounce.repo.denounce_repo import DenounceRepo

def create_app():
	denounce_repo = DenounceRepo()
	api = falcon.API()
	api.add_route('/api/v1/denounce/create', DenounceApi(denounce_repo))
	api.add_route('/api/v1/denounce/complete', DenounceWithAuth(denounce_repo))
	return api


def get_app():
    return create_app()