from __future__ import unicode_literals
__author__ = "Jordan Sanders"
"""
Downloads articles in Reddit submissions
"""

def article_text(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text.encode('ascii', 'ignore').decode('ascii')

import cPickle
from optparse import OptionParser
import praw
import os.path
from newspaper import Article
import spacy
from pprint import pprint

def main(options):
    #Load Spacy English Model
    nlp = spacy.load("en")

    #Let Reddit know who we are
    r = praw.Reddit(client_id='wU1FwN1ugWt7eQ',
                     client_secret='BgciYaBpyH8ef21jXMyJjn_DARE',
                     password='XPlstazuMC0CaX1Njhf0ny5u^nMD5t*P73O',
                     user_agent='News Article Downloader /u/JS_Research',
                     username='JS_Research')

    #Verify login
    authenticated_user = r.user.me()
    if authenticated_user.name:
        print "Logged in as "+ authenticated_user.name

    #Get all submissions from a subreddit between a time period
    subreddit = r.subreddit("science")

    submissions = subreddit.submissions(start=options.start,end=options.end)

    all_submissions = list(submissions)
    #Sort submissions by karma value
    all_submissions.sort(key=lambda x: x.score, reverse=True)
    #Find 2 appropriate articles from that week
    count = 0
    for submission in all_submissions:
        #End after finding 2
        if count == 2500:
            break;
        try:
            #Extract URL text
            text = article_text(submission.url)
            #Create spacy doc with text
            article = nlp(text)
        except:
            continue

        #url
        blacklist = ["reddit.com"]
        blacklisted = False
        for url in blacklist:
            if url in submission.url:
                blacklisted = True

        if not blacklisted:
            setattr(submission,"article_text", text)
            out_s = open("articles/" + str(submission.link_flair_text) + "_" + str(submission.id), "wb")
            print submission.link_flair_text
            cPickle.dump(submission,out_s)
            out_s.close()
            count += 1





if __name__ == '__main__':
    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-s", "--start", type=int, default=1479254400,
                      help="Start time in UNIX format")
    parser.add_option("-e", "--end", type=int, default=None,
                      help="Start time in UNIX format")
    options, args = parser.parse_args()
    main(options)
