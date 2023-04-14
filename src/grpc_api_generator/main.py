import os
import sys
import subprocess

from pathlib import Path
from grpc_tools import protoc


class ConstantSet:
    def __init__(self, project_name: str, api_name: str):
        self.project_name = project_name

        for path in sys.path:
            if project_name + '/src' in path:

                self.API_NAME: str = (
                    # self.project_name.lower().replace('-', '_')
                    api_name
                )

                self.API_NAME_ALIAS: str = (
                    self.API_NAME.replace('_', '__')
                )

                self.ROOT_DIR_PATH: Path = Path(
                    # os.path.expanduser(path)
                    path
                )

                self.PROTO_DIR_PATH: Path = Path.joinpath(
                    self.ROOT_DIR_PATH,
                    "proto_schemas"
                )

                self.PROTO_FILE_PATH: Path = Path.joinpath(
                    self.PROTO_DIR_PATH,
                    self.API_NAME + ".proto"
                )

                self.OUT_DIR_PATH: Path = Path.joinpath(
                    self.ROOT_DIR_PATH,
                    "grpc_api"
                )

                self.TARGET_FILE_PATH: Path = Path.joinpath(
                    self.OUT_DIR_PATH,
                    f"{self.API_NAME}_pb2_grpc.py"
                )

                self.INVALID_LINE: str = (
                    f"import {self.API_NAME}_pb2 "
                    f"as {self.API_NAME_ALIAS}__pb2"
                )

                self.FIX_LINE: str = (
                    "from grpc_api "
                    f"import {self.API_NAME}_pb2 "
                    f"as {self.API_NAME_ALIAS}__pb2"
                )

                self.PATCH: list[str] = [
                    "sed",
                    "-i",
                    f"s/{self.INVALID_LINE}/{self.FIX_LINE}/",
                    f"{self.TARGET_FILE_PATH}"
                ]

                break


def run(project_name: str, echo: bool = False) -> bool:
    const = ConstantSet(project_name)

    check = (
        const.PROTO_FILE_PATH.exists(),
        const.PROTO_FILE_PATH.is_file(),
        const.PROTO_FILE_PATH.stat().st_size != 0
    )

    if not all(check):
        raise ValueError("Proto file does not exists or empty")
    else:
        protoc.main(
            [f"-I{os.getcwd()}",
             f"--proto_path={const.PROTO_DIR_PATH}",
             f"{const.PROTO_FILE_PATH}",
             f"--python_out={const.OUT_DIR_PATH}",
             f"--grpc_python_out={const.OUT_DIR_PATH}",
             f"--pyi_out={const.OUT_DIR_PATH}"]
        )

        subprocess.call(const.PATCH, shell=False)

        if echo:
            print("[ OK ]: Complete")
            print("[ Generated modules ]:",
                  f"\t- {const.API_NAME}_pb2.py",
                  f"\t- {const.API_NAME}_pb2_grpc.py",
                  sep='\n',
                  end='\n'*2)

        return True
