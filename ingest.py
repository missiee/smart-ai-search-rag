import os
import glob
import chromadb
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

DOCS_DIR = 'docs'
DB_DIR = 'chroma_db'

model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.PersistentClient(path=DB_DIR)
collection = client.get_or_create_collection('docs', metadata={'hnsw:space': 'cosine'})


def read_file(path):
    if path.endswith('.pdf'):
        reader = PdfReader(path)
        return '\n'.join((p.extract_text() or '') for p in reader.pages)
    with open(path, encoding='utf-8') as f:
        return f.read()


def chunk_text(text, size=800, overlap=150):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + size])
        start += size - overlap
    return chunks


ids, texts, metas = [], [], []
for path in glob.glob(DOCS_DIR + '/**/*', recursive=True):
    if not path.endswith(('.txt', '.md', '.pdf')):
        continue
    text = read_file(path)
    for i, chunk in enumerate(chunk_text(text)):
        if chunk.strip():
            ids.append(path + '-' + str(i))
            texts.append(chunk)
            metas.append({'source': os.path.basename(path), 'chunk': i})

if not texts:
    print('docs folder mein koi file nahi mili')
else:
    embeddings = model.encode(texts, show_progress_bar=True).tolist()
    collection.upsert(ids=ids, documents=texts, embeddings=embeddings, metadatas=metas)
    print('Done:', len(texts), 'chunks stored')