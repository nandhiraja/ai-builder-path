import gzip
import html
import ipaddress
import json
import re
import socket
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

MAX_RESPONSE_BYTES = 1_500_000
MAX_TEXT_CHARS = 6_000
TIMEOUT_SECONDS = 10
MAX_REDIRECTS = 5

USER_AGENT = "BedrockWebCrawlerAgent/1.0 (educational-project)"


class HtmlTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag.lower() in {"script", "style", "noscript", "svg", "iframe"}:
            self.skip_depth += 1

    def handle_endtag(self, tag):
        if tag.lower() in {"script", "style", "noscript", "svg", "iframe"}:
            self.skip_depth = max(0, self.skip_depth - 1)

    def handle_data(self, data):
        if self.skip_depth == 0:
            self.text_parts.append(data)

    def get_clean_text(self):
        text = html.unescape(" ".join(self.text_parts))
        return re.sub(r"\s+", " ", text).strip()


def is_public_ip(ip_address):
    ip = ipaddress.ip_address(ip_address)

    return not (
        ip.is_private
        or ip.is_loopback
        or ip.is_link_local
        or ip.is_multicast
        or ip.is_reserved
        or ip.is_unspecified
    )


def validate_url(url):
    parsed_url = urllib.parse.urlparse(url)

    if parsed_url.scheme not in {"http", "https"}:
        raise ValueError("Only HTTP and HTTPS URLs are allowed.")

    if not parsed_url.hostname:
        raise ValueError("A valid website hostname is required.")

    if parsed_url.port not in {None, 80, 443}:
        raise ValueError("Only ports 80 and 443 are allowed.")

    hostname = parsed_url.hostname.lower()

    blocked_hosts = {
        "localhost",
        "metadata.google.internal",
        "169.254.169.254"
    }

    if hostname in blocked_hosts:
        raise ValueError("This URL is not allowed for security reasons.")

    try:
        resolved_addresses = socket.getaddrinfo(hostname, None)

        for address in resolved_addresses:
            ip_value = address[4][0]

            if not is_public_ip(ip_value):
                raise ValueError(
                    "Private, local, or unsafe IP addresses are not allowed."
                )

    except socket.gaierror:
        raise ValueError("The hostname could not be resolved.")


class LimitedRedirectHandler(urllib.request.HTTPRedirectHandler):
    def __init__(self):
        super().__init__()
        self.redirect_count = 0

    def redirect_request(self, request, file_pointer, code, message, headers, new_url):
        self.redirect_count += 1

        if self.redirect_count > MAX_REDIRECTS:
            raise urllib.error.HTTPError(
                new_url,
                code,
                "Too many redirects.",
                headers,
                file_pointer
            )

        validate_url(new_url)

        return super().redirect_request(
            request,
            file_pointer,
            code,
            message,
            headers,
            new_url
        )


def get_page_html(url):
    validate_url(url)

    redirect_handler = LimitedRedirectHandler()
    opener = urllib.request.build_opener(redirect_handler)

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Encoding": "gzip"
        }
    )

    with opener.open(request, timeout=TIMEOUT_SECONDS) as response:
        content_type = response.headers.get("Content-Type", "").lower()

        if "text/html" not in content_type and "application/xhtml+xml" not in content_type:
            raise ValueError("The URL did not return an HTML webpage.")

        content = response.read(MAX_RESPONSE_BYTES + 1)

        if len(content) > MAX_RESPONSE_BYTES:
            raise ValueError("The webpage is too large to crawl.")

        content_encoding = response.headers.get("Content-Encoding", "").lower()

        if content_encoding == "gzip":
            content = gzip.decompress(content)

        charset = response.headers.get_content_charset() or "utf-8"
        page_html = content.decode(charset, errors="replace")

        return {
            "final_url": response.geturl(),
            "status_code": response.status,
            "html": page_html
        }


def scrape_website(url):
    webpage = get_page_html(url)

    extractor = HtmlTextExtractor()
    extractor.feed(webpage["html"])

    extracted_text = extractor.get_clean_text()

    if not extracted_text:
        raise ValueError("No readable text was found on this webpage.")

    is_truncated = len(extracted_text) > MAX_TEXT_CHARS

    return {
        "url": webpage["final_url"],
        "status_code": webpage["status_code"],
        "text": extracted_text[:MAX_TEXT_CHARS],
        "truncated": is_truncated
    }


def extract_url_from_event(event):
    parameters = event.get("parameters", [])

    for parameter in parameters:
        if parameter.get("name") == "url":
            return parameter.get("value")

    raise ValueError("The required URL parameter was not received.")


def build_bedrock_response(event, status_code, body):
    return {
        "messageVersion": "1.0",
        "response": {
            "actionGroup": event.get("actionGroup", "WebScrapeActionGroup"),
            "apiPath": event.get("apiPath", "/scrape"),
            "httpMethod": event.get("httpMethod", "POST"),
            "httpStatusCode": status_code,
            "responseBody": {
                "application/json": {
                    "body": json.dumps(body)
                }
            }
        }
    }


def lambda_handler(event, context):
    try:
        url = extract_url_from_event(event)
        result = scrape_website(url)

        response_body = {
            "success": True,
            "message": "Webpage scraped successfully.",
            **result
        }

        return build_bedrock_response(event, 200, response_body)

    except urllib.error.HTTPError as error:
        return build_bedrock_response(
            event,
            400,
            {
                "success": False,
                "message": f"Website returned HTTP error {error.code}: {error.reason}"
            }
        )

    except urllib.error.URLError as error:
        return build_bedrock_response(
            event,
            400,
            {
                "success": False,
                "message": f"Could not reach the website: {error.reason}"
            }
        )

    except Exception as error:
        return build_bedrock_response(
            event,
            400,
            {
                "success": False,
                "message": str(error)
            }
        )