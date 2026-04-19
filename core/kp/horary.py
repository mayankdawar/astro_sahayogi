"""KP horary number <-> ascendant degree mapping (1-2193)."""
from astro_sahayogi.data.constants import YRS


def get_horary_ascendant(number: int) -> float:
    """Map a horary number (1-2193) to its ascendant longitude in degrees."""
    num = int(number)
    if num < 1 or num > 2193:
        raise ValueError(f"Horary number must be 1-2193, got {num}")

    curr_sec = 0.0
    curr_idx = 1

    for star in range(27):
        star_lord = star % 9
        for sub in range(9):
            sub_lord = (star_lord + sub) % 9
            for ssub in range(9):
                ssub_lord = (sub_lord + ssub) % 9
                span_sec = (YRS[sub_lord] * YRS[ssub_lord] * 400.0) / 120.0
                next_sec = curr_sec + span_sec
                boundary = (int(curr_sec + 0.1) // 108000 + 1) * 108000

                if curr_sec < boundary and next_sec > boundary + 0.1:
                    if curr_idx == num:
                        return (curr_sec / 3600.0) + 1e-5
                    curr_idx += 1
                    if curr_idx == num:
                        return (boundary / 3600.0) + 1e-5
                    curr_idx += 1
                else:
                    if curr_idx == num:
                        return (curr_sec / 3600.0) + 1e-5
                    curr_idx += 1
                curr_sec = next_sec
    return 0.0


def get_horary_number(deg: float) -> int:
    """Map a sidereal longitude (degrees) back to its horary number (1-2193)."""
    d = int(deg)
    remainder = (deg - d) * 60
    m = int(remainder)
    s = (remainder - m) * 60
    return get_number_from_dms(float(d), float(m), s)


def get_number_from_dms(d: float, m: float, s: float) -> int:
    """Map a degree/min/sec position to the matching horary number."""
    target_sec = d * 3600.0 + m * 60.0 + s
    if target_sec < 0 or target_sec >= 1296000:
        return 0

    curr_sec = 0.0
    curr_idx = 1

    for star in range(27):
        star_lord = star % 9
        for sub in range(9):
            sub_lord = (star_lord + sub) % 9
            for ssub in range(9):
                ssub_lord = (sub_lord + ssub) % 9
                span_sec = (YRS[sub_lord] * YRS[ssub_lord] * 400.0) / 120.0
                next_sec = curr_sec + span_sec
                boundary = (int(curr_sec + 0.1) // 108000 + 1) * 108000

                if curr_sec < boundary and next_sec > boundary + 0.1:
                    if curr_sec <= target_sec < boundary:
                        return curr_idx
                    curr_idx += 1
                    if boundary <= target_sec < next_sec:
                        return curr_idx
                    curr_idx += 1
                else:
                    if curr_sec <= target_sec < next_sec:
                        return curr_idx
                    curr_idx += 1
                curr_sec = next_sec
    return 2193
