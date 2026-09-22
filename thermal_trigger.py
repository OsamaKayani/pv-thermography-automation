from collections import deque
from dataclasses import dataclass


@dataclass(frozen=True)
class Detection:
    frame_id: int
    object_id: str
    confidence: float
    center_x: float
    center_y: float


class StableDetectionTrigger:
    """Trigger thermal capture only after a stable RGB detection sequence."""

    def __init__(self, minimum_confidence=.7, stable_frames=3, max_motion_px=12):
        self.minimum_confidence = minimum_confidence
        self.stable_frames = stable_frames
        self.max_motion_px = max_motion_px
        self.history = deque(maxlen=stable_frames)

    def update(self, detection: Detection | None) -> bool:
        if detection is None or detection.confidence < self.minimum_confidence:
            self.history.clear()
            return False
        if self.history and detection.object_id != self.history[-1].object_id:
            self.history.clear()
        self.history.append(detection)
        if len(self.history) < self.stable_frames:
            return False
        origin = self.history[0]
        return all(abs(item.center_x-origin.center_x) <= self.max_motion_px and abs(item.center_y-origin.center_y) <= self.max_motion_px for item in self.history)

