# pylint: disable=too-few-public-methods
"""Utils methods for pytest-dash such wait_for wrappers"""
import time
import logging
from selenium.common.exceptions import WebDriverException
from dash.testing.errors import TestingTimeoutError


logger = logging.getLogger(__name__)


def until(
    wait_cond,
    timeout,
    poll=0.1,
    msg="expected condition not met within timeout",
):  # noqa: C0330
    res = wait_cond()
    logger.debug(
        "start wait.until with method, timeout, poll => %s %s %s",
        wait_cond,
        timeout,
        poll,
    )
    end_time = time.time() + timeout
    while not res:
        if time.time() > end_time:
            raise TestingTimeoutError(msg)
        time.sleep(poll)
        res = wait_cond()
        logger.debug("poll => %s", time.time())

    return res


def until_not(
    wait_cond, timeout, poll=0.1, msg="expected condition met within timeout"
):  # noqa: C0330
    res = wait_cond()
    logger.debug(
        "start wait.until_not method, timeout, poll => %s %s %s",
        wait_cond,
        timeout,
        poll,
    )
    end_time = time.time() + timeout
    while res:
        if time.time() > end_time:
            raise TestingTimeoutError(msg)
        time.sleep(poll)
        res = wait_cond()
        logger.debug("poll => %s", time.time())

    return res


class contains_text(object):
    def __init__(self, selector, text):
        self.selector = selector
        self.text = text

    def __call__(self, driver):
        try:
            elem = driver.find_element_by_css_selector(self.selector)
            logger.debug(
                "contains text {%s} => expected %s", elem.text, self.text
            )
            return self.text in str(elem.text) or self.text in str(
                elem.get_attribute("value")
            )
        except WebDriverException:
            logger.exception("contains_text encountered an exception")
            return False


class text_to_equal(object):
    def __init__(self, selector, text):
        self.selector = selector
        self.text = text

    def __call__(self, driver):
        try:
            elem = driver.find_element_by_css_selector(self.selector)
            logger.debug(
                "text to equal {%s} => expected %s", elem.text, self.text
            )
            return (
                str(elem.text) == self.text
                or str(elem.get_attribute("value")) == self.text
            )
        except WebDriverException:
            logger.exception("text_to_equal encountered an exception")
            return False


class style_to_equal(object):
    def __init__(self, selector, style, val):
        self.selector = selector
        self.style = style
        self.val = val

    def __call__(self, driver):
        try:
            elem = driver.find_element_by_css_selector(self.selector)
            val = elem.value_of_css_property(self.style)
            logger.debug("style to equal {%s} => expected %s", val, self.val)
            return val == self.val
        except WebDriverException:
            logger.exception("style_to_equal encountered an exception")
            return False
