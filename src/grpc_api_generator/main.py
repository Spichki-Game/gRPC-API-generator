import os
import sys
import subprocess

from grpc_tools import protoc


class GeneratorAPI:
    WORK_DIR: str = "src"
    PROTO_DIR: str = "protobuf"
    API_DIR: str = "grpc_api"

    def __init__(self, service_name: str):
        self.service_name = service_name

    def __generate(self) -> None:
        protoc.main(
            [f"-I{self.API_DIR}",
             "--python_out=.",
             "--grpc_python_out=.",
             "--pyi_out=.",
             f"{self.API_DIR}/{self.service_name}.proto"]
        )

    def __change_workdir(self) -> None:
        os.chdir(self.WORK_DIR)

    def __copy_proto(self) -> None:
        subprocess.call(
            ["cp",
             f"{self.PROTO_DIR}/{self.service_name}.proto",
             f"{self.API_DIR}/{self.service_name}.proto"]
        )

    def __remove_proto(self) -> None:
        subprocess.call(
            ["rm",
             "-f",
             f"{self.API_DIR}/{self.service_name}.proto"]
        )

    def __print_complete(self) -> None:
        api_files: str = subprocess.getoutput(
            f"ls {self.API_DIR}/{self.service_name}*.py*"
        )

        print()
        print(" [ Info ]: Generated api files:")

        for name in api_files.split('\n'):
            print(f"  - {name}")
        print()

    def run(self, echo: bool = False) -> None:
        self.__change_workdir()
        self.__copy_proto()
        self.__generate()
        self.__remove_proto()
        self.__print_complete() if echo else None


def run(command_line_args: list = sys.argv) -> None:
    try:
        generator = GeneratorAPI(service_name=command_line_args[1])
        generator.run(echo=True)
    except IndexError:
        print("[ Error ]: Missing service name parameter")
