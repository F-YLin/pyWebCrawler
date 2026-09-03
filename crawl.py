from urllib.parse import urlsplit


def normalize_url(input_url: str) -> str:
    parsed_url = urlsplit(input_url)

    netloc = parsed_url.netloc
    path = parsed_url.path.rstrip('/')

    output_url = f"{netloc}{path}"

    output_url = output_url.lower()

    return output_url
