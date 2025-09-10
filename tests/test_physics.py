from core.physics import update_speed


def test_update_speed_accelerates():
    row_speed, col_speed = update_speed(0, 0, 1, 0, row_speed_limit=2, column_speed_limit=2, fading=1)
    assert row_speed > 0
    assert col_speed == 0


def test_update_speed_brakes():
    row_speed, col_speed = update_speed(1, 0, -1, 0, row_speed_limit=2, column_speed_limit=2)
    assert row_speed < 1
    assert col_speed == 0
