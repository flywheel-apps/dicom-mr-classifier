#!/usr/local/bin/python
import datetime
import logging
import os
import shutil
import sys
import time
from pathlib import Path

import tzlocal
from flywheel_gear_toolkit import GearToolkitContext

from dicom_mr_classifier import dicom_classify, validate_timezone

log = logging.getLogger(__name__)


def handle_config(conf):
    if "timezone" in conf:
        tz = conf.get("timezone")
        os.environ["TZ"] = tz
        time.tzset()
    return conf.get("timezone"), conf.get("force")


def handle_inputs(gc):
    dcm_path = Path(gc.get_input_path("dicom"))
    if not (dcm_path.exists() and dcm_path.is_file()):
        log.error("Input doesn't exist, exiting")
        sys.exit(1)
    return dcm_path


def handle_dicom_mr(in_file, out_dir, gc):
    timezone = validate_timezone(tzlocal.get_localzone())

    metadatafile = dicom_classify(in_file, out_dir, timezone, gc.config_json)

    metadata_path = Path(metadatafile)

    if metadata_path.exists() and metadata_path.is_file():
        log.info(f"Generated {metadatafile}")
        return metadata_path
    else:
        log.error("Metadata file not generated")
        return None


if __name__ == "__main__":
    with GearToolkitContext() as gc:
        gc.init_logging()
        log.info(f"start: f{datetime.datetime.utcnow()}")

        tz, force = handle_config(gc.config)

        in_dicom = handle_inputs(gc)

        out = handle_dicom_mr(str(in_dicom), gc.output_dir, gc)

        if out:
            log.info("Success")
            log.info(f"stop: f{datetime.datetime.utcnow()}")
        else:
            log.error("Failure")
            log.info(f"stop: f{datetime.datetime.utcnow()}")
