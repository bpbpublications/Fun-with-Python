def __post_data(self, url, page_limit=500, page_offset=0):
    click.echo(f"Page limit: {page_limit}, offset: {page_offset}")
    data = {
        "currency": "USD",
        "sort": "rank",
        "order": "ascending",
        "offset": page_offset,
        "limit": page_limit,
        "meta": True,
    }
    data = requests.post(
        url, headers={"x-api-key": self.__api_token, "content-type": "application/json"}, json=data
    ).json()
    if data:
        more_data = self.__post_data(url, page_limit=page_limit, page_offset=((page_offset + 1) + page_limit))
        if more_data:
            data += more_data
    return data
