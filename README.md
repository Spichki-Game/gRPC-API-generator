# gRPC-API Generator

Library for the Spichki Game project.

<br>
<br>

## API

func: run(project_name: str) -> bool
---

This function generates gRPC-API (Server + Client) from a protobuf files. The library was required for comfortable api generation for microservices of the Spichki Game project.

<br>
<br>

## Required microservice project structure

```
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

    proto_schemas/
        name_of_main_package.proto
```
