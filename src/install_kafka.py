import tarfile
from io import BytesIO
from pathlib import Path
from shutil import copytree
from tarfile import TarInfo
from tempfile import TemporaryDirectory

import requests
from filelock import FileLock

from config import KAFKA_PATH


def remove_root_directory(member: TarInfo, _: str) -> TarInfo:
    parts = Path(member.path).parts[1:]
    path = Path(*parts)

    return member.replace(name=str(path))


def install_kafka(kafka_url: str, path: Path = KAFKA_PATH) -> None:
    with FileLock(path.with_suffix(".lock")):
        if path.exists():
            return

        response = requests.get(kafka_url)

        with (
            TemporaryDirectory() as temp_dir,
            tarfile.open(fileobj=BytesIO(response.content)) as file,
        ):
            file.extractall(
                path=temp_dir,
                filter=remove_root_directory,
            )
            copytree(temp_dir, path)


if __name__ == "__main__":
    install_kafka("https://dlcdn.apache.org/kafka/4.1.1/kafka_2.13-4.1.1.tgz")
