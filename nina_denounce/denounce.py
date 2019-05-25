import json
import ast
from util.crypto import decode_rs512

import grpc
import rpc.user_service_pb2_grpc as user_service_pb2_grpc
import rpc.user_service_pb2 as user_service_pb2
import falcon
from nina_denounce.repo.denounce_repo import DenounceRepo, Denounce

class DenounceApi:

    def __init__(self, denounce_repo):
        self.denounce_repo = denounce_repo

    def on_post(self, req, resp):
        try:
            denounce_payload = json.load(req.bounded_stream)
            if(self.validate_denounce_payload(denounce_payload)):
                new_denounce = Denounce()
                new_denounce.lat = denounce_payload['lat']
                new_denounce.lon = denounce_payload['lon']
                new_denounce.bus_number = denounce_payload['bus_number']

                new_denounce = self.denounce_repo.save(new_denounce)

                resp_body = {
                    "status": "OK",
                    "denounce_id": str(new_denounce.id)
                }
                resp.body = json.dumps(resp_body, ensure_ascii=False)
        except:
            error_msg = {
                "status": "Bad Request"
            }
            resp.body = json.dumps(error_msg, ensure_ascii=False)
            resp.status = falcon.HTTP_BAD_REQUEST

    def validate_denounce_payload(self, denounce_data):
        if(denounce_data.has_key('lat') and denounce_data.has_key('lon') and denounce_data.has_key('bus_number')):
            return True
        else:
            raise falcon.HTTPBadRequest()

    def on_get(self, req, resp):
        try:
            denounces = self.denounce_repo.list_all()
            resp_body = {
                "status": "OK",
                "denounces": []
            }
            channel = grpc.insecure_channel('localhost:50051')
            stub = user_service_pb2_grpc.UserServiceStub(channel)
            for denounce in denounces:
                user_name = stub.GetName(user_service_pb2.UserId(id=denounce.user_id))
                resp_body["denounces"].insert(0,
                    {
                        "denounce_id": str(denounce.id),
                        "user_id": str(denounce.user_id),
                        "name": user_name.name.encode('utf-8'),
                        "bus_number": str(denounce.bus_number),
                        "lat": str(denounce.lat),
                        "lon": str(denounce.lon)
                    }
                )
            resp.body = json.dumps(resp_body, ensure_ascii=False)
        except:
            error_msg = {
                "status": "Bad Request"
            }
            resp.body = json.dumps(error_msg, ensure_ascii=False)
            resp.status = falcon.HTTP_BAD_REQUEST


class DenounceWithAuth:

    def __init__(self, denounce_repo):
        self.denounce_repo = denounce_repo

    def on_put(self, req, resp):
        try:
            token = self.remove_token_prefix(req.get_header('Authorization'), 'Bearer ')
            user_id_param = ast.literal_eval(decode_rs512(token))

            denounce_payload = json.load(req.bounded_stream)
            if(self.validate_denounce_complete_payload(denounce_payload)):
                denounce = self.denounce_repo.find_by_id(denounce_payload['denounce_id'])
                if(denounce):
                    denounce.user_id = int(user_id_param['user_id'])
                    denounce.description = denounce_payload['description']
                    denounce = self.denounce_repo.save(denounce)
                    resp_body = {
                        "status": "OK",
                        "denounce_id": str(denounce.id)
                    }
                    resp.body = json.dumps(resp_body, ensure_ascii=False)
                else:
                    raise falcon.HTTPBadRequest()
        except:
            error_msg = {
                "status": "Bad Request"
            }
            resp.body = json.dumps(error_msg, ensure_ascii=False)
            resp.status = falcon.HTTP_BAD_REQUEST

    def validate_denounce_complete_payload(self, auth_data):
        if(auth_data.has_key('denounce_id') and auth_data.has_key('description')):
            return True
        else:
            raise falcon.HTTPBadRequest()

    def remove_token_prefix(self, text, prefix):
        return text[text.startswith(prefix) and len(prefix):]


