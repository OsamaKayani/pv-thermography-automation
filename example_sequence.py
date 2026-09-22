from thermal_trigger import Detection, StableDetectionTrigger


def main() -> None:
    trigger = StableDetectionTrigger(stable_frames=3, max_motion_px=8, cooldown_frames=20)
    stream = [
        Detection(101, "panel-7", 0.91, 320, 181),
        Detection(102, "panel-7", 0.93, 322, 180),
        Detection(103, "panel-7", 0.92, 321, 183),
    ]
    for detection in stream:
        request = trigger.update(detection)
        print(f"frame={detection.frame_id} request={request}")


if __name__ == "__main__":
    main()
