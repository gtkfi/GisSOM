# pylint: disable=missing-docstring
import os
import sys
import logging
import warnings
import percy

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains

from selenium.common.exceptions import WebDriverException, TimeoutException

from dash.testing.wait import (
    text_to_equal,
    style_to_equal,
    contains_text,
    until,
)
from dash.testing.dash_page import DashPageMixin
from dash.testing.errors import DashAppLoadingError, BrowserError


logger = logging.getLogger(__name__)


class Browser(DashPageMixin):
    def __init__(
        self,
        browser,
        headless=False,
        options=None,
        remote=None,
        download_path=None,
        percy_finalize=True,
        wait_timeout=10,
    ):
        self._browser = browser.lower()
        self._headless = headless
        self._options = options
        self._download_path = download_path
        self._wait_timeout = wait_timeout
        self._percy_finalize = percy_finalize

        self._driver = until(lambda: self.get_webdriver(remote), timeout=1)
        self._driver.implicitly_wait(2)

        self._wd_wait = WebDriverWait(self.driver, wait_timeout)
        self._last_ts = 0
        self._url = None

        self._window_idx = 0  # switch browser tabs

        self.percy_runner = percy.Runner(
            loader=percy.ResourceLoader(
                webdriver=self.driver,
                base_url="/assets",
                root_dir="tests/assets",
            )
        )
        self.percy_runner.initialize_build()

        logger.debug("initialize browser with arguments")
        logger.debug("  headless => %s", self._headless)
        logger.debug("  download_path => %s", self._download_path)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        try:
            self.driver.quit()
            if self._percy_finalize:
                logger.info("percy runner finalize build now")
                self.percy_runner.finalize_build()
            else:
                logger.info("percy finalize relies on CI job")
        except WebDriverException:
            logger.exception("webdriver quit was not successful")
        except percy.errors.Error:
            logger.exception("percy runner failed to finalize properly")

    def percy_snapshot(self, name=""):
        """percy_snapshot - visual test api shortcut to `percy_runner.snapshot`
        it also combines the snapshot `name` with the python version
        """
        snapshot_name = "{} - py{}.{}".format(
            name, sys.version_info.major, sys.version_info.minor
        )
        logger.info("taking snapshot name => %s", snapshot_name)
        self.percy_runner.snapshot(name=snapshot_name)

    def take_snapshot(self, name):
        """hook method to take snapshot when a selenium test fails
        The snapshot is placed under
            - `/tmp/dash_artifacts` in linux
            - `%TEMP` in windows
        with a filename combining test case name and the
        running selenium session id
        """
        target = (
            "/tmp/dash_artifacts"
            if not self._is_windows()
            else os.getenv("TEMP")
        )
        if not os.path.exists(target):
            try:
                os.mkdir(target)
            except OSError:
                logger.exception("cannot make artifacts")

        self.driver.save_screenshot(
            "{}/{}_{}.png".format(target, name, self.session_id)
        )

    def find_element(self, selector):
        """find_element returns the first found element by the css `selector`
        shortcut to `driver.find_element_by_css_selector`
        """
        return self.driver.find_element_by_css_selector(selector)

    def find_elements(self, selector):
        """find_elements returns a list of all elements matching the css
        `selector`. shortcut to `driver.find_elements_by_css_selector`
        """
        return self.driver.find_elements_by_css_selector(selector)

    def _wait_for(self, method, args, timeout, msg):
        """abstract generic pattern for explicit WebDriverWait"""
        _wait = (
            self._wd_wait
            if timeout is None
            else WebDriverWait(self.driver, timeout)
        )
        logger.debug(
            "method, timeout, poll => %s %s %s",
            method,
            _wait._timeout,  # pylint: disable=protected-access
            _wait._poll,  # pylint: disable=protected-access
        )

        return _wait.until(method(*args), msg)

    def wait_for_element(self, selector, timeout=None):
        """wait_for_element is shortcut to `wait_for_element_by_css_selector`
        timeout if not set, equals to the fixture's `wait_timeout`
        """
        return self.wait_for_element_by_css_selector(selector, timeout)

    def wait_for_element_by_css_selector(self, selector, timeout=None):
        """explicit wait until the element is present,
        timeout if not set, equals to the fixture's `wait_timeout`
        shortcut to `WebDriverWait` with `EC.presence_of_element_located`
        """
        return self._wait_for(
            EC.presence_of_element_located,
            ((By.CSS_SELECTOR, selector),),
            timeout,
            "timeout {}s => waiting for selector {}".format(
                timeout if timeout else self._wait_timeout, selector
            ),
        )

    def wait_for_style_to_equal(self, selector, style, val, timeout=None):
        """explicit wait until the element's style has expected `value`
        timeout if not set, equals to the fixture's `wait_timeout`
        shortcut to `WebDriverWait` with customized `style_to_equal` condition
        """
        return self._wait_for(
            method=style_to_equal,
            args=(selector, style, val),
            timeout=timeout,
            msg="style val => {} {} not found within {}s".format(
                style, val, timeout if timeout else self._wait_timeout
            ),
        )

    def wait_for_text_to_equal(self, selector, text, timeout=None):
        """explicit wait until the element's text equals the expected `text`.
        timeout if not set, equals to the fixture's `wait_timeout`
        shortcut to `WebDriverWait` with customized `text_to_equal` condition
        """
        return self._wait_for(
            method=text_to_equal,
            args=(selector, text),
            timeout=timeout,
            msg="text -> {} not found within {}s".format(
                text, timeout if timeout else self._wait_timeout
            ),
        )

    def wait_for_contains_text(self, selector, text, timeout=None):
        """explicit wait until the element's text contains the expected `text`.
        timeout if not set, equals to the fixture's `wait_timeout`
        shortcut to `WebDriverWait` with customized `contains_text` condition
        """
        return self._wait_for(
            method=contains_text,
            args=(selector, text),
            timeout=timeout,
            msg="text -> {} not found inside element within {}s".format(
                text, timeout if timeout else self._wait_timeout
            ),
        )

    def wait_for_page(self, url=None, timeout=10):
        """wait_for_page navigates to the url in webdriver
        wait until the renderer is loaded in browser. use the `server_url`
        if url is not provided.
        """
        self.driver.get(self.server_url if url is None else url)
        try:
            self.wait_for_element_by_css_selector(
                self.dash_entry_locator, timeout=timeout
            )
        except TimeoutException:
            logger.exception(
                "dash server is not loaded within %s seconds", timeout
            )
            logger.debug(self.get_logs())
            raise DashAppLoadingError(
                "the expected Dash react entry point cannot be loaded"
                " in browser\n HTML => {}\n Console Logs => {}\n".format(
                    self.driver.find_element_by_tag_name("body").get_property(
                        "innerHTML"
                    ),
                    "\n".join((str(log) for log in self.get_logs())),
                )
            )

    def select_dcc_dropdown(self, selector, value=None, index=None):
        dropdown = self.driver.find_element_by_css_selector(selector)
        dropdown.click()

        menu = dropdown.find_element_by_css_selector("div.Select-menu-outer")
        logger.debug(
            "the available options are %s", "|".join(menu.text.split("\n"))
        )

        options = menu.find_elements_by_css_selector(
            "div.VirtualizedSelectOption"
        )
        if options:
            if isinstance(index, int):
                options[index].click()
                return

            for option in options:
                if option.text == value:
                    option.click()
                    return

        logger.error(
            "cannot find matching option using value=%s or index=%s",
            value,
            index,
        )

    def toggle_window(self):
        """switch between the current working window and the new opened one"""
        idx = (self._window_idx + 1) % 2
        self.switch_window(idx=idx)
        self._window_idx += 1

    def switch_window(self, idx=0):
        """switch to window by window index
        shortcut to `driver.switch_to.window`
        """
        if len(self.driver.window_handles) <= idx:
            raise BrowserError("there is no second window in Browser")

        self.driver.switch_to.window(self.driver.window_handles[idx])

    def open_new_tab(self, url=None):
        """open a new tab in browser
        url is not set, equals to `server_url`
        """
        self.driver.execute_script(
            'window.open("{}", "new window")'.format(
                self.server_url if url is None else url
            )
        )

    def get_webdriver(self, remote):
        try:
            return (
                getattr(self, "_get_{}".format(self._browser))()
                if remote is None
                else webdriver.Remote(
                    command_executor=remote,
                    desired_capabilities=getattr(
                        DesiredCapabilities, self._browser.upper()
                    ),
                )
            )
        except WebDriverException:
            logger.exception("<<<Webdriver not initialized correctly>>>")
            return None

    def _get_wd_options(self):
        options = (
            self._options[0]
            if self._options and isinstance(self._options, list)
            else getattr(webdriver, self._browser).options.Options()
        )

        if self._headless:
            options.headless = True

        return options

    def _get_chrome(self):
        options = self._get_wd_options()

        capabilities = DesiredCapabilities.CHROME
        capabilities["loggingPrefs"] = {"browser": "SEVERE"}

        if "DASH_TEST_CHROMEPATH" in os.environ:
            options.binary_location = os.environ["DASH_TEST_CHROMEPATH"]

        options.add_experimental_option(
            "prefs",
            {
                "download.default_directory": self.download_path,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": False,
                "safebrowsing.disable_download_protection": True,
            },
        )

        chrome = webdriver.Chrome(
            options=options, desired_capabilities=capabilities
        )

        # https://bugs.chromium.org/p/chromium/issues/detail?id=696481
        if self._headless:
            # pylint: disable=protected-access
            chrome.command_executor._commands["send_command"] = (
                "POST",
                "/session/$sessionId/chromium/send_command",
            )
            params = {
                "cmd": "Page.setDownloadBehavior",
                "params": {
                    "behavior": "allow",
                    "downloadPath": self.download_path,
                },
            }
            res = chrome.execute("send_command", params)
            logger.debug("enabled headless download returns %s", res)

        chrome.set_window_position(0, 0)
        return chrome

    def _get_firefox(self):
        options = self._get_wd_options()

        capabilities = DesiredCapabilities.FIREFOX
        capabilities["loggingPrefs"] = {"browser": "SEVERE"}
        capabilities["marionette"] = True

        # https://developer.mozilla.org/en-US/docs/Download_Manager_preferences
        fp = webdriver.FirefoxProfile()
        fp.set_preference("browser.download.dir", self.download_path)
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference(
            "browser.helperApps.neverAsk.saveToDisk",
            "application/octet-stream",  # this MIME is generic for binary
        )
        return webdriver.Firefox(
            firefox_profile=fp, options=options, capabilities=capabilities
        )

    @staticmethod
    def _is_windows():
        return sys.platform == "win32"

    def multiple_click(self, selector, clicks):
        """multiple_click click the element with number of `clicks`"""
        for _ in range(clicks):
            self.find_element(selector).click()

    def clear_input(self, elem):
        """simulate key press to clear the input"""
        (
            ActionChains(self.driver)
            .click(elem)
            .send_keys(Keys.HOME)
            .key_down(Keys.SHIFT)
            .send_keys(Keys.END)
            .key_up(Keys.SHIFT)
            .send_keys(Keys.DELETE)
        ).perform()

    def get_logs(self):
        """return a list of `SEVERE` level logs after last reset time stamps
        (default to 0, resettable by `reset_log_timestamp`. Chrome only
        """
        if self.driver.name.lower() == "chrome":
            return [
                entry
                for entry in self.driver.get_log("browser")
                if entry["timestamp"] > self._last_ts
            ]
        warnings.warn(
            "get_logs always return None with webdrivers other than Chrome"
        )
        return None

    def reset_log_timestamp(self):
        """reset_log_timestamp only work with chrome webdrier"""
        if self.driver.name.lower() == "chrome":
            entries = self.driver.get_log("browser")
            if entries:
                self._last_ts = entries[-1]["timestamp"]

    @property
    def driver(self):
        """expose the selenium webdriver as fixture property"""
        return self._driver

    @property
    def session_id(self):
        return self.driver.session_id

    @property
    def server_url(self):
        return self._url

    @server_url.setter
    def server_url(self, value):
        """set the server url so the selenium is aware of the local server port
        it also implicitly calls `wait_for_page`
        """
        self._url = value
        self.wait_for_page()

    @property
    def download_path(self):
        return self._download_path
