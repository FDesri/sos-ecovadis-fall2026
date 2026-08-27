#!/usr/bin/env python3
"""ENEX -> clean markdown-ish text converter for the SOS-EcoVadis knowledge catalog."""
import sys, re, html
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Tag

def cell_text(el):
    t = inline_text(el)
    return re.sub(r'\s+', ' ', t).strip()

def inline_text(el):
    out = []
    for child in el.children if isinstance(el, Tag) else []:
        if isinstance(child, NavigableString):
            out.append(str(child))
        elif isinstance(child, Tag):
            if child.name == 'br':
                out.append(' ')
            elif child.name == 'a':
                href = child.get('href', '')
                txt = inline_text(child).strip()
                out.append(f'[{txt}]({href})' if href else txt)
            elif child.name in ('b', 'strong'):
                inner = inline_text(child)
                out.append(f'**{inner.strip()}**' if inner.strip() else inner)
            elif child.name in ('i', 'em'):
                inner = inline_text(child)
                out.append(f'*{inner.strip()}*' if inner.strip() else inner)
            elif child.name == 'u':
                out.append(inline_text(child))
            elif child.name == 'code':
                out.append('`' + inline_text(child) + '`')
            else:
                out.append(inline_text(child))
    return ''.join(out)

def walk(el, out, depth=0):
    for child in el.children:
        if isinstance(child, NavigableString):
            s = str(child).strip()
            if s:
                out.append(s)
            continue
        if not isinstance(child, Tag):
            continue
        name = child.name
        if name in ('h1', 'h2', 'h3', 'h4', 'h5'):
            lvl = int(name[1])
            txt = cell_text(child)
            if txt:
                out.append('\n' + '#' * lvl + ' ' + txt + '\n')
        elif name == 'div':
            style = child.get('style', '')
            if 'display:none' in style:
                continue
            if '--en-codeblock' in style:
                lines = []
                for d in child.find_all('div', recursive=False):
                    lines.append(cell_text(d))
                out.append('\n```\n' + '\n'.join(l for l in lines) + '\n```\n')
                continue
            # a div may contain nested block elements
            if child.find(['table', 'ul', 'ol', 'h1', 'h2', 'h3', 'div']):
                walk(child, out, depth)
            else:
                txt = inline_text(child).strip()
                if txt:
                    out.append(txt)
                else:
                    out.append('')
        elif name in ('ul', 'ol'):
            i = int(child.get('start', 1))
            for li in child.find_all('li', recursive=False):
                marker = f'{i}.' if name == 'ol' else '-'
                txt = cell_text(li)
                sub = []
                for subl in li.find_all(['ul', 'ol'], recursive=True):
                    pass
                out.append(('  ' * depth) + f'{marker} {txt}')
                if name == 'ol':
                    i += 1
        elif name == 'table':
            rows = []
            for tr in child.find_all('tr'):
                cells = [cell_text(td) for td in tr.find_all(['td', 'th'])]
                rows.append(cells)
            if rows:
                out.append('')
                ncol = max(len(r) for r in rows)
                for j, r in enumerate(rows):
                    r += [''] * (ncol - len(r))
                    out.append('| ' + ' | '.join(r) + ' |')
                    if j == 0:
                        out.append('|' + '---|' * ncol)
                out.append('')
        elif name == 'blockquote':
            inner = []
            walk(child, inner, depth)
            for l in inner:
                if l.strip():
                    out.append('> ' + l)
        elif name == 'hr':
            out.append('\n---\n')
        elif name == 'br':
            out.append('')
        else:
            walk(child, out, depth)

def parse_enex(path):
    raw = Path(path).read_text(encoding='utf-8', errors='replace')
    notes = []
    for m in re.finditer(r'<note>(.*?)</note>', raw, re.S):
        block = m.group(1)
        title = re.search(r'<title>(.*?)</title>', block, re.S)
        created = re.search(r'<created>(.*?)</created>', block, re.S)
        updated = re.search(r'<updated>(.*?)</updated>', block, re.S)
        author = re.search(r'<author>(.*?)</author>', block, re.S)
        source = re.search(r'<source>(.*?)</source>', block, re.S)
        cdata = re.search(r'<!\[CDATA\[(.*?)\]\]>', block, re.S)
        content_md = ''
        if cdata:
            soup = BeautifulSoup(cdata.group(1), 'html.parser')
            en = soup.find('en-note') or soup
            out = []
            walk(en, out)
            # collapse multiple blank lines
            txt = '\n'.join(out)
            txt = re.sub(r'\n{3,}', '\n\n', txt)
            content_md = txt.strip()
        notes.append({
            'title': html.unescape(title.group(1)) if title else '',
            'created': created.group(1) if created else '',
            'updated': updated.group(1) if updated else '',
            'author': html.unescape(author.group(1)) if author else '',
            'source': source.group(1) if source else '',
            'content': content_md,
        })
    return notes

if __name__ == '__main__':
    src_dir = Path('/home/claude/kc/enex')
    dst_dir = Path('/home/claude/kc/parsed')
    dst_dir.mkdir(exist_ok=True)
    for f in sorted(src_dir.iterdir()):
        if f.suffix.lower() not in ('.enex', '.ene'):
            continue
        try:
            notes = parse_enex(f)
        except Exception as e:
            print(f'ERROR {f.name}: {e}')
            continue
        for idx, n in enumerate(notes):
            suffix = f'_{idx}' if len(notes) > 1 else ''
            outname = f.stem + suffix + '.md'
            hdr = (f"<!-- source_file: {f.name} | title: {n['title']} | created: {n['created']}"
                   f" | updated: {n['updated']} | author: {n['author']} | source_app: {n['source']} -->\n\n")
            (dst_dir / outname).write_text(hdr + '# ' + n['title'] + '\n\n' + n['content'] + '\n', encoding='utf-8')
            print(f"OK {outname} ({len(n['content'])} chars)")
