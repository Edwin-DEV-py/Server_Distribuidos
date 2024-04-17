import grpc
import jwt
import concurrent.futures
from upload_pb2 import FileUploadResponse
import upload_pb2_grpc as upload_pb2_grpc

class FileService2(upload_pb2_grpc.FileServiceServicer):
    def Upload(self, request_iterator, context):
        try:
            for request in request_iterator:
                binary_file = request.binary_file
                owner_id = request.owner_id
                file_id = request.file_id

                print("Archivo recibido del cliente:", binary_file)
                print("ID del propietario:", owner_id)
                print("ID del archivo:", file_id)

            return FileUploadResponse(
                file_id=file_id,
                urls=["ruta1GRPC", "ruta2GRPC"]
            )
        except Exception as e:
            print("Error en el servidor:", e)
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.UNKNOWN)
            return FileUploadResponse(message="Error en el servidor")
    
def serve():
    print("Iniciando el servidor...")
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    upload_pb2_grpc.add_FileServiceServicer_to_server(FileService2(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor iniciado correctamente.")
    server.wait_for_termination()
    print("El servidor ha dejado de esperar solicitudes.")
    
if __name__ == '__main__':
    print("funcionando")
    serve()
