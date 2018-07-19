import smtplib, sqlite3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase

def main():
    conn = sqlite3.connect('urlscan.db')
    c = conn.cursor()
    c.execute('SELECT url FROM urls WHERE email_sent=(?) AND url LIKE (?)', ('NO', '%file%'))
    results = c.fetchall()

    if results:
        with open ('links.txt', 'w') as f:
            for link in results:
                f.write(link[0] + '\n')
            f.close()

        msg = MIMEMultipart()
        msg['To'] = 'recipient@email.here'
        msg['From'] = 'Google Driveby'
        msg['Subject'] = 'Open Google Drive Files'
        msg.attach(MIMEText("Hello, please find attached a list of open Google Drive files."))

        part = MIMEBase('application', "octet-stream")
        part.set_payload(open('links.txt', "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="links.txt"')
        msg.attach(part)

        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.starttls()
        gmail.login('change.me@gmail.com','PASSWORD')
        gmail.sendmail("change.me@gmail.com", "recipient@email.here", msg.as_string())
        gmail.quit()

        c.execute('UPDATE urls SET email_sent=(?) WHERE email_sent=(?) AND url LIKE (?)', ('YES', 'NO', '%file%'))
        conn.commit()

    conn.close()

if __name__ == '__main__':
    main()