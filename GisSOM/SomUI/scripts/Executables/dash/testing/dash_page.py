from bs4 import BeautifulSoup


class DashPageMixin(object):
    def _get_dash_dom_by_attribute(self, attr):
        return BeautifulSoup(
            self.find_element(self.dash_entry_locator).get_attribute(attr),
            "lxml",
        )

    @property
    def devtools_error_count_locator(self):
        return ".test-devtools-error-count"

    @property
    def dash_entry_locator(self):
        return "#react-entry-point"

    @property
    def dash_outerhtml_dom(self):
        return self._get_dash_dom_by_attribute("outerHTML")

    @property
    def dash_innerhtml_dom(self):
        return self._get_dash_dom_by_attribute("innerHTML")

    @property
    def redux_state_paths(self):
        return self.driver.execute_script(
            "return window.store.getState().paths"
        )

    @property
    def redux_state_rqs(self):
        return self.driver.execute_script(
            "return window.store.getState().requestQueue"
        )

    def get_local_storage(self, store_id="local"):
        return self.driver.execute_script(
            "return JSON.parse(window.localStorage.getItem('{}'));".format(
                store_id
            )
        )

    def get_session_storage(self, session_id="session"):
        return self.driver.execute_script(
            "return JSON.parse(window.sessionStorage.getItem('{}'));".format(
                session_id
            )
        )
