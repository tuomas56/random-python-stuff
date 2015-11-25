#!/usr/bin/env python3

from ffnet import Story
from ebooklib import epub
import argparse
from urllib.parse import urlparse
import re
from tsprint import print
from multiprocessing import Pool

INFO_TEMPLATE = """
<dl>
    <dt>Title</dt><dd>{s.title}</dd>
    <dt>Author</dt><dd>{s.author}</dd>
    <dt>Summary<dt><dd>{s.summary}</dd>
<hr/>
    <dt>Number of Chapters</dt><dd>{s.number_chapters}</dd>
    <dt>Number of Words</dt><dd>{s.number_words}</dd>
<hr/>
    <dt>Category</dt><dd>{s.category}</dd>
    <dt>Date Published</dt><dd>{s.date_published}</dd>
    <dt>Status</dt><dd>{s.status}</dd>
</dl>
"""

STYLE = """
@namespace epub "http://www.idpf.org/2007/ops";

body {
    font-family: Verdana, Helvetica, Arial, sans-serif;
    color: black;
}

dt {
 font-weight: bold;
 display: inline;
}

dd:after {
    content: '';
    display: block;
    clear: both;
}

dd {
 display: inline;
}

h1 {
    text-align: center;
    font-weight: bold;
}

h2 {
    text-align: left;
    text-transform: uppercase;
    font-weight: bold;
}

ol {
    list-style-type: none;
    margin: 0;
}

ol > li:first-child {
        margin-top: 0.3em;
}

nav[epub|type~='toc'] > ol > li > ol  {
    list-style-type:square;
}

nav[epub|type~='toc'] > ol > li > ol > li {
        margin-top: 0.3em;
}

ol > li {
    margin-top: 0.3em;
}

ol > li > span {
    font-weight: bold;
}

ol > li > ol {
    margin-left: 0.5em;
}
"""

def process_url(url, debug=True):
    story = Story(url)
    book = epub.EpubBook()

    book.set_identifier("fanfiction.net-%s" % story.id)
    book.set_title(story.title)
    book.set_language('en')

    book.add_author(story.author)

    default_css = epub.EpubItem(uid="style_default", file_name="style/default.css", media_type="text/css", content=STYLE)
    book.add_item(default_css)

    chapters = []

    for i, chapter in enumerate(story.get_chapters(), start=1):
        if debug:
            print('\r{2} - [{0}] {1}%'.format('#'*int(10 * i/story.number_chapters), int(100*i/story.number_chapters), '%s/%s' % (story.title, story.author)),end='')
        c = epub.EpubHtml(title=chapter.title, file_name='chapter%s.xhtml' % i)
        c.content = '<h1>%s</h1><br/>%s' % (chapter.title, chapter.text)
        c.add_item(default_css)
        chapters.append(c)
        book.add_item(c)

    info_chapter = epub.EpubHtml(title='Information', file_name='info.xhtml')
    info_chapter.content = INFO_TEMPLATE.format(s=story)
    info_chapter.add_item(default_css)
    book.add_item(info_chapter)

    book.toc = tuple(chapters)

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    book.spine = ['nav', info_chapter] + chapters

    if debug:
        print()

    return book

def parse_list(urls, debug=True, threads=1):
    result = []

    for url in urls:
        url_comp = urlparse(url)
        if url_comp.scheme == '' and url_comp.netloc == '':
            url = 'http://' + url
            url_comp = urlparse(url)
        elif url_comp.scheme == '':
            url = 'http:' + url
            url_comp = urlparse(url)
        if re.match(r'(www\.)?fanfiction\.net', url_comp.netloc) is None:
            return False
        elif re.match(r'\/s\/[0-9]+\/[0-9]+\/.*', url_comp.path) is None:
            return False

        output = re.match(r'\/s\/[0-9]+\/[0-9]+\/(.*)', url_comp.path).group(1) + '.epub'
        result.append((url, output, debug))

    with Pool(threads) as p:
        p.starmap(process_one, result)
        


def process_one(url, output, debug=True):
    book = process_url(url, debug=debug)
    epub.write_epub(output, book, {})

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    parser.add_argument('url', help='the url of the story you wish to download or the location of a text file containing a list of stories (with the -l option.)')
    group.add_argument('-o','--output', help='output the story as an epub the specified location.', metavar='FILE')
    group.add_argument('-l','--list',help='download every story listed on a text file.', action='store_false')
    parser.add_argument('-s', '--silent', help='silence stdout.', action='store_false')
    parser.add_argument('-t','--threads', help='use multithreading (list mode only.)', type=int, default=5, metavar='NUM_THREADS')
    parsera = parser.parse_args()
    url_comp = urlparse(parsera.url)
    if url_comp.scheme == '' and url_comp.netloc == '' and parsera.list:
        parsera.url = 'http://' + parsera.url
        url_comp = urlparse(parsera.url)
    elif url_comp.scheme == '' and parsera.list:
        parsera.url = 'http:' + parsera.url
        url_comp = urlparse(parsera.url)
    if re.match(r'(www\.)?fanfiction\.net', url_comp.netloc) is None and parsera.list:
        parser.print_usage()
        return
    elif re.match(r'\/s\/[0-9]+\/[0-9]+\/.*', url_comp.path) is None and parsera.list:
        parser.print_usage()
        return
    
    if parsera.output is None and parsera.list:
        parsera.output = re.match(r'\/s\/[0-9]+\/[0-9]+\/(.*)', url_comp.path).group(1) + '.epub'

    if parsera.list:
        process_one(parsera.url, parsera.output, debug=parsera.silent)
    else:
        with open(parsera.url, 'r') as f:
            urls = f.readlines()
        if not parse_list(urls, debug=parsera.silent, threads=parsera.threads):
            parser.print_usage()
    
if __name__ == "__main__":
    main()


