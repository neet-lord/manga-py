from manga_dl.provider import Provider
from manga_dl.providers.helpers.jav_zip_org import JavZipOrg
from .helpers.std import Std


class ZipReadCom(Provider, Std):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        idx = self.re.search(r'/.p=(\d+)', self.chapter).group(1)
        return '{}-{}'.format(self.chapter_index, idx)

    def get_main_content(self):
        pass

    def get_manga_name(self) -> str:
        return self._get_name(r'\.com/([^/]+)')

    def get_chapters(self):
        return self.html_fromstring(self.get_url(), '#content .entry > p > a')

    def get_files(self):
        jav_zip_org = JavZipOrg(self)
        return jav_zip_org.get_images()

    def get_cover(self):
        return self._cover_from_content('#content .entry p > img')


main = ZipReadCom