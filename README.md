# PV Thermography Automation

A hardware-independent trigger state machine for coordinating RGB detections with thermal-image capture. Capture occurs only after the same object remains confident and spatially stable across several frames.

```bash
python -m pip install -r requirements.txt
pytest -q
```

This original demonstration reflects the system-design lessons of an automated thermographic camera-control thesis. The thesis achieved approximately 92.4% mAP@0.5 on its reported Dataset B, but no Fraunhofer data, trained weights, source code, camera credentials or proprietary assets are published here.

