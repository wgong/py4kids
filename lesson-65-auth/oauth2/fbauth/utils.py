import re

def parse_url(url):
    """assume 4 parts: proto://host:port/path
    """
    z = re.match(r"^(.*:)//([A-Za-z0-9\-\.]+)(:[0-9]+)?(/.*)$", url)
    if not z:
        return None

    return z.group(1)[:-1], z.group(2), z.group(3)[1:], z.group(4)