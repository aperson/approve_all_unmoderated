#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import praw
from praw.handlers import MultiprocessHandler

try:
    from config import *  # NOQA
except:
    USERNAME = 'someuser'
    PASSWORD = 'somepass'


class Bot(object):
    def __init__(self, username, password):
        user_agent = '/u/{} running approve_all_unmoderated.py'.format(username)
        self.r = praw.Reddit(user_agent, handler=MultiprocessHandler())
        self.r.login(username, password)

    def accept_mod_invites(self):
        '''Accepts all moderator invites.'''

        for message in self.r.get_unread(limit=None):
            message.mark_as_read()
            # lets assume every message is a mod-invite
            try:
                self.r.accept_moderator_invite(message.subreddit.display_name)
            except praw.errors.InvalidInvite:
                pass

    def approve_all_unmoderated(self):
        '''Goes through subreddits individually and then approves all submission, then demods'''

        for subreddit in self.r.get_my_moderation(limit=None):
            for thing in subreddit.get_unmoderated(limit=None):
                thing.approve()
            subreddit.remove_moderator(self.r.user.name)

    def run(self):
        self.accept_mod_invites()
        self.approve_all_unmoderated()

if __name__ == '__main__':
    bot = Bot(USERNAME, PASSWORD)
    bot.run()
