from collections import defaultdict

from app.config import Config


def reciprocal_rank_fusion(
    result_lists: list[list[dict]],
    k: int | None = None,
    top_k: int | None = None,
) -> list[dict]:

    if k is None:
        k = Config.RRF_K

    if top_k is None:
        top_k = Config.TOP_K

    scores = defaultdict(float)
    documents = {}

    for results in result_lists:

        for rank, result in enumerate(
            results,
            start=1,
        ):
            chunk_id = result["chunk_id"]

            scores[chunk_id] += (
                1 / (k + rank)
            )

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