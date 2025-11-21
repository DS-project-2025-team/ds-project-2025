from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent

BINARY_DIR = ROOT_DIR / "bin"
BINARY_DIR.mkdir(exist_ok=True)

KAFKA_PATH = BINARY_DIR / "kafka"
