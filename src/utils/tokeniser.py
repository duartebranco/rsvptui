def simple_tokenise(text: str) -> list[str]:
    return [word for word in text.split() if word]
