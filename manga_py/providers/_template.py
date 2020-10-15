from manga_py.provider import Provider
from .helpers.std import Std


class _Template(Provider, Std):
    def get_archive_name(self) -> str:
        """
        Allows you to overload name generation. Method may be missing
        """

    def get_chapter_index(self) -> str:
        """
        Any string separated by "-"
        Example: "1-3"
        """

    def get_main_content(self):
        """
        Called second. Returns the initial content to parse (just a cache)
        Can be obtained using self.content
        """

    def get_manga_name(self) -> str:
        """
        String for the name of the manga directory
        """

    def get_manga_title(self) -> str:
        """
        String for the title of the manga directory
        """

    def get_chapters(self):
        """
        Should return an array of data (you can return the result of the self._elements ('css selector') method)
        """
        # return self._elements('a.chapter')
        return []

    def get_files(self):
        """
        Should return an array of strings (url of images)
        """
        return []

    def get_cover(self) -> str:
        """
        Not used in the original repo, but reimplemented in my fork.
        Get the cover of the comic.
        """

    def book_meta(self) -> dict:
        """
        Not used in the original repo, but reimplemented in my fork.
        :see http://acbf.wikia.com/wiki/Meta-data_Section_Definition
        return {
            'author': str,
            'title': str,
            'alternate-names': list,
            'description': str,
            'tags': list,
            'source': url
          }
        """

    def chapter_for_json(self) -> str:
        """
        overload std param, if need
        If present, overloads getting chapter name for json dump
        Should return a string
        """
        # return self.chapter
        pass

    def get_tags(self) -> list:
        """
        Fetch the tags for the manga. This is meant to be used
        for my webscraper. 
        """

    def get_authors(self) -> list:
        """
        Fetch the authors for the manga.
        Again, this is meant to be used for web scraping purposes.
        """
    
    def get_alternate_names(self) -> list:
        """
        Fetch the alternate names for the manga.
        """

main = _Template
