from enum import Enum
from PIL import Image as PilImage
from urllib.request import urlopen
from mongoengine import (
    Document,
    LongField,
    StringField,
    ReferenceField,
    FloatField,
    EmbeddedDocument,
    EmbeddedDocumentListField,
    EnumField
)


class Neighbor(EmbeddedDocument):
    matched_image = ReferenceField('Image', required=True)
    distance = FloatField(required=True)

    def __str__(self):
        return f'<Neighbor: {self.matched_image} {self.distance}>'

    def __repr__(self):
        return str(self)


class ImageStatus(Enum):
    PENDING_CLASSIFICATION = 'PENDING_CLASSIFICATION'
    CLASSIFIED = 'CLASSIFIED'
    PENDING_ENCODING = 'PENDING_ENCODING'
    PENDING_MATCHING = 'PENDING_MATCHING'
    PENDING_CLUSTERING = 'PENDING_CLUSTERING'
    CLUSTERIZED = 'CLUSTERIZED'


class Image(Document):
    # label is assigned by classifier
    label = StringField()

    # URL to get image file
    url = StringField(required=True)

    # Milvus's vector id (int64)
    vector_id = LongField()

    cluster_id = StringField()
    clustering_request_id = StringField()

    neighbors = EmbeddedDocumentListField(Neighbor)

    status = EnumField(ImageStatus, default=ImageStatus.PENDING_CLASSIFICATION)

    def get_pil_image(self):
        image = PilImage.open(urlopen(self.url))
        return image

    def to_dict(self):
        image_dict = {
            'id': self.id,
            'status': self.status,
            'label': self.label,
            'cluster_id': self.cluster_id,
            'url': self.url
        }
        return image_dict

    def __str__(self):
        s = f'<Image: {self.id} {self.status} label={self.label} vid={self.vector_id} cid={self.cluster_id} neighbors({len(self.neighbors)})>'
        return s

    def __repr__(self):
        return str(self)

