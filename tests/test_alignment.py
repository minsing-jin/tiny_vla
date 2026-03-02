from vla.core.clock import match_observation_to_action


def test_match_observation_to_action():
    obs_ts = [1.0, 1.1, 1.2]
    idx = match_observation_to_action(obs_ts, action_t=1.19, tolerance=0.2)
    assert idx == 1


def test_match_observation_to_action_drop():
    obs_ts = [1.0]
    idx = match_observation_to_action(obs_ts, action_t=2.0, tolerance=0.1)
    assert idx is None
