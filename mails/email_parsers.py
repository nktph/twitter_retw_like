import imaplib
import email

MAIL_RU = ("imap.mail.ru", "INBOX/Newsletters")
OUTLOOK = ("outlook.office365.com", "INBOX")
GMAIL = ("imap.gmail.com", "INBOX")


def read_mail(username, password, mail_service):
    server = imaplib.IMAP4_SSL(mail_service[0], 993)
    server.login(username, password)
    server.select(mail_service[1])

    senders = []
    subjects = []

    _, data = server.search(None, 'UNSEEN')
    email_ids = data[0].split()
    if email_ids:
        latest_email_id = email_ids[-1]  # Получаем ID последнего непрочитанного письма
        _, msg_data = server.fetch(latest_email_id, '(RFC822)')
        raw_email = msg_data[0][1]
        email_message = email.message_from_bytes(raw_email)

        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    part.get_payload(decode=True).decode('utf-8')
                    # Извлекаем имя отправителя
                    sender = email_message["From"]
                    senders.append(sender)

                    # Извлекаем тему письма
                    subject = email_message["Subject"]
                    subjects.append(subject)

        else:
            sender = email_message["From"]
            senders.append(sender)

            subject = email_message["Subject"]
            subjects.append(subject)

    server.close()
    server.logout()

    return senders, subjects


def get_code(login, password, server):
    if "gmail" in server[0]:
        code = input(f"Введите код пришедший на почту {login}:")
        return str(code)
    else:
        senders, subjects = read_mail(login, password, server)
        try:
            if "info@twitter" in senders[0]:
                code = subjects[0][len(subjects[0])-8:len(subjects[0])]
                print(f"Получено письмо с темой {subjects[0]}")
                return str(code)
            else:
                print(f"У последнего полученного письма отправитель не Twitter: {senders[0]}")
                return None
        except IndexError:
            print("Новых писем на почте не обнаружено")
            return None
