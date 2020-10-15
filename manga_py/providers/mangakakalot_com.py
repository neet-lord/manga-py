from manga_py.provider import Provider
from .helpers.std import Std
from .helpers.manganelo_com_helper import check_alternative_server

import cssselect


class MangaKakalotCom(Provider, Std):
    # __alternative_cdn = 'https://bu2.mkklcdnbuv1.com'

    def get_chapter_index(self) -> str:
        re = self.re.search('/chapter_([^/]+)', self.chapter)
        return re.group(1).replace('.', '-', 2)

    def get_main_content(self):
        return self.http_get(self.get_url())

    def __new_url(self):
        from requests import get
        from sys import stderr
        with get(self.get_url()) as req:
            if req.url != self.get_url():
                print('New url: %s' % req.url, file=stderr)

            self._params['url'] = req.url
            self._storage['main_content'] = req.text

    def get_manga_name(self) -> str:
        if ~self.get_url().find('/manga/'):
            self.__new_url()

        return self._get_name(r'/(?:read-|manga/)(\w+)')

    def get_chapters(self):
        return self._elements('.chapter-list span a')

    def get_files(self):
        chapter = self.chapter
        result = self.html_fromstring(chapter, '#vungdoc img')
        images = [i.get('src') for i in result]
        return images
        # check_alternative_server(images, self.__alternative_cdn, headers={
        #     'Referer': chapter,
        #     'Accept': 'image/webp,*/*',
        # })

    def book_meta(self) -> dict:
        # todo meta
        title = self.get_title()
        url = self.get_url()
        
        cover = self.get_cover()
        tags = self.get_tags()
        alternate_names = self.get_alternate_names()
        authors = self.get_authors()
        description = self.get_description()
        meta = {
            'author': authors,
            'title': title,
            'url': url,
            'description': description,
            'cover': cover,
            'tags': tags,
            'alternate_names': alternate_names,
            'authors': authors,
        }

        return meta
    def get_title(self) -> str:
        return self._title_from_content('.manga-info-text h1')

    def get_cover(self) -> str:
        return self._cover_from_content('.manga-info-pic img')

    def get_tags(self) -> list:
        return self._tags_from_content('.manga-info-text li:nth-child(7) a')

    def get_authors(self) -> list:
        return self._authors_from_content('.manga-info-text li:nth-child(2) a')

    def get_alternate_names(self) -> list:
        _alternate_names = list()
        try:
            _alternate_names = self._elements('.manga-info-text .story-alternative')[0].text_content()
            _alternate_names = _alternate_names.split(':')[1].strip().split(';')

            alternate_names = list()

            for _alternate_name in _alternate_names:
                alternate_names.append(_alternate_name.strip())
        except IndexError:
            alternate_names = _alternate_names
    
        return alternate_names
    
    def get_description(self) -> str:
        
        _description = 'Please wait for us to review this before we add a description.'
        try:
            _description = self._elements('#noidungm')
            description = ''.join(_description[0].xpath('//div[@id="noidungm"]/text()')).strip()
        except IndexError:
            description = _description
            
        return description
    
main = MangaKakalotCom
