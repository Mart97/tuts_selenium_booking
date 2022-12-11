from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

class BookingFiltration:
    """ This class will be responsible to interact
    with our website after the results, to apply filters """
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def apply_star_rating(self, *star_values):
        star_filtration_box = self.driver.find_element(By.CSS_SELECTOR, 'div[data-filters-group="class"]')
        star_child_elements = star_filtration_box.find_elements(By.CSS_SELECTOR, '*')

        for star_value in star_values:
            for star_element in star_child_elements:
                if str(star_element.get_attribute('innerHTML')).strip() == f'{star_value} estrelas':
                    star_element.click()

    def sort_price_lowest_first(self):
        element_button_sort = self.driver.find_element(By.CSS_SELECTOR, 'button[data-testid="sorters-dropdown-trigger"]')
        element_button_sort.click()

        element_lowest_prices = self.driver.find_element(By.CSS_SELECTOR, 'button[data-id="price"]')
        element_lowest_prices.click()