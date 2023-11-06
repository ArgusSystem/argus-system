import hdbscan


def fit(samples):
    clt = hdbscan.HDBSCAN()
    clt.fit(samples)
    return clt
