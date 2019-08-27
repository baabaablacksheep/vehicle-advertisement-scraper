
def format_url(url):
    # Sample Url - https://ikman.lk/en/ad/nissan-march-k11-2000-for-sale-kalutara-82
    protocol_removed = url.split("//")[-1]
    slash_split_arr = protocol_removed.split("/")
    slash_split_arr.pop(0)
    web_site_removed = "_".join(slash_split_arr)
    if web_site_removed.endswith(".html"):
        web_site_removed = web_site_removed.replace(".html", "")
    return web_site_removed
