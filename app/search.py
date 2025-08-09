import os

from whoosh.fields import ID, TEXT, Schema
from whoosh.index import create_in, open_dir
from whoosh.qparser import MultifieldParser

# Define schema
schema = Schema(id=ID(stored=True), body=TEXT)
# Ensure index directory exists
index_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "whoosh_index")
if not os.path.exists(index_dir):
    os.mkdir(index_dir)
# Create or open index
if not os.listdir(index_dir):
    ix = create_in(index_dir, schema)
else:
    ix = open_dir(index_dir)


def add_to_index(model, post):
    writer = ix.writer()
    writer.add_document(id=str(post.id), body=post.body)
    writer.commit()


def remove_from_index(model, post):
    writer = ix.writer()
    writer.delete_by_term("id", str(post.id))
    writer.commit()


def query_index(model, query, page, per_page):
    with ix.searcher() as searcher:
        parser = MultifieldParser(["body"], schema=ix.schema)
        myquery = parser.parse(query)
        results = searcher.search_page(myquery, page, pagelen=per_page)
        ids = [int(hit["id"]) for hit in results]
        total = results.total
    return ids, total
