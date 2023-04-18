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
```bash
poetry add git https://github.com/Spichki-Game/gRPC-API-generator.git
```

<br>

#### After the above steps, run your script to generate gRPC API:

```shell
poetry run generate-api $SERVICE_NAME
```

<br>

## Required microservice project structure

```python
src/
   name_of_other_package/
      __init__.py
      ...etc

  name_of_main_package/
      __init__.py
      ...etc

  grpc_api/
      __init__.py
      name_of_main_package_pb2.py
      name_of_main_package_pb2_grpc.py

  protobuf/
      name_of_main_package.proto
```
