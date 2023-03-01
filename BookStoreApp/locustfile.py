from locust import HttpUser, task


class HomePageLoadTest(HttpUser):

    @task
    def home_page(self):
        self.client.get("/")

    @task
    def home_page(self):
        self.client.get("book_detail/book1/")