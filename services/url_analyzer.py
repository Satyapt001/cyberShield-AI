import re

def extract_urls(text):

    urls = re.findall(
        r'https?://\S+|www\.\S+',
        text
    )

    return urls