from bs4 import NavigableString, BeautifulSoup


def text_node(tag):
    if tag.name not in ["h1", "h2", "h3", "h4", "h5", "h6", "a", "div", "p", "li"]:
        return False
    if isinstance(tag, NavigableString):
        return False
    if not tag.text:  # if no text return false
        return False
    elif len(tag.find_all(text=False)) > 0:  # no other tags inside other than text
        return False

    return True


def extract_text_nodes(html):
    soup = BeautifulSoup(html, 'html.parser')
    text_nodes = soup.find_all(text_node)

    data = []
    for text in text_nodes:
        # text_content = text[text.find('>') + 1:text.rfind('<')]
        data.append({
            'src_html': text,
            'dest_html': text
        })

    return data
