from utils.orm.src.models import UnknownCluster, UnknownFace


class ClusterStorage:

    def __init__(self, skip_outliers):
        self.clusters = {}
        self.skip_outliers = skip_outliers

    def store(self, face_id, label):
        is_outlier = label < 0

        if self.skip_outliers and is_outlier:
            return

        if label not in self.clusters:
            self.clusters[label] = UnknownCluster(outliers=is_outlier).save()

        UnknownFace(cluster_id=self.clusters[label], face_id=face_id).save()
