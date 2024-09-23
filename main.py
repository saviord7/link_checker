# Link Method Checker

import asyncio
import aiohttp
import pytest
import json


async def check_link_methods(link):
    methods = ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH"]
    available_methods = {}

    async with aiohttp.ClientSession() as session:
        for method in methods:
            try:
                async with session.request(method, link) as response:
                    available_methods[method] = response.status
            except Exception:
                available_methods[method] = "Error"

    return available_methods


def process_input(input_strings):
    results = {}
    for line in input_strings:
        line = line.strip()
        if line.startswith("http://") or line.startswith("https://"):
            results[line] = asyncio.run(check_link_methods(line))
        else:
            results[line] = f'The line "{line}" is not a link.'
    return results


# Tests


@pytest.mark.asyncio
async def test_check_link_methods():
    link = "http://google.com"
    result = await check_link_methods(link)
    assert "GET" in result
    assert "POST" in result
    assert "PUT" in result
    assert "DELETE" in result


def test_process_input():
    input_strings = [
        "http://google.com",
        "Not a link",
        "https://spb.hh.ru/",
        "https://www.yandex.ru",
        "https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0",
        "https://www.rbc.ru",
        "https://www.mail.ru",
        "https://www.ria.ru",
        "https://www.tass.ru",
        "https://www.kommersant.ru",
        "https://www.gazeta.ru",
        "https://www.lenta.ru",
        "https://www.fontanka.ru",
        "https://www.newsru.com",
    ]
    result = process_input(input_strings)
    assert isinstance(result, dict)
    assert result["http://google.com"] is not None
    assert result["Not a link"] == 'The line "Not a link" is not a link.'
    assert result["https://spb.hh.ru/"] is not None
    assert result["https://www.yandex.ru"] is not None
    assert (
        result[
            "https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0"
        ]
        is not None
    )
    assert result["https://www.rbc.ru"] is not None
    assert result["https://www.mail.ru"] is not None
    assert result["https://www.ria.ru"] is not None
    assert result["https://www.tass.ru"] is not None
    assert result["https://www.kommersant.ru"] is not None
    assert result["https://www.gazeta.ru"] is not None
    assert result["https://www.lenta.ru"] is not None
    assert result["https://www.fontanka.ru"] is not None
    assert result["https://www.newsru.com"] is not None
    with open("links.json", "w") as fp:
        json.dump(result, fp, indent=3)
