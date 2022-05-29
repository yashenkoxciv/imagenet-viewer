import numpy as np
from pymilvus import (
    connections,
    utility,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
)


class BasicCollection:
    def __init__(self, collection_name, features_dim, auto_id=True):
        fields = [
            FieldSchema(name='pk', dtype=DataType.INT64, is_primary=True, auto_id=auto_id),
            FieldSchema(name='features', dtype=DataType.FLOAT_VECTOR, dim=features_dim)
        ]
        schema = CollectionSchema(fields)
        # , consistency_level='Strong'
        self.collection = Collection(collection_name, schema)

    def insert_vectors(self, vectors):
        mutation_result = self.collection.insert([vectors])
        return mutation_result.primary_keys

    def insert_vectors_with_pk(self, pk, vectors):
        mutation_result = self.collection.insert([pk, vectors])
        return mutation_result.primary_keys

    def search(self, query_vectors, k):
        #collection.load()
        result = self.collection.search(query_vectors, 'features', {'metric_type': 'l2'}, limit=k)
        #collection.release()
        return result

    def get_vector(self, vector_id):
        #collection.load()
        result = self.collection.query(expr=f'pk in [{vector_id}]', output_fields=['features'], consistency_level='Strong')
        #collection.release()
        return result


class ImagesFeatures(BasicCollection):
    collection_name = 'images_features'
    def __init__(self):
        #super(UnrecognizedCollection, self).__init__('unrecognized_images', 2048)
        super().__init__(ImagesFeatures.collection_name, 2048)


class ImagesMatching(BasicCollection):
    collection_name = 'images_matching'
    def __init__(self):
        # TODO: add vector indexing
        #super(UnrecognizedCollection, self).__init__('unrecognized_images', 2048)
        super().__init__(ImagesMatching.collection_name, 2048, auto_id=False)

