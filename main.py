"""Terminal entry point for the local USCityURL municipal RAG assistant."""

import argparse

from filelock import FileLock, Timeout

from rag import (
    DEFAULT_EMBED_MODEL,
    DEFAULT_LLM_MODEL,
    add_keyword_to_settings,
    add_place_to_settings,
    answer_question,
    open_vector_store,
    rebuild_database_if_needed,
    resolve_scope,
    verify_database_ready,
    verify_ollama_model,
)
from setting import MAIN_LOCK_FILE, PERSISTENT_DIR


def main() -> None:
    """Verify the notebook-built database, then answer scoped questions."""
    parser = argparse.ArgumentParser(description="Local USCityURL municipal RAG assistant")
    parser.add_argument(
        "--update",
        action="store_true",
        help="add missing INDEX_PLACES and keyword coverage before starting chat",
    )
    parser.add_argument(
        "--add-place", "--place",
        dest="places",
        action="append",
        default=[],
        metavar="PLACE",
        help="append a state or municipality to INDEX_PLACES and update Chroma",
    )
    parser.add_argument(
        "--add-keyword", "--keyword",
        dest="keywords",
        action="append",
        default=[],
        metavar="KEYWORD",
        help="append a crawl keyword to KEYWORDS and update Chroma",
    )
    args = parser.parse_args()

    verify_ollama_model(DEFAULT_EMBED_MODEL)
    should_update = args.update
    for place in args.places:
        try:
            added = add_place_to_settings(place)
            should_update = True
            print(f"{'Added' if added else 'Already present'}: {place}")
        except ValueError:
            print(
                f"Could not add {place}: it does not exist in the pipeline CSV. "
                "Continuing to question mode."
            )
    for keyword in args.keywords:
        try:
            added = add_keyword_to_settings(keyword)
            should_update = True
            print(f"{'Added keyword' if added else 'Keyword already present'}: {keyword}")
        except ValueError as error:
            print(f"Could not add keyword: {error}. Continuing to question mode.")

    # --update synchronizes missing place/keyword pairs. The add flags first
    # persist their values in setting.py, then perform the same additive update.
    if should_update:
        rebuild_database_if_needed(DEFAULT_EMBED_MODEL)
    else:
        verify_database_ready(DEFAULT_EMBED_MODEL)
    verify_ollama_model(DEFAULT_LLM_MODEL)
    vector_store = open_vector_store(DEFAULT_EMBED_MODEL)

    print("Persistent database is current. Ask a question, or type 'exit'.")

    while True:
        question = input("\nQuestion: ").strip()
        if question.casefold() in {"exit", "quit"}:
            break
        if not question:
            continue

        try:
            cities, scope_label, missing_context = resolve_scope(question)
        except ValueError as error:
            print(f"Cannot answer: {error}")
            continue
        for place in missing_context:
            print(f"No context available for {place}; skipping it.")
        print(f"Geographic scope: {scope_label} ({len(cities):,} municipalities)")
        answer, sources = answer_question(
            vector_store,
            cities,
            scope_label,
            question,
            llm_model=DEFAULT_LLM_MODEL,
        )
        print(f"\nAnswer:\n{answer}")
        if sources:
            print("\nRetrieved sources:")
            for url in sources:
                print(f"- {url}")


if __name__ == "__main__":
    # Keep one interactive process in control of the local models and database.
    # The operating-system lock is released automatically on exit or Ctrl-C.
    PERSISTENT_DIR.mkdir(parents=True, exist_ok=True)
    try:
        with FileLock(str(MAIN_LOCK_FILE), timeout=0):
            main()
    except Timeout:
        raise SystemExit(
            "Another main.py session is already running. Exit that session first."
        ) from None
