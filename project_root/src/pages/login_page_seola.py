from selenium.webdriver.common.by import By

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.email_field = (By.NAME, "loginId")
        self.pw_field = (By.NAME, "password")
        self.login_button = (By.XPATH, "//button[text()='로그인']")

    def input_email(self, email):
        self.driver.find_element(*self.email_field).send_keys(email)

    def input_password(self, password):
        self.driver.find_element(*self.pw_field).send_keys(password)

    def click_login_button(self):
        self.driver.find_element(*self.login_button).click()

    def login(self, email, password):
        self.input_email(email)
        self.input_password(password)
        self.click_login_button()