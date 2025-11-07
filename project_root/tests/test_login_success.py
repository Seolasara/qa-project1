import time
from src.pages.login_page import LoginPage

def test_helpychat_login(driver,login):
    assert "qaproject.elice.io" in driver.current_url
    print("✅ HelpyChat 로그인 성공!")