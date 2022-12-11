import datetime
import booking.constants as const
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from prettytable import PrettyTable
from booking.booking_filtration import BookingFiltration
from booking.booking_report import BookingReport


class Booking:
    def __init__(self, teardown=False):
        self.teardown = teardown
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--incognito')
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.options.add_experimental_option('detach', not self.teardown)
        # self.options.add_argument('--headless')
        self.service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.driver.implicitly_wait(3)
        self.driver.maximize_window()  # HAVE A CLEANER LOOK WHILE TEST THE BOT

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.driver.quit()

    def land_first_page(self):
        self.driver.get(const.BASE_URL)

    def change_currency(self, currency=None):
        currency_element = self.driver.find_element(By.CSS_SELECTOR, 'button[data-tooltip-text="Escolha sua moeda"]')
        currency_element.click()
        selected_currency_element = self.driver.find_element(
            By.CSS_SELECTOR,
            f'a[data-modal-header-async-url-param*="selected_currency={currency}"]')
        selected_currency_element.click()

    def select_place_to_go(self, place_to_go):
        search_field = self.driver.find_element(By.NAME, 'ss')
        search_field.clear()
        search_field.send_keys(place_to_go)
        try:
            first_result = self.driver.find_element(By.CSS_SELECTOR, 'li[data-i="0"]')
        except NoSuchElementException:
            first_result = self.driver.find_element(By.CSS_SELECTOR, 'ul[data-testid="autocomplete-results"]')
        first_result.click()

    def select_dates(self, check_in_date: str, check_out_date: str):
        # If the difference between dates is greater than 1 month, click to advance in calendar
        today = datetime.date.today()
        check_in_date = check_in_date[6:10] + '-' + check_in_date[3:5] + '-' + check_in_date[0:2]
        chosen_in_date = datetime.date.fromisoformat(check_in_date)
        check_out_date = check_out_date[6:10] + '-' + check_out_date[3:5] + '-' + check_out_date[0:2]
        chosen_out_date = datetime.date.fromisoformat(check_out_date)

        if chosen_in_date.year > today.year:
            diff_months = chosen_in_date.month + 12 - today.month
        else:
            diff_months = chosen_in_date.month - today.month

        if diff_months > 0:
            try:
                button_advance_calendar = self.driver.find_element(By.CSS_SELECTOR, 'div[data-bui-ref="calendar-next"]')
            except NoSuchElementException:
                button_advance_calendar = self.driver.find_element(By.XPATH, '//*[@id="indexsearch"]/div[2]/div/div/div/form/div[1]/div[2]/div/div[2]/div/div/button')
            for _ in range(diff_months):
                button_advance_calendar.click()
        try:
            check_in_element = self.driver.find_element(By.CSS_SELECTOR, f'span[data-date="{check_in_date}"]')
        except NoSuchElementException:
            check_in_element = self.driver.find_element(By.CSS_SELECTOR, f'td[data-date="{check_in_date}"]')

        check_in_element.click()

        if chosen_out_date.year > chosen_in_date.year:
            diff_months = chosen_out_date.month + 12 - chosen_in_date.month
        else:
            diff_months = chosen_out_date.month - chosen_in_date.month

        if diff_months > 0:
            try:
                button_advance_calendar = self.driver.find_element(By.CSS_SELECTOR, 'div[data-bui-ref="calendar-next"]')
            except NoSuchElementException:
                button_advance_calendar = self.driver.find_element(By.XPATH, '//*[@id="indexsearch"]/div[2]/div/div/div/form/div[1]/div[2]/div/div[2]/div/div/button')
            for _ in range(diff_months):
                button_advance_calendar.click()
        try:
            check_out_element = self.driver.find_element(By.CSS_SELECTOR, f'span[data-date="{check_out_date}"]')
        except NoSuchElementException:
            check_out_element = self.driver.find_element(By.CSS_SELECTOR, f'td[data-date="{check_out_date}"]')

        check_out_element.click()

    def select_adults(self, count=1):
        try:
            selection_element = self.driver.find_element(By.CSS_SELECTOR, 'button[data-testid="occupancy-config"]')
        except NoSuchElementException:
            selection_element = self.driver.find_element(By.ID, 'xp__guests__toggle')

        selection_element.click()

        while True:
            try:
                decrease_adults = self.driver.find_element(By.CSS_SELECTOR, 'button[data-bui-ref="input-stepper-subtract-button"]')
            except NoSuchElementException:
                decrease_adults = self.driver.find_element(By.XPATH, '//*[@id="indexsearch"]/div[2]/div/div/div/form/div[1]/div[3]/div/div/div/div/div[1]/div[2]/button[1]')
            decrease_adults.click()
            try:
                adults_value_element = self.driver.find_element(By.CSS_SELECTOR, 'span[class="bui-stepper__display"]')
            except NoSuchElementException:
                adults_value_element = self.driver.find_element(By.XPATH, '//*[@id="indexsearch"]/div[2]/div/div/div/form/div[1]/div[3]/div/div/div/div/div[1]/div[2]/span')
            if int(adults_value_element.text) == 1:
                break

        for _ in range(count - 1):
            try:
                increase_adults = self.driver.find_element(By.CSS_SELECTOR, 'button[data-bui-ref="input-stepper-add-button"]')
            except NoSuchElementException:
                increase_adults = self.driver.find_element(By.XPATH, '//*[@id="indexsearch"]/div[2]/div/div/div/form/div[1]/div[3]/div/div/div/div/div[1]/div[2]/button[2]')
            increase_adults.click()

    def click_search(self):
        button_pesquisar = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        button_pesquisar.click()

    def drop_popup(self):
        try:
            popup = self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Ignorar informações de login."]')
            popup.click()
        except NoSuchElementException:
            pass

    def apply_filtrations(self):
        filtration = BookingFiltration(driver=self.driver)
        filtration.apply_star_rating(3, 4, 5)
        sorting = BookingFiltration(driver=self.driver)
        sorting.sort_price_lowest_first()

    def report_results(self):
        hotel_boxes = self.driver.find_element(By.ID, 'search_results_table')
        report = BookingReport(hotel_boxes)
        table_results = PrettyTable(
            field_names=['Hotel Name', 'Hotel Price', 'Hotel Score']
        )
        table_results.add_rows(report.pull_deal_box_attributes())
        print('Reporting the results: ')
        print(table_results)
