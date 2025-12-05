from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
SOURCE_DIR = ROOT_DIR / "src"

BINARY_DIR = ROOT_DIR / "bin"
BINARY_DIR.mkdir(exist_ok=True)

KAFKA_PATH = BINARY_DIR / "kafka"
KAFKA_CLUSTER_ID = "e54a5213-2e0f-49d6-8339-978aae554a11"

# Size of subintervals is 2 ** SUBINTERVAL_EXPONENT
SUBINTERVAL_EXPONENT = 16
