import pytest

from thermal_trigger import CaptureRequest, Detection, StableDetectionTrigger


def detection(frame: int, x: float = 100, confidence: float = 0.9) -> Detection:
    return Detection(frame, "panel-1", confidence, x, 80)


def test_stable_sequence_creates_capture_request():
    trigger = StableDetectionTrigger(stable_frames=3)
    results = [trigger.update(detection(i, 100 + i)) for i in range(3)]
    assert results[:2] == [None, None]
    assert isinstance(results[2], CaptureRequest)
    assert results[2].samples == 3


def test_low_confidence_resets_history():
    trigger = StableDetectionTrigger(stable_frames=2)
    trigger.update(detection(1))
    assert trigger.update(detection(2, confidence=0.2)) is None
    assert trigger.update(detection(3)) is None


def test_large_euclidean_motion_does_not_trigger():
    trigger = StableDetectionTrigger(stable_frames=2, max_motion_px=5)
    trigger.update(detection(1, 10))
    assert trigger.update(detection(2, 20)) is None


def test_cooldown_prevents_repeated_camera_requests():
    trigger = StableDetectionTrigger(stable_frames=2, cooldown_frames=10)
    assert trigger.update(detection(1)) is None
    assert trigger.update(detection(2)) is not None
    assert trigger.update(detection(3)) is None
    assert trigger.update(detection(4)) is None


def test_object_change_starts_a_new_sequence():
    trigger = StableDetectionTrigger(stable_frames=2)
    trigger.update(detection(1))
    other = Detection(2, "panel-2", 0.9, 100, 80)
    assert trigger.update(other) is None


def test_invalid_configuration_is_rejected():
    with pytest.raises(ValueError, match="at least 2"):
        StableDetectionTrigger(stable_frames=1)
