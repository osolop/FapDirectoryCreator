import praw
import requests
from os.path import expanduser
from pathlib import Path
import argparse


def check_dir():
    fap_path = Path(expanduser('~'))/Path('fap_dir')
    if fap_path.exists():
        return fap_path
    else:
        Path.mkdir(fap_path)
        return fap_path


def download_stuff(submission):
    response = requests.get(submission.url)
    filename = '_'.join(submission.title.split())
    if response.status_code == 200:
        print('Downloading %s...' % (filename))
        dest = check_dir() / Path(filename)
        try:
            with open(str(dest), 'wb') as fo:
                for chunk in response.iter_content(4096):
                        fo.write(chunk)
        except:
            pass


def parse_args():
    parser = argparse.ArgumentParser(description="Parse arguments")
    parser.add_argument('-id', type=str, help="Client ID", required=True)
    parser.add_argument('-secret', type=str, help="Client secret", required=True)
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    reddit = praw.Reddit(client_id=args.id,
                         client_secret=args.secret,
                         user_agent='Download content to local machine.')
    for submission in reddit.subreddit('The_Best_NSFW_GIFS').hot(limit=20):
        download_stuff(submission)


if __name__ == '__main__':
    main()
