from clarifai.client.auth.helper import ClarifaiAuthHelper
from clarifai_grpc.grpc.api.status import status_code_pb2
from clarifai.client import V2Stub, create_stub
from clarifai_grpc.grpc.api import resources_pb2, service_pb2


def authenticate():
    global userDataObject, auth, stub
    auth = ClarifaiAuthHelper(user_id="mansi_k", pat='95978ef1e65e4e1ab8b268e94a49b1e9', app_id="demo_img_app")
    stub = create_stub(auth)
    userDataObject = resources_pb2.UserAppIDSet(user_id=auth.user_id, app_id=auth.app_id)
    return stub, userDataObject



def model_types_lister():
    response = stub.ListModelTypes(
        service_pb2.ListModelTypesRequest(user_app_id=userDataObject), metadata=auth.metadata) #.json()
    if response.status.code not in [status_code_pb2.SUCCESS]:
        print("ERROR: {}".format(response.status.description))
    #   return response
    model_types = []
    for proto in response.model_types:
        model_types.append(proto.id)
    return model_types


def get_model_type_info(model_type_id):
    response = stub.GetModelType(
        service_pb2.GetModelTypeRequest(user_app_id=userDataObject, model_type_id=model_type_id), metadata=auth.metadata) #.json()
    if response.status.code not in [status_code_pb2.SUCCESS]:
        print("ERROR: {}".format(response.status.description))
    #   return response
    return response


