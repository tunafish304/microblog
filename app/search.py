from flask import current_app

# from elastic_transport import ConnectionTimeout


# def add_to_index(index, model):
# if not current_app.elasticsearch:
#    return
# payload = {}
# for field in model.__searchable__:
#    payload[field] = getattr(model, field)
# current_app.elasticsearch.index(index=index, id=model.id, document=payload)


def add_to_index(index, model):
    es = current_app.elasticsearch
    if not es:
        return
    try:
        if not es.ping():  # Make a lightweight test connection
            current_app.logger.warning(
                "Elasticsearch client exists but is unreachable."
            )
            return
        payload = {field: getattr(model, field) for field in model.__searchable__}
        es.index(index=index, id=model.id, document=payload)
    except Exception as e:
        current_app.logger.error(f"Search indexing failed: {e}")


def remove_from_index(index, model):
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, id=model.id)


def query_index(index, query, page, per_page):
    if not current_app.elasticsearch:
        return [], 0
    search = current_app.elasticsearch.search(
        index=index,
        query={"multi_match": {"query": query, "fields": ["*"]}},
        from_=(page - 1) * per_page,
        size=per_page,
    )
    ids = [int(hit["_id"]) for hit in search["hits"]["hits"]]
    return ids, search["hits"]["total"]["value"]
