from src.provider import Provider
from src.base_classes.web_driver import WebDriver
from requests import Session


class TsuminoCom:
    provider = None

    def __init__(self, provider: Provider):
        self.provider = provider

    def get_cookies(self, url):
        web_driver = WebDriver()
        driver = web_driver.get_driver()
        page = driver.get(url)
        iframe = page.find_element_by_css_selector(".g-recaptcha iframe")
        src = self.provider.http_get(iframe.get_attribute('src'))
        driver.close()

        g_token = self.provider.html_fromstring(src).cssselect('#recaptcha-token')
        session = Session()
        h = session.post('{}/Read/AuthProcess'.format(self.provider.domain), data={
            'g-recaptcha-response': g_token[0].get('value'),
            'Id': 1,
            'Page': 1,
        })
        session.close()
        return h.cookies
