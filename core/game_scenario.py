PHRASES = {
    1957: "First Sputnik",
    1961: "Gagarin flew!",
    1969: "Armstrong got on the moon!",
    1971: "First orbital space station Salute-1",
    1981: "Flight of the Shuttle Columbia",
    1998: 'ISS start building',
    2011: 'Messenger launch to Mercury',
    2020: "Take the plasma gun! Shoot the garbage!",
}


def get_garbage_delay_tics(year):
    # Make garbage sparser across the timeline (bigger delay -> fewer spawns)
    if year < 1961:
        return None
    elif year < 1969:
        return 400
    elif year < 1981:
        return 320
    elif year < 1995:
        return 260
    elif year < 2010:
        return 200
    elif year < 2020:
        return 160
    else:
        return 120
