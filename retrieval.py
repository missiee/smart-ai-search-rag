import chromadb
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
collection = chromadb.PersistentClient(path='chroma_db').get_collection('docs')

_data = collection.get()
_ids = _data['ids']
_docs = _data['documents']
_metas = _data['metadatas']
bm25 = BM25Okapi([d.lower().split() for d in _docs])
lookup = {i: (d, m) for i, d, m in zip(_ids, _docs, _metas)}


def search_with_score(query, k=5):
    # vector search
    q_emb = model.encode([query]).tolist()
    v = collection.query(query_embeddings=q_emb, n_results=k * 2)
    vector_ids = v['ids'][0]
    top_sim = 1 - v['distances'][0][0]

    # keyword search
    scores = bm25.get_scores(query.lower().split())
    top = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k * 2]
    bm_ids = [_ids[i] for i in top]

    # dono ko mila do
    fused = {}
    for rank, id_ in enumerate(vector_ids):
        fused[id_] = fused.get(id_, 0) + 1 / (60 + rank)
    for rank, id_ in enumerate(bm_ids):
        fused[id_] = fused.get(id_, 0) + 1 / (60 + rank)

    best = sorted(fused, key=fused.get, reverse=True)[:k]
    hits = [{'id': i, 'text': lookup[i][0], 'source': lookup[i][1]['source']} for i in best]
    return hits, top_sim


def search(query, k=5):
    hits, _ = search_with_score(query, k)
    return hits
