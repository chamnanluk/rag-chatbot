def unique_sources(sources: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for src in sources:
        if src not in seen:
            seen.add(src)
            ordered.append(src)
    return ordered
