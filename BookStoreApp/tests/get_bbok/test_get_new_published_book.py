from selenium.webdriver.common.by import By
from tests.conftest import TestBaseConfig


class TestGetBestSellerBook(TestBaseConfig):

    def test_get_best_seller_book(self):

        book_title = self.driver.find_element(By.XPATH, '((//*[@class="item active"])[2]/child::*)[1]//h2')

        book_title_text = book_title.text

        get_book_btn = self.driver.find_element(By.XPATH, "//*[text()='مشاهده کتاب']")
        get_book_btn.click()

        book_title_target = self.driver.find_element(By.XPATH, '(//*[@class="product-information"])/child::*[2]/h2')
        book_title_target_text = book_title_target.text

        assert book_title_text == book_title_target_text

        add_to_card_btn = self.driver.find_element(By.XPATH, '//*[text()="افـزودن به سبـد خریـد"]')
        assert 'افـزودن به سبـد خریـد' in add_to_card_btn.text
