from selenium.webdriver.common.by import By
from tests.conftest import TestBaseConfig


class Test_GetBestSellerBook(TestBaseConfig):

    def test_get_best_seller_book(self):

        book_title = self.driver.find_element(By.XPATH, '//*[@id="recommended-item-carousel"]/div/div/div/div/div/div/h2')
        book_title_text = book_title.text

        get_book_btn = self.driver.find_element(By.XPATH, "//*[text()='مشاهده کتاب']")
        get_book_btn.click()

        book_title_target = self.driver.find_element(By.XPATH, '/html/body/section/div/div/div[1]/div[1]/div[2]/div/div[1]/h2')
        book_title_target_text = book_title_target.text

        assert book_title_text == book_title_target_text

        add_to_card_btn = self.driver.find_element(By.XPATH, "/html/body/section/div/div/div[1]/div[1]/div[2]/div/div[2]/form/span/button")

        assert "افـزودن به سبـد خریـد" in add_to_card_btn.text
