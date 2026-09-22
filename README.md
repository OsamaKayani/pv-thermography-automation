# PV Thermography Automation

A hardware-independent state machine for coordinating RGB detections with thermal-image capture. A request is emitted only after the same tracked object remains confident and spatially stable across several increasing frame IDs. Per-object cooldown prevents the camera from receiving a new request on every subsequent frame.

```bash
python -m pip install -e ".[dev]"
python example_sequence.py
pytest -q
```

## Boundary of this demo

The state machine accepts tracker output and returns a typed `CaptureRequest`; it does not pretend to be a camera SDK. A production adapter would translate that request into a vendor-specific command, attach timestamps, retry transient transport failures, and persist capture acknowledgements.

This original demonstration reflects the system-design lessons of an automated thermographic camera-control thesis. The thesis achieved approximately 92.4% mAP@0.5 on its reported Dataset B, but no Fraunhofer data, trained weights, source code, camera credentials, or proprietary assets are published here.
