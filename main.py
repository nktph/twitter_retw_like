from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from mails import email_parsers
def start_account(need, username, password, mail, mail_password, url):
    driver = webdriver.Chrome()
    print()
    # Открытие страницы для входа в аккаунт
    driver.get('https://twitter.com/login')
    time.sleep(2)

    # Вход в аккаунт
    username_input = driver.find_element('xpath', '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input')
    username_input.send_keys(username)
    driver.find_element('xpath', '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div/span/span').click()
    time.sleep(4)
    password_input = driver.find_element('xpath', '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
    password_input.send_keys(password)
    password_input.send_keys(Keys.ENTER)
    time.sleep(5)
    if "login" in driver.current_url:
        code = ""
        print("Потребовалось подтверждение с почты, ждём некоторое время")
        time.sleep(10)
        print(mail)
        print("Проверяем почтовый ящик")
        if "mail.ru" in mail:
            code = email_parsers.get_code(mail, mail_password, email_parsers.MAIL_RU)
        elif "outlook.com" in mail:
            code = email_parsers.get_code(mail, mail_password, email_parsers.OUTLOOK)
        elif "gmail.com" in mail:
            code = email_parsers.get_code(mail, mail_password, email_parsers.GMAIL)
        else:
            print("Неизвесный почтовый домен, пропускаем аккаунт")
            return
        if code:
            print(f"Код: {code}")
            code_input = driver.find_element('xpath', '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input')
            code_input.click()
            code_input.send_keys(code)
            btn = driver.find_element('xpath', '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div/span/span')
            btn.click()
            time.sleep(5)
        else:
            print("Не удалось получить код подтверждения, пропускаем аккаунт")

    driver.get(url)
    time.sleep(5)
    likes = driver.find_elements('css selector', '[data-testid="like"]')
    retweet = driver.find_elements('css selector', '[data-testid="retweet"]')

    likes_count = [i.text for i in likes]
    retweet_count = [i.text for i in retweet]

    count = len(likes_count) if len(likes_count) < len(retweet_count) else len(retweet_count)
    while need > 0:
        for i in range(count):
            if need == 0:
                break
            driver.execute_script("arguments[0].scrollIntoView(true);", retweet[i])
            time.sleep(0.6)
            driver.execute_script("window.scrollBy(0, -200);")
            retweet[i].click()
            time.sleep(0.6)
            driver.find_element('css selector', '[data-testid="retweetConfirm"]').click()
            time.sleep(0.6)
            driver.execute_script("arguments[0].scrollIntoView(true);", likes[i])
            time.sleep(0.6)
            driver.execute_script("window.scrollBy(0, -200);")
            driver.execute_script("arguments[0].click();",  likes[i])
            time.sleep(0.6)
            need -= 1

        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(5)

        likes = driver.find_elements('css selector', '[data-testid="like"]')
        retweet = driver.find_elements('css selector', '[data-testid="retweet"]')

        count = len(likes) if len(likes) < len(retweet) else len(retweet)

    driver.quit()

# Открытие профиля пользователя
#profile_url = 'https://twitter.com/имя_пользователя'
#driver.get(profile_url)
#time.sleep(3)
#
## Лайкинг первых 10 твитов
#tweets = driver.find_element('xpath', '//div[@data-testid="tweet"]')
#for tweet in tweets[:10]:
#    like_button = tweet.find_element('xpath', './/div[@data-testid="like"]')
#    like_button.click()
#    time.sleep(2)
#
## Закрытие браузера
