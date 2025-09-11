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
    """Spawn interval in ticks (TIC_TIMEOUT ~= 0.012). Lower = more often."""
    if year < 1961:
        return 180
    elif year < 1969:
        return 140
    elif year < 1981:
        return 120
    elif year < 1995:
        return 100
    elif year < 2010:
        return 80
    elif year < 2020:
        return 65
    else:
        return 55
