#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import praw

try:
    from config import *  # NOQA
except:
    USERNAME = 'someuser'
    PASSWORD = 'somepass'
    CLIENT_ID = 'someid'
    CLIENT_SECRET = 'somesecret'


class Bot(object):
    def __init__(self, username, password, client_id, client_secret):
        user_agent = '/u/{} running approve_all_unmoderated.py'.format(username)
        self.r = praw.Reddit(client_id=client_id, client_secret=client_secret,
            user_agent=user_agent, username=username, password=password)

    def accept_mod_invites(self):
        '''Accepts all moderator invites.'''

        for message in self.r.inbox.unread(limit=None):
            message.mark_read()
            subreddit = self.r.subreddit(message.subreddit)
            if message.was_comment == False:
                if message.distinguished == 'moderator':
                    # lets assume every message is a mod-invite
                    try:
                        subreddit.mod.accpet_invite()
                    except praw.exceptions.APIException:
                        pass

    def approve_all_unmoderated(self):
        '''Goes through subreddits individually and then approves all submission, then demods'''

        for subreddit in self.r.user.moderator_subreddits(limit=None):
            for thing in [i for i in subreddit.mod.unmoderated(limit=None)]:
                thing.mod.approve()
            subreddit.moderator.leave()

    def run(self):
        self.accept_mod_invites()
        self.approve_all_unmoderated()

if __name__ == '__main__':
    bot = Bot(USERNAME, PASSWORD, CLIENT_ID, CLIENT_SECRET)
    bot.run()
