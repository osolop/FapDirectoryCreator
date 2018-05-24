import praw
import requests
from os.path import expanduser
from pathlib import Path
import argparse
import re


def check_dir():
    fap_path = Path(expanduser('~'))/Path('fap_dir')
    if fap_path.exists():
        return fap_path
    else:
        Path.mkdir(fap_path)
        return fap_path


def fix_title(title):
    filename = '_'.join(title.split())
    return re.sub("[\(\[].*?[\)\]]", "", filename)

def download_stuff(submission):
    response = requests.get(submission.url, stream=True, allow_redirects=True)
    print(submission.url)
    # print(submission.title)
    filename = fix_title(submission.title)
    print(dir(response.url))
    # print(response.headers['content-type'])
    # print(response)
    if response.status_code == 200:
        print('Downloading %s...' % (filename))
        dest = check_dir() / Path(filename)
        # try:
        with open(str(dest), 'wb') as fo:
            for chunk in response.iter_content(4096):
                    fo.write(chunk)
                    fo.flush()
        # except:
            # pass


def parse_args():
    parser = argparse.ArgumentParser(description="Parse arguments")
    parser.add_argument('-id', type=str, help="Client ID", required=True)
    parser.add_argument('-secret', type=str, help="Client secret", required=True)
    parser.add_argument('-category', type=str, help="Category reddit", default='The_Best_NSFW_GIFS')
    parser.add_argument('-hot_count', type=int, help="Hot posts count", default=1)
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    reddit = praw.Reddit(client_id=args.id,
                         client_secret=args.secret,
                         user_agent='Download content to local machine.')
    for submission in reddit.subreddit(args.category).hot(limit=args.hot_count):
        download_stuff(submission)


if __name__ == '__main__':
    main()
