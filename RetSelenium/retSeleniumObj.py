from selenium import webdriver


class RetSeleniumObj():

    chrome_driver_path = "/Users/kimjunhyeon/Desktop/chrome_driver/chromedriver"

    @classmethod
    def get_selenium_obj(cls):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        # 혹은 options.add_argument("--disable-gpu")

        driver = webdriver.Chrome(RetSeleniumObj.chrome_driver_path, chrome_options=options)

        return driver

