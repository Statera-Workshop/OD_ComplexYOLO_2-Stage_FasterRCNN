"""Evaluate complex faster_rcnn on the KITTI test split only."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common.runner import main
from detectors.faster_rcnn.build import build_model

if __name__ == "__main__":
    main("evaluate", task="complex", version="faster_rcnn", build_model=build_model)
