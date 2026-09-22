from thermal_trigger import Detection, StableDetectionTrigger


def detection(frame, x=100, confidence=.9):
    return Detection(frame,"panel-1",confidence,x,80)


def test_stable_sequence_triggers_capture():
    trigger = StableDetectionTrigger(stable_frames=3)
    assert [trigger.update(detection(i,100+i)) for i in range(3)] == [False,False,True]


def test_low_confidence_resets_history():
    trigger = StableDetectionTrigger(stable_frames=2)
    trigger.update(detection(1))
    assert trigger.update(detection(2,confidence=.2)) is False
    assert trigger.update(detection(3)) is False


def test_large_motion_does_not_trigger():
    trigger = StableDetectionTrigger(stable_frames=2,max_motion_px=5)
    trigger.update(detection(1,10))
    assert trigger.update(detection(2,30)) is False

