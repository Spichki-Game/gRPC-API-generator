import sys
import subprocess

from grpc_tools import protoc


class GeneratorAPI:
    PROTO_PATH: str = "src/protobuf"
    API_PATH: str = "src/grpc_api"

    def __init__(self, service_name: str):
        self.service_name = service_name

    def run(self, echo: bool = False) -> None:
        self.generate()
        self.move()
        self.patch()
        self.print_complete() if echo else None

    def generate(self) -> None:
        protoc.main(
            [f"--proto-path={self.PROTO_PATH}",
             "--python_out=.",
             "--grpc_python_out=.",
             f"{self.PROTO_PATH}/{self.service_name}.proto"]
        )

    def move(self) -> None:
        file_names = [
            f"{self.service_name}_pb2.py",
            f"{self.service_name}_pb2_grpc.py"
        ]

        for name in file_names:
            subprocess.call(
                ["mv",
                 f"{self.PROTO_PATH}/{name}",
                 f"{self.API_PATH}/{name}"]
            )

    def patch(self) -> None:
        target_file = f"{self.API_PATH}/{self.service_name}_pb2_grpc.py"
        patch = "s/from src.protobuf/from grpc_api/"

        subprocess.call(
            ["sed", "-i", patch, target_file]
        )

    def print_complete(self) -> None:
        api_files: str = subprocess.getoutput(
            f"ls {self.API_PATH}"
        )

        print("[ Info ]: Generated api files:")

        for name in api_files.split('\n'):
            print(f" - {self.API_PATH}/{name}")


def run(command_line_args: list = sys.argv) -> None:
    try:
        generator = GeneratorAPI(service_name=command_line_args[1])
        generator.run(echo=True)
    except IndexError:
        print("[ Error ]: Missing service name parameter")
