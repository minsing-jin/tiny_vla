from vla.core.types import Command, Status, AtomicAction, Observation


def test_command_roundtrip():
    cmd = Command(cmd_id="1", skill="CLICK_UI")
    data = cmd.to_dict()
    rebuilt = Command.from_dict(data)
    assert rebuilt.cmd_id == "1"
    assert rebuilt.skill == "CLICK_UI"


def test_status_roundtrip():
    s = Status(cmd_id="x", status="SUCCESS", info={"attempts": 1})
    rebuilt = Status.from_dict(s.to_dict())
    assert rebuilt.status == "SUCCESS"
    assert rebuilt.info["attempts"] == 1


def test_atomic_action_roundtrip():
    a = AtomicAction(t=1.0, type="CLICK", x=10, y=20, button="LEFT")
    rebuilt = AtomicAction.from_dict(a.to_dict())
    assert rebuilt.type == "CLICK"
    assert rebuilt.button == "LEFT"


def test_observation_roundtrip():
    o = Observation(t=1.0, frame_path="f.png", cursor=[1, 2], window={"w": 100})
    rebuilt = Observation.from_dict(o.to_dict())
    assert rebuilt.frame_path == "f.png"
