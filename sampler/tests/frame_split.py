from math import ceil


def split(frames, sampling_rate):
    in_between_frames = frames / sampling_rate
    offset = in_between_frames / 2

    result = [0] * sampling_rate
    for p in range(sampling_rate):
        result[p] = ceil(offset)
        offset += in_between_frames

    return result


def test_split():
    assert split(30, 1) == [15]
    assert split(30, 2) == [8, 23]
    assert split(30, 3) == [5, 15, 25]
    assert split(30, 4) == [4, 12, 19, 27]
    assert split(30, 5) == [3, 9, 15, 21, 27]
    assert split(30, 6) == [3, 8, 13, 18, 23, 28]
    assert split(30, 7) == [3, 7, 11, 15, 20, 24, 28]