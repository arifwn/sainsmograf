
import os
import sys
import re
from unidecode import unidecode

import yaml
import datetime
import unicodedata

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\:\[\\\]^_`{|},.]+')

def slugify(text, delim=u'-'):
    """Generates an ASCII-only slug."""
    if sys.version_info[0] == 2:
        if isinstance(text, str):
            text = unicode(text, "utf-8")

    result = []
    for word in _punct_re.split(text.lower()):
        result.extend(unidecode(word).split())
    slug = delim.join(result)
    if sys.version_info[0] == 2:
        return unicode(slug)
    return slug


def create_content(content_type, title, slug=None):
    from fsbp import app

    if slug is None:
        slug = slugify(title)

    filename = '{0}.markdown'.format(slug)

    header = {
                'layout': content_type,
                'title': title,
             }

    if content_type == 'page':
        header['url'] = '/{0}/'.format(slug)
    if content_type == 'post':
        header['date'] = datetime.datetime.now()
        header['author'] = app.config.get('SITE_AUTHOR', 'Unknown')
        header['published'] = True
        header['comments'] = True
        header['excerpt'] = ''
        header['tags'] = ['uncategorized']
        header['thumbnail'] = { 'image': '' }
        header['cover'] = { 'image': '', 'image_type': 'parallax', 'image_credit': '', 'image_credit_url': '' }

        filename = '{0}-{1}.markdown'.format(header['date'].strftime('%Y-%m-%d'), slug)

    header_str = yaml.dump(header, default_flow_style=False)

    contents = "---\n{0}\n---\n\n# {1}\n\nInsert markdown contents here...\n".format(header_str, title)

    filepath = os.path.join('contents', '{0}s'.format(content_type), filename)

    if os.path.isfile(filepath):
        raise Exception('file {0} is already exist!'.format(filepath))

    with open(filepath, 'w') as f:
        f.write(contents)

    return filepath
