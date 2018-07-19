import requests

def main():
    return

def post_image(url):
    token = 'YOUR-SLACK-API-TOKEN-HERE'
    f = {'file': ('screenshot.png', open('screenshot.png', 'rb'), 'image/png', {'Expires':'0'})}
    response = requests.post(url='https://slack.com/api/files.upload', data=
       {'token': token, 'channels': '#google-driveby', 'media': f, 'initial_comment': url},
       headers={'Accept': 'application/json'}, files=f)

    return response.text

if __name__ == '__main__':
    main()