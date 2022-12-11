from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException


class BookingReport:
    def __init__(self, boxes_section_element: WebElement):
        self.boxes_section_element = boxes_section_element
        self.deal_boxes = self.pull_deal_boxes()

    def pull_deal_boxes(self):
        return self.boxes_section_element.find_elements(By.CSS_SELECTOR,
                                                        'div[data-testid="property-card"]')

    def pull_deal_box_attributes(self):
        collection = []

        for deal_box in self.deal_boxes:
            # Pulling the hotel name
            hotel_name = deal_box.find_element(By.CSS_SELECTOR,
                                               'div[data-testid="title"]').get_attribute('innerHTML').strip()

            # Pulling the hotel price
            hotel_price = deal_box.find_element(By.CSS_SELECTOR,
                                                'span[data-testid="price-and-discounted-price"]').get_attribute(
                'innerHTML').strip()
            hotel_price = hotel_price.replace('&nbsp;', ' ')

            # Pulling the hotel rate
            try:
                hotel_score = deal_box.find_element(By.CSS_SELECTOR,
                                                    'div[class="b5cd09854e d10a6220b4"]').get_attribute(
                    'innerHTML').strip()
            except NoSuchElementException:
                hotel_score = deal_box.find_element(By.XPATH,
                                                    '//*[@id="search_results_table"]/div[2]/div/div/div/div[5]/div[2]/div[1]/div[2]/div/div[1]/div[2]/div/a/span/div/div[1]')

            if 'selenium.webdriver.remote.webelement.WebElement' in str(hotel_score):
                hotel_score = 'N/A'

            collection.append([hotel_name, hotel_price, hotel_score])  # tip: create a list to append lists of items

        return collection
