class ScriptInjector:
    def __init__(self, driver,html_path):
        self.driver = driver
        self.html_path = html_path
    # Inject necessary scripts into the webpage
    def inject_scripts(self):
        with open("myapp/scripts/traditionalway+evaluation/vision_based_algorithm/js/injectBoundingBox.js", "r") as js_file:
            self.driver.execute_script(js_file.read())
        with open("myapp/scripts/traditionalway+evaluation/vision_based_algorithm/js/injectStyle.js", "r") as js_file:
            self.driver.execute_script(js_file.read())
        with open("myapp/scripts/traditionalway+evaluation/vision_based_algorithm/js/injectXpath.js", "r") as js_file:
            self.driver.execute_script(js_file.read())
        with open("myapp/scripts/traditionalway+evaluation/vision_based_algorithm/js/injectCleaned.js", "r") as js_file:
            self.driver.execute_script(js_file.read())
        
        if (self.html_path != ""):
            html_code = self.driver.page_source
            with open(self.html_path, 'w', encoding="utf-8") as f:
                f.write(html_code)
