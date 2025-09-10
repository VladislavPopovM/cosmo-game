from entities.obstacles import has_collision


def test_no_collision_when_far():
    assert not has_collision((0, 0), (1, 1), (5, 5), (1, 1))


def test_collision_when_overlap():
    assert has_collision((0, 0), (2, 2), (1, 1), (2, 2))
