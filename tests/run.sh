#!/bin/bash
cd ..
docker build . -t flywheel/dicom-mr-classifier:2.0.0
docker run -it --entrypoint=/bin/bash -v $(pwd)/tests/T1w.dicom.zip:/flywheel/v0/input/dicom/T1w.dicom.zip -v $(pwd)/tests/config.json:/flywheel/v0/config.json flywheel/dicom-mr-classifier:2.0.0
