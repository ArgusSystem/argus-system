from math import ceil


def split(frames, framerate, sampling_rate):
    in_between_frames = framerate / sampling_rate
    offset = in_between_frames / 2

    # samples = round(sampling_rate * frames / framerate)
    # result = [0] * samples
    # for p in range(samples):
    #     result[p] = ceil(offset)
    #     offset += in_between_frames

    result = []

    while offset <= frames:
        result.append(ceil(offset))
        offset += in_between_frames

    return result


def test_split():
    assert split(30, 30, 1) == [15]
    assert split(30, 30, 2) == [8, 23]
    assert split(30, 30, 3) == [5, 15, 25]
    assert split(30, 30, 4) == [4, 12, 19, 27]
    assert split(30, 30, 5) == [3, 9, 15, 21, 27]
    assert split(30, 30, 6) == [3, 8, 13, 18, 23, 28]
    assert split(30, 30, 7) == [3, 7, 11, 15, 20, 24, 28]

    assert split(30, 25, 5) == [3, 8, 13, 18, 23, 28]
    assert split(30, 26, 5) == [3, 8, 13, 19, 24, 29]
    assert split(30, 27, 5) == [3, 9, 14, 19, 25, 30]
    assert split(30, 28, 5) == [3, 9, 14, 20, 26]
    assert split(30, 29, 5) == [3, 9, 15, 21, 27]

