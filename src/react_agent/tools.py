import requests
from react_agent.models import LiteraturePlan
from tenacity import retry, stop_after_attempt, wait_fixed


def _reconstruct_abstract(inverted_index: dict) -> str:
    if not inverted_index:
        return ""
    position_map = {}
    for word, positions in inverted_index.items():
        for pos in positions:
            position_map[pos] = word
    return " ".join(word for _, word in sorted(position_map.items()))


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def fetch_papers_openalex(plan: LiteraturePlan) -> list[dict]:
    url = "https://api.openalex.org/works"
    search_query = " ".join(plan.keywords)

    params = {
        "filter": f"title.search:{search_query},publication_year:>{plan.min_year}",
        "per_page": 5,
        "sort": "cited_by_count:desc"
    }

    full_url = requests.Request("GET", url, params=params).prepare().url
    print("OpenAlex URL:", full_url)

    resp = requests.get(
        url,
        params=params,
        headers={"User-Agent": "your-email@example.com"},  # Replace with your actual email
        timeout=10
    )
    resp.raise_for_status()
    data = resp.json()

    results = []
    for item in data.get("results", []):
        abstract_raw = item.get("abstract_inverted_index")
        abstract = _reconstruct_abstract(abstract_raw) if abstract_raw else "No abstract available"

        authorships = item.get("authorships", [])
        authors = [a["author"]["display_name"] for a in authorships if "author" in a]

        paper_info = {
            "title": item.get("title", "Untitled"),
            "authors": authors,
            "abstract": abstract,
            "year": item.get("publication_year"),
            "doi": item.get("doi"),
            "url": item.get("id")
        }
        results.append(paper_info)

    # Optional debug print
    print("\n🔎 Retrieved Papers:")
    for p in results:
        print(f"- {p['title']} ({p['year']})")
        print(f"  Authors: {', '.join(p['authors'])}")
        print(f"  Abstract: {p['abstract'][:200]}...\n")

    return results


def fetch_author_stats(plan: LiteraturePlan) -> dict:
    # Simula estadísticas de autores para testing
    return {
        "note": "Mocked author stats based on keywords",
        "top_authors": [
            {"name": "John Preskill", "h_index": 95},
            {"name": "Michelle Simmons", "h_index": 78}
        ]
    }
