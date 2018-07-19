import signal, requests, sqlite3, time, slack_poster
from selenium import webdriver

class TimeoutException(Exception):
  pass

def TimeoutHandler(signum, frame):
  raise TimeoutException


def main():
    conn = sqlite3.connect('urlscan.db')
    c = conn.cursor()
    for url in requests.get('https://urlscan.io/api/v1/search/?q=domain:drive.google.com').json()['results']:
        url = url['task']['url']
        c.execute('SELECT url FROM urls WHERE url=(?)', [url])
        if c.fetchone() == None:
            if (url.split(".")[1]) == "google":
                take_screenshot(url)
                slack_poster.post_image(url)
                with open('screenshot.png', 'rb') as image:
                    data = [url, time.time(), image.read(), 'NO', None]
                    c.execute('INSERT INTO urls VALUES (?, ?, ?, ?, ?)', data)
        conn.commit()
    conn.close()

def take_screenshot(url):

    OriginalHandler = signal.signal(signal.SIGALRM, TimeoutHandler)
    signal.alarm(30)

    try:
        driver = webdriver.Firefox()
        driver.get(url)
        time.sleep(10)
        driver.save_screenshot('screenshot.png')
        driver.quit()

    except TimeoutException:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, OriginalHandler)
        return

if __name__ == '__main__':
    main()