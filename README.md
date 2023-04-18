# gRPC API generator

Common library for the Spichki Game project. It's provide gRPC API (server + client stubs) for gateway-to-microservice communication.

<br>

## Usage

#### Add **grpc-api-generator** library to [Poetry config](https://python-poetry.org/docs/pyproject/):

```toml
# File: pyproject.toml

[tool.poetry.dependencies]
grpc-api-generator = {git = "https://github.com/Spichki-Game/gRPC-API-generator.git"}

[tool.poetry.scripts]
generate-api = "grpc_api_generator:run"

```

<br>

Alternatively, you can use [Poetry CLI](https://python-poetry.org/docs/cli/#add):
```Shell
poetry add git https://github.com/Spichki-Game/gRPC-API-generator.git
```

<br>

#### After the above steps, run your script to generate gRPC API:

```Shell
poetry run generate-api $SERVICE_NAME
```

<br>

#### Usage in your services:

* Server:
```Python
import grpc
import asyncio

from grpc_api import service_name_pb2 as msg
from grpc_api import service_name_pb2_grpc as srv


LISTEN_ADDR = "[::]:50051"


class ServiceName(srv.ServiceNameServicer:
    async def RpcName(self,
                      request: msg.RequestNameType,
                      context: grpc.aoi.ServicerContext) -> msg.ResponseNameType:
        
        return msg.ResponseNameType(
            field_name_a=data,
            field_name_b=data
        )
        
        
async def service_name_server() -> None:
    server = grpc.aio.server()
    
    srv.add_ServiceNameServicer_to_server(
        ServiceName(),
        server
    )
    
    server.add_insecure_port(LISTEN_ADDR)
    
    await server.start()
    await server.wait_for_termination()
    
    
def start() -> None:
    print("[ Start ]: Service_name server\n")
    
    asyncio.run(
        service_name_server()
    )

```

* Client:
```Python
from grpc_api import service_name_pb2 as msg
from grpc_api import service_name_pb2_grpc as srv
```

<br>

## Required microservice project structure

```yaml
service_name/:
   docs/:
      - etc...
      
   src/:

      name_of_other_package/:
         - __init__.py
         - etc...

      service_name/:
         - __init__.py
         - etc...

      grpc_api/:
         - __init__.py
         - name_of_main_package_pb2.py       # generated types from proto schema
         - name_of_main_package_pb2_grpc.py  # generated server and client stubs

      protobuf/:
         - service_name.proto
         
   tests/:
      - etc...

   - .dockerignore
   - Dockerfile
   - LICENSE
   - README.md
   - pyproject.toml
```
