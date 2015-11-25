#github.com/jabagawee/FanFiction.Net-API
#@tuomas56 & @pigworts2 - Converted to Py3k and Updated REGEXES

import re
import urllib.request, urllib.error, urllib.parse

import bs4


_STORYID_REGEX = r"var\s+storyid\s*=\s*(\d+);"
_CHAPTER_REGEX = r"var\s+chapter\s*=\s*(\d+);"
_CHAPTERS_REGEX = r"Chapters:\s*?([0-9]+)"
_WORDS_REGEX = r"Words:\s*?([0-9]+(\,[0-9]+)*)"
_USERID_REGEX = r"var\s+userid\s*=\s*(\d+);"
_TITLE_REGEX = r"var\s+title\s*=\s*'(.+)';"
_TITLE_T_REGEX = r"<b class='xcontrast_txt'>(.*?)</b>"
_SUMMARY_REGEX = r"<div style='margin-top:2px' class='xcontrast_txt'>(.*?)<\/div>"
_CAT_TITLE_REGEX = r"<a class=xcontrast_txt href=\"\/.+?\/.+?\/\">(.*?)</a>"
_DATEP_REGEX = r"<span data-xutime='[0-9]+'>(.*?)</span>"
_AUTHOR_REGEX = r"<a class='xcontrast_txt' href='\/u\/[0-9]+\/.*?'>(.*?)</a>"

# Useful for generating a review URL later on
_STORYTEXTID_REGEX = r"storytextid=(\d+);"

# Used to parse the attributes which aren't directly contained in the
# JavaScript and hence need to be parsed manually
_NON_JAVASCRIPT_REGEX = r'Rated:(.+)'
_HTML_TAG_REGEX = r'<.*?>'

# Needed to properly decide if a token contains a genre or a character name
# while manually parsing data that isn't directly contained in the JavaScript
_GENRES = [
    'General', 'Romance', 'Humor', 'Drama', 'Poetry', 'Adventure', 'Mystery',
    'Horror', 'Parody', 'Angst', 'Supernatural', 'Suspense', 'Sci-Fi',
    'Fantasy', 'Spiritual', 'Tragedy', 'Western', 'Crime', 'Family', 'Hurt',
    'Comfort', 'Friendship'
]
_CHAPTER_URL_TEMPLATE = 'http://www.fanfiction.net/s/%d/%d'


def _parse_string(regex, source):
    """Returns first group of matched regular expression as string."""
    return re.search(regex, source).group(1)


def _parse_integer(regex, source):
    """Returns first group of matched regular expression as integer."""
    return int(re.search(regex, source).group(1))


def _unescape_javascript_string(string_):
    """Removes JavaScript-specific string escaping characters."""
    return string_.replace("\\'", "'").replace('\\"', '"').replace('\\\\', '\\')


class Story(object):
    def __init__(self, url, opener=urllib.request.urlopen):
        source = opener(url).read().decode()
        # Easily parsable and directly contained in the JavaScript, lets hope
        # that doesn't change or it turns into something like below
        self.id = _parse_integer(_STORYID_REGEX, source)
        try:
            self.number_chapters = _parse_integer(_CHAPTERS_REGEX, source)
        except:
            self.number_chapters = 1
        self.number_words = int(_parse_string(_WORDS_REGEX, source).replace(',',''))
        self.author_id = _parse_integer(_USERID_REGEX, source)
        self.title = _unescape_javascript_string(_parse_string(_TITLE_T_REGEX, source))
        self.summary = _unescape_javascript_string(_parse_string(_SUMMARY_REGEX, source))
        self.category = _unescape_javascript_string(_parse_string(_CAT_TITLE_REGEX, source))
        self.date_published = _parse_string(_DATEP_REGEX, source)
        self.author = _unescape_javascript_string(_parse_string(_AUTHOR_REGEX, source))

        # Tokens of information that aren't directly contained in the
        # JavaScript, need to manually parse and filter those
        tokens = [token.strip() for token in re.sub(_HTML_TAG_REGEX, '', _parse_string(_NON_JAVASCRIPT_REGEX, source)).split('-')]

        # Both tokens are constant and always available
        self.rated = tokens[0]
        self.language = tokens[1]

        # After those the remaining tokens are uninteresting and looking for
        # either character or genre tokens is useless
        token_terminators = ['Reviews: ', 'Updated: ', 'Published: ']

        # Check if tokens[2] contains the genre
        if tokens[2] in _GENRES or '/' in tokens[2] and all(token in _GENRES for token in tokens[2].split('/')):
            self.genre = tokens[2]
            # tokens[2] contained the genre, check if next token contains the
            # characters
            if not any(tokens[3].startswith(terminator) for terminator in token_terminators):
                self.characters = tokens[3]
            else:
                # No characters token
                self.characters = ''
        elif any(tokens[2].startswith(terminator) for terminator in token_terminators):
            # No genre and/or character was specified
            self.genre = ''
            self.characters = ''
            # tokens[2] must contain the characters since it wasn't a genre
            # (check first clause) but isn't either of "Reviews: ", "Updated: "
            # or "Published: " (check previous clause)
        else:
            self.characters = tokens[2]

        for token in tokens:
            if token.startswith('Reviews: '):
                # Replace comma in case the review count is greater than 9999
                self.reviews = int(token.split()[1].replace(',', ''))
                break
        else:
            # "Reviews: " wasn't found and for-loop not broken, hence no (0)
            # reviews
            self.reviews = 0

        # Status is directly contained in the tokens as a single-string
        if 'Complete' in tokens:
            self.status = 'Complete'
        else:
            # FanFiction.Net calls it "In-Progress", I'll just go with that
            self.status = 'In-Progress'

    def get_chapters(self, opener=urllib.request.urlopen):
        for number in range(1, self.number_chapters + 1):
            url = _CHAPTER_URL_TEMPLATE % (self.id, number)
            yield Chapter(url, opener)

    # Method alias which allows the user to treat the get_chapters method like
    # a normal property if no manual opener is to be specified.
    chapters = property(get_chapters)


class Chapter(object):
    def __init__(self, url, opener=urllib.request.urlopen):
        source = opener(url).read().decode()
        self.story_id = _parse_integer(_STORYID_REGEX, source)
        self.number = _parse_integer(_CHAPTER_REGEX, source)
        self.story_text_id = _parse_integer(_STORYTEXTID_REGEX, source)

        soup = bs4.BeautifulSoup(source, 'html5lib')
        select = soup.find('select', {'name': 'chapter'})
        if select:
            # There are multiple chapters available, use chapter's title
            self.title = select.find('option', selected=True).string.split(None, 1)[1]
        else:
            # No multiple chapters, one-shot or only a single chapter released
            # until now; for the lack of a proper chapter title use the story's
            self.title = _unescape_javascript_string(_parse_string(_TITLE_T_REGEX, source))
        soup = soup.find('div', id='storytext')
        # Normalize HTML tag attributes
        for hr in soup('hr'):
            del hr['size']
            del hr['noshade']
        self.text = soup.decode()