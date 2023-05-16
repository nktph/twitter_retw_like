from selenium import webdriver
from selenium.common import ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
import time
from mails import email_parsers
def start_account(need, username, password, mail, mail_password, url):
    driver = webdriver.Chrome()
    print()
    # Открытие страницы для входа в аккаунт
    driver.get('https://twitter.com/login')
    time.sleep(4)

    # Вход в аккаунт
    try:
        username_input = driver.find_element('xpath', '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input')
        username_input.send_keys(username)
        driver.find_element('xpath', '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div/span/span').click()
        time.sleep(5)
        password_input = driver.find_element('xpath', '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
        password_input.send_keys(password)
        time.sleep(0.3)
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
                return 0,0
    except:
        print("При авторизации возникла ошибка, пропускаем аккаунт")
        driver.quit()
        return 0,0

    try:
        driver.get(url)
        time.sleep(5)
        likes = driver.find_elements('css selector', '[data-testid="like"]')
        retweet = driver.find_elements('css selector', '[data-testid="retweet"]')

        likes_count = [i.text for i in likes]
        retweet_count = [i.text for i in retweet]
    except:
        print("Не удалось получить разметку лайков/ретвитов, переходим к следующему аккаунту")
        driver.quit()
        return 0,0

    success_tweets = 0
    success_likes = 0

    try:
        count = min(len(likes_count), len(retweet_count))
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
                success_tweets += 1
                time.sleep(2)
                if 'Unlock more on Twitter' in driver.page_source:
                    print('Уведомление')
                    time.sleep(2)
                    driver.find_element('xpath', '//*[@id="layers"]/div[3]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[3]/div').click()
                    print('Убрано')

                time.sleep(0.6)
                driver.execute_script("arguments[0].scrollIntoView(true);", likes[i])
                time.sleep(0.6)
                driver.execute_script("window.scrollBy(0, -200);")
                driver.execute_script("arguments[0].click();",  likes[i])
                success_likes += 1
                time.sleep(0.6)
                need -= 1

            driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(5)

            likes = driver.find_elements('css selector', '[data-testid="like"]')
            retweet = driver.find_elements('css selector', '[data-testid="retweet"]')
    except:
        print("Произошла неизвестная ошибка, переходим на следующий аккаунт")
        driver.quit()
        return [success_likes, success_tweets]
        # count = min(len(likes_count), len(retweet_count))

    driver.quit()
    return [success_likes, success_tweets]
