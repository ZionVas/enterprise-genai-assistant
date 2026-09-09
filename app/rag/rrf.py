from collections import defaultdict


def reciprocal_rank_fusion(
    result_lists: list[list[dict]],
    k: int = 60,
    top_k: int = 5,
) -> list[dict]:

    scores = defaultdict(float)
    documents = {}

    for results in result_lists:

        for rank, result in enumerate(results, start=1):

            chunk_id = result["chunk_id"]

            scores[chunk_id] += 1 / (k + rank)

            if chunk_id not in documents:
                documents[chunk_id] = result

    ranked_chunk_ids = sorted(
        scores,
        key=scores.get,
        reverse=True,
    )

    fused_results = []

    for chunk_id in ranked_chunk_ids[:top_k]:

        result = documents[chunk_id].copy()

        result["rrf_score"] = scores[chunk_id]

        fused_results.append(result)

    return fused_results