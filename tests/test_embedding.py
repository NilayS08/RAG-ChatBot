# import sys
# from pathlib import Path

# # Add parent directory to path
# sys.path.insert(0, str(Path(__file__).parent.parent))

from src.embeddings import get_embedding_model

def test_embedding_shape():
    model = get_embedding_model()
    vec = model.embed_query('test sentence')
    assert len(vec) == 384, 'BGE-small should produce 384-dim vectors'
def test_embedding_similarity():
    model = get_embedding_model()
    v1 = model.embed_query('leave policy India')
    v2 = model.embed_query('vacation days employees India')
    v3 = model.embed_query('quarterly earnings report')
    # v1 and v2 should be more similar to each other than to v3
    from numpy import dot
    from numpy.linalg import norm
    sim12 = dot(v1, v2) / (norm(v1) * norm(v2))
    sim13 = dot(v1, v3) / (norm(v1) * norm(v3))
    assert sim12 > sim13, 'Similar topics should have higher cosine similarity'