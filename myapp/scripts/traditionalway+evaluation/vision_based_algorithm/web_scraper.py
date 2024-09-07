from pywebcopy import save_webpage
import os, sys

class WebScraper:
    def __init__(self, driver, url,domain):
        self.driver = driver
        self.url = url
        self.domain = domain
        self.current_dir = os.getcwd()
    #Save full page
    def save_full_html(self):
        kwargs = {'bypass_robots': True, 'project_name': 'resources/saved_full_html'}
        sys.stdout = open(os.devnull, 'w')
        save_webpage(self.url,self.current_dir, **kwargs)
        sys.stdout = sys.__stdout__
        html_path = f'{self.current_dir}/resources/saved_full_html/{self.domain}/index.html'
        html_url = f'file:///{html_path}'
        return html_path, html_url
    
    #Save just html
    def save_html(self):
        html_code = self.driver.page_source
        html_path = f'{self.current_dir}/resources/saved_html/{self.domain}.html'
        html_url = f'file:///{html_path}'
        app_url =  f"myapp/static/saved_html/result.html"
        with open(app_url, 'w', encoding="utf-8") as f:
            f.write(html_code)
        return app_url, html_url
