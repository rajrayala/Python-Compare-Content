from bs4 import BeautifulSoup

def parse_and_flatten_html(soup):
    def parse_html_structure(element, parent_name=''):
        structure = []
        for child in element.find_all(recursive=False):
            if child.name not in ['script', 'style', 'img', 'header', 'nav']:
                text = child.get_text(strip=True)
                full_name = f"{parent_name}>{child.name}" if parent_name else child.name
                children = parse_html_structure(child, full_name)
                if text and not children:
                    structure.append({
                        'tag': full_name,
                        'text': text,
                        'children': []
                    })
                structure.extend(children)
        return structure

    def flatten_structure(structure, parent_tag=''):
        flat_structure = []
        for elem in structure:
            combined_tag = f"{parent_tag}>{elem['tag']}" if parent_tag else elem['tag']
            if elem['text']:
                flat_structure.append((combined_tag, elem['text']))
            flat_structure.extend(flatten_structure(elem['children'], combined_tag))
        return flat_structure

    parsed_structure = parse_html_structure(soup)
    return flatten_structure(parsed_structure)
