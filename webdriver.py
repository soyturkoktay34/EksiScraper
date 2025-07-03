import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as SeleniumOptions
from undetected_chromedriver import ChromeOptions as UcOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

class WebDriverManager:
    def __init__(self, driver_path=None, use_undetected_driver=False, custom_options=None):
        self.driver_path = driver_path
        self.driver = None
        self.wait = None
        self.use_undetected_driver = use_undetected_driver
        self.options = self.default_options()
        if custom_options:
            self.configure_options(custom_options)

    def default_options(self):
        """Returns default Chrome options."""
        if self.use_undetected_driver:
            options = UcOptions()
            options.use_subprocess = False
        else:
            options = SeleniumOptions()

        prefs = {
            "profile.managed_default_content_settings.images": 2,
            "profile.content_settings.exceptions.automatic_downloads": {"*": {"setting": 2}},
            "media.autoplay.default": 1,
            "intl.accept_languages": "en,en_US"  # Set language to English
        }
        options.add_experimental_option("prefs", prefs)
        options.add_argument("--log-level=3")
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-cookies")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--window-size=1920,1080")  # Set window size to avoid automation detection
        options.add_argument("--lang=en")  # Set language to English
        options.add_argument("--headless")

        return options

    def configure_options(self, custom_options):
        """Adds or modifies Chrome options based on user-defined settings."""
        for option_method, *args in custom_options:
            getattr(self.options, option_method)(*args)

    def initialize_driver(self):
        """Configures and starts the Chrome WebDriver."""
        if self.use_undetected_driver:
            self.driver = uc.Chrome(options=self.options)
        else:
            service = Service(executable_path=self.driver_path)
            self.driver = webdriver.Chrome(service=service, options=self.options)
        self.wait = WebDriverWait(self.driver, 10)
        return self.driver, self.wait

    def get_action_chains(self):
        """Creates an ActionChains object."""
        return ActionChains(self.driver)

    def close_driver(self):
        """Safely closes the WebDriver."""
        if self.driver is not None:
            self.driver.quit()
