import grpc
from server_pb2 import UserCredentials, AuthenticationResponse
import jwt
import server_pb2_grpc as server_pb2_grpc
import concurrent.futures

SECRET_KEY = 'secret'

# Servidor gRPC
class AuthenticationServiceLogin(server_pb2_grpc.AuthenticationServiceServicer):
    
    def AuthenticateUser(self, request, context):
        username = request.username
        password = request.password
        
        
        if username == "admin" and password == "admin":
            print(username)
            payload_data= {
                "name":"admin"
            }
            token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE0MzQ0NjY1LCJpYXQiOjE3MTMwNDg2NjUsImp0aSI6ImVkYjkzMTkwOGI5YjQ2MGJhZDU2MWIzNDcxNDc1YTNmIiwidXNlcl9pZCI6ImFkbWluIn0.PIe92t-GAtNrMB6q8dYOtMUSqWLTQXCy9wlV_M3Zd6Y'
            print(token)
            return AuthenticationResponse(success=True, token=token)
        else:
            context.set_details('Credenciales inválidas')
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            return AuthenticationResponse(success=False, error_message="Credenciales inválidas")
    
#iniciar el server gRPC:
def serve():
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    server_pb2_grpc.add_AuthenticationServiceServicer_to_server(AuthenticationServiceLogin(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
    
