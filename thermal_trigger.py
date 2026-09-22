from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from math import hypot, isfinite


@dataclass(frozen=True)
class Detection:
    frame_id: int
    object_id: str
    confidence: float
    center_x: float
    center_y: float

    def __post_init__(self) -> None:
        if self.frame_id < 0:
            raise ValueError("frame_id cannot be negative")
        if not self.object_id.strip():
            raise ValueError("object_id cannot be empty")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        if not isfinite(self.center_x) or not isfinite(self.center_y):
            raise ValueError("detection center must be finite")


@dataclass(frozen=True)
class CaptureRequest:
    frame_id: int
    object_id: str
    mean_x: float
    mean_y: float
    samples: int


class StableDetectionTrigger:
    """Create one capture request after a stable RGB detection sequence."""

    def __init__(
        self,
        minimum_confidence: float = 0.7,
        stable_frames: int = 3,
        max_motion_px: float = 12,
        cooldown_frames: int = 20,
    ) -> None:
        if not 0.0 <= minimum_confidence <= 1.0:
            raise ValueError("minimum confidence must be between 0 and 1")
        if stable_frames < 2:
            raise ValueError("stable_frames must be at least 2")
        if max_motion_px < 0 or cooldown_frames < 0:
            raise ValueError("motion and cooldown limits cannot be negative")
        self.minimum_confidence = minimum_confidence
        self.stable_frames = stable_frames
        self.max_motion_px = max_motion_px
        self.cooldown_frames = cooldown_frames
        self.history: deque[Detection] = deque(maxlen=stable_frames)
        self.last_capture_frame: dict[str, int] = {}

    def update(self, detection: Detection | None) -> CaptureRequest | None:
        if detection is None or detection.confidence < self.minimum_confidence:
            self.history.clear()
            return None
        if self.history and (
            detection.object_id != self.history[-1].object_id
            or detection.frame_id <= self.history[-1].frame_id
        ):
            self.history.clear()
        self.history.append(detection)
        if len(self.history) < self.stable_frames:
            return None

        origin = self.history[0]
        if any(
            hypot(item.center_x - origin.center_x, item.center_y - origin.center_y)
            > self.max_motion_px
            for item in self.history
        ):
            return None

        last_frame = self.last_capture_frame.get(detection.object_id)
        if last_frame is not None and detection.frame_id - last_frame <= self.cooldown_frames:
            return None
        self.last_capture_frame[detection.object_id] = detection.frame_id
        return CaptureRequest(
            frame_id=detection.frame_id,
            object_id=detection.object_id,
            mean_x=sum(item.center_x for item in self.history) / len(self.history),
            mean_y=sum(item.center_y for item in self.history) / len(self.history),
            samples=len(self.history),
        )
