import logging
import faiss
import numpy as np
from typing import List, Tuple
import pickle
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('vector_store.log'), logging.StreamHandler()]
)

class VectorStore:
    def __init__(self, vector_dim: int, index_path: str = "vector_index.faiss"):
        self.vector_dim = vector_dim
        self.index_path = index_path
        self.index = self._initialize_index()
        self.metadata_store = {}
        self.metadata_path = "metadata.pkl"
        self._load_metadata()
        logging.info(f"VectorStore initialized with dimension {self.vector_dim}.")

    def _initialize_index(self):
        if os.path.exists(self.index_path):
            logging.info(f"Loading existing FAISS index from {self.index_path}.")
            return faiss.read_index(self.index_path)
        else:
            logging.info("Creating new FAISS index.")
            return faiss.IndexFlatL2(self.vector_dim)

    def add_vectors(self, vectors: np.ndarray, metadata: List[dict]):
        if vectors.shape[1] != self.vector_dim:
            raise ValueError(f"Vector dimension mismatch. Expected {self.vector_dim}, got {vectors.shape[1]}.")
        
        logging.info(f"Adding {vectors.shape[0]} vectors to the FAISS index.")
        self.index.add(vectors)
        for i, meta in enumerate(metadata):
            self.metadata_store[len(self.metadata_store)] = meta
        self._save_index()
        self._save_metadata()
        logging.info("Vectors and metadata added successfully.")

    def search_vectors(self, query_vector: np.ndarray, top_k: int = 5) -> List[Tuple[int, float, dict]]:
        logging.info("Performing vector similarity search.")
        distances, indices = self.index.search(query_vector, top_k)
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx in self.metadata_store:
                results.append((idx, distance, self.metadata_store[idx]))
        logging.info(f"Search completed. Found {len(results)} results.")
        return results

    def _save_index(self):
        faiss.write_index(self.index, self.index_path)
        logging.info(f"FAISS index saved to {self.index_path}.")

    def _save_metadata(self):
        with open(self.metadata_path, 'wb') as f:
            pickle.dump(self.metadata_store, f)
        logging.info(f"Metadata saved to {self.metadata_path}.")

    def _load_metadata(self):
        if os.path.exists(self.metadata_path):
            with open(self.metadata_path, 'rb') as f:
                self.metadata_store = pickle.load(f)
            logging.info("Metadata loaded from file.")

if __name__ == "__main__":
    vector_store = VectorStore(vector_dim=128)

    # Example: Adding vectors
    sample_vectors = np.random.random((3, 128)).astype('float32')
    metadata = [
        {"id": 1, "text": "Elon Musk founded SpaceX."},
        {"id": 2, "text": "The moon is made of cheese."},
        {"id": 3, "text": "Water boils at 100°C."}
    ]
    vector_store.add_vectors(sample_vectors, metadata)

    # Example: Searching vectors
    query = np.random.random((1, 128)).astype('float32')
    results = vector_store.search_vectors(query, top_k=2)
    print(results)
