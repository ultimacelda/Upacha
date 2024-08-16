# fetching.py
from datetime import datetime, timezone
import imapclient
from imapclient import IMAPClient
import email
from email.header import decode_header
from django.core.files.base import ContentFile
from django.utils.dateparse import parse_datetime
from .models import Letter, Mail

def get_imap_server(email):
    if 'gmail.com' in email:
        return 'imap.gmail.com'
    elif 'yandex.ru' in email:
        return 'imap.yandex.ru'
    elif 'mail.ru' in email:
        return 'imap.mail.ru'
    else:
        raise ValueError('Unsupported email domain')

def fetch_emails(email_address, password, server_address):
    try:
        server = IMAPClient(server_address, ssl=True)
        server.login(email_address, password)
        server.select_folder('INBOX')

        messages = server.search('ALL')
        mail_instance = Mail.objects.get(login=email_address)
        last_uid = mail_instance.last_uid
        new_messages_added = False

        for uid, message_data in server.fetch(messages, 'RFC822').items():
            if last_uid and uid <= last_uid:
                continue  # Пропустить сообщения, которые уже были обработаны

            msg = email.message_from_bytes(message_data[b'RFC822'])
            subject = decode_header(msg['Subject'])[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode('utf-8', errors='ignore')
            posting_time_str = msg['Date']
            posting_time = parse_datetime(posting_time_str)

            if posting_time is None:
                print(f"Warning: Could not parse posting time from {posting_time_str}")
                posting_time = datetime.now(timezone.utc)
            text = ''
            attachment = None
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    if "attachment" in content_disposition:
                        filename = part.get_filename()
                        if filename:
                            attachment_data = part.get_payload(decode=True)
                            attachment = ContentFile(attachment_data, name=filename)
                    elif content_type == "text/plain":
                        text = part.get_payload(decode=True).decode('utf-8', errors='ignore')
            else:
                text = msg.get_payload(decode=True).decode('utf-8', errors='ignore')

            letter = Letter.objects.create(
                subject=subject,
                posting_time=posting_time,
                receiving_time=datetime.now(timezone.utc),
                text=text,
                mail=mail_instance  
            )

            if attachment:
                letter.attachment.save(attachment.name, attachment)

            letter.save()
            new_messages_added = True
            mail_instance.last_uid = uid  # Обновляем последний обработанный UID
            mail_instance.save() 

        return {"status": "completed", "new_messages": new_messages_added}

    except imapclient.exceptions.LoginError:
        return {"status": "auth_error"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
