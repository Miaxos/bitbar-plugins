#!/usr/local/bin/python3

import os
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
import json
import os
import sys
from urllib.request import Request, urlopen
from docopt import docopt
import pprint

load_dotenv(find_dotenv())

DARK_MODE = os.getenv('BitBarDarkMode')

pp = pprint.PrettyPrinter(indent=2)

GITHUB_LOGO = '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'

COLORS = {
    'inactive': '#b4b4b4',
    'mainText': '#ffffff' if DARK_MODE else '#000000',
    'alternativeText': '#b4b4b4',
}

help = '''github-central

Usage:
  github-central.py
  github-central.py <command> <param>

Options:
  -h --help          C'est généré automatiquement.
'''

MY_PRS_QUERY = '''{{
authorPrs: search(query: "type:pr state:open author:{login}", type: ISSUE, first: 100) {{
    edges {{
        node {{
            ... on PullRequest {{
                id
                number
                repository {{
                    nameWithOwner
                }}
                author {{
                    login
                }}
                createdAt
                url
                title
                mergeStateStatus
                state
            }}
        }}
    }}
}}
assigneePrs: search(query: "type:pr state:open assignee:{login}", type: ISSUE, first: 100) {{
    edges {{
        node {{
            ... on PullRequest {{
                id
                number
                repository {{
                    nameWithOwner
                }}
                author {{
                    login
                }}
                createdAt
                url
                title
                mergeStateStatus
                state
            }}
        }}
    }}
}}
}}'''

NOTIFICATIONS_REASON_TO_EMOJIS = {
    'assign': '👨‍💻',
    'author': '👨‍💻',
    'comment': '💬',
    'invitation': '🎉',
    'manual': '👀',
    'mention': '💬',
    'team_mention': '💬',
    'state_change': '🔁',
    'subscribed': '👀',
    'review_requested': '🔍',
}

NOTIFICATIONS_TYPE_TO_ISSUE_PR = {
    'Issue': 'issue',
    'PullRequest': 'pull',
}

MERGE_STATE_EMOJIS = {
    'BEHIND': '❌',
    'BLOCKED': '❌',
    'DIRTY': '❌',
    'CLEAN': '✅',
    'HAS_HOOKS': '⚙️',
    'UNKNOWN': '❔',
    'UNSTABLE': '❌',
}

def strToDate(dateStr):
    return datetime.strptime(dateStr, '%Y-%m-%dT%H:%M:%SZ')


class PullRequests:
    def __init__(self, config):
        self.config = config

        self.prs = {};
        self.repositoryLastActivityDates = {}

    def savePr(self, repositoryName, prId, pr):
        if not repositoryName in self.prs:
            self.prs[repositoryName] = {}

        if not prId in self.prs[repositoryName]:
            self.prs[repositoryName][prId] = pr

    def readResponse(self, prsResponse):
        nodes = prsResponse.get('edges', [])

        for node in nodes:
            nodeData = node.get('node')
            pr = {
                'id': nodeData.get('id'),
                'number': nodeData.get('number'),
                'title': nodeData.get('title'),
                'createdAt': nodeData.get('createdAt'),
                'author': nodeData.get('author').get('login'),
                'mergeStateStatus': nodeData.get('mergeStateStatus'),
                'url': nodeData.get('url'),
                'state': nodeData.get('state'),
            }

            if pr.get('state') != 'OPEN':
                continue

            repositoryName = nodeData.get('repository').get('nameWithOwner')
            self.savePr(repositoryName, pr.get('id'), pr);

    def sort(self):
        for repositoryName in self.prs:
            prs = self.prs[repositoryName]
            self.prs[repositoryName] = sorted(
                prs.values(),
                key=lambda pr: pr.get('createdAt'),
                reverse=True
            )

            self.repositoryLastActivityDates[repositoryName] = max(
                self.prs[repositoryName],
                key=lambda pr: pr.get('createdAt'),
            )

        self.repositoryLastActivityDates = sorted(
            self.repositoryLastActivityDates.items(),
            key=lambda x: x[1]['createdAt'],
            reverse=True
        )

    def request(self, query):
        headers = {
            'Authorization': 'bearer ' + self.config['GITHUB_ACCESS_TOKEN'],
            'Content-Type': 'application/json',
            'Accept': 'application/vnd.github.merge-info-preview+json',
        }
        data = json.dumps({'query': query}).encode('utf-8')

        req = Request(
            'https://api.github.com/graphql',
            data=data,
            headers=headers,
        )

        body = urlopen(req).read()
        return json.loads(body)

    def get(self):
        login = self.config['GITHUB_LOGIN']

        queryBody = MY_PRS_QUERY.format(login=login)

        response = self.request(queryBody)

        authorPrs = response.get('data').get('assigneePrs')
        assigneePrs = response.get('data').get('assigneePrs')

        self.readResponse(authorPrs)
        self.readResponse(assigneePrs)

        self.sort()

    def getEmoji(self, pr):
        status = pr.get('mergeStateStatus')

        return MERGE_STATE_EMOJIS.get(status, '')

    def __str__(self):
        output = []

        if not self.prs:
            output.append('No pull-request| color={}'.format(COLORS['inactive']));
        else:
            output.append('Pull requests| color={}'.format(COLORS['alternativeText']))
            for repositoryName, _ in self.repositoryLastActivityDates:
                output.append('{} |href={} color={}'.format(
                    repositoryName,
                    'https://github.com/{}/pulls'.format(repositoryName),
                    COLORS['alternativeText'],
                ))

                prs = self.prs[repositoryName]

                for pr in prs:
                    output.append('{} #{} {} | href={} color={}'.format(
                        self.getEmoji(pr),
                        pr.get('number'),
                        pr.get('title'),
                        pr.get('url'),
                        COLORS['mainText']
                    ))

                output.append('---')

        return '\n'.join(output)

class Notifications:
    def __init__(self, config):
        self.config = config

        self.notifications = {}
        self.repositoryLastActivityDates = {}
        self.nbNotifications = 0

    def request(self):
        headers = {
            'Authorization': 'bearer ' + self.config['GITHUB_ACCESS_TOKEN'],
            'Content-Type': 'application/json',
        }
        req = Request(
            'https://api.github.com/notifications',
            headers=headers,
        )
        body = urlopen(req).read()
        return json.loads(body)

    def save(self, repositoryName, notification):
        if not repositoryName in self.notifications:
            self.notifications[repositoryName] = []

        self.notifications[repositoryName].append(notification)
        self.nbNotifications += 1

    def sort(self):
        for repositoryName in self.notifications:
            notifications = self.notifications[repositoryName]
            self.notifications[repositoryName] = sorted(
                notifications,
                key=lambda notification: notification['lastActivityDate'],
                reverse=True
            )

            self.repositoryLastActivityDates[repositoryName] = max(
                self.notifications[repositoryName],
                key=lambda notification: notification['lastActivityDate'],
            )

        self.repositoryLastActivityDates = sorted(
            self.repositoryLastActivityDates.items(),
            key=lambda x: x[1]['lastActivityDate'],
            reverse=True,
        )

    def get(self):
        response = self.request()

        for notification in response:
            threadId = notification.get('id')
            lastActivityDate = notification.get('updated_at')
            reason = notification.get('reason')

            title = notification.get('subject').get('title')
            url = notification.get('subject').get('url')
            notificationType = notification.get('subject').get('type')

            repositoryName = notification.get('repository').get('full_name')

            self.save(repositoryName, {
                'threadId': threadId,
                'lastActivityDate': strToDate(lastActivityDate),
                'reason': reason,
                'title': title,
                'url': url,
                'type': notificationType,
                'repositoryName': repositoryName,
            });

        self.sort()

    def getReasonEmoji(self, notification):
        return NOTIFICATIONS_REASON_TO_EMOJIS.get(
            notification.get('reason'),
            '?',
        )

    def getLink(self, notification):
        urlParts = notification.get('url').split('/')
        prOrIssueId = urlParts[-1]

        thing = NOTIFICATIONS_TYPE_TO_ISSUE_PR.get(
            notification.get('type')
        )

        if not thing:
            return 'https://github.com/notifications'

        return 'https://github.com/{}/{}/{}'.format(
            notification['repositoryName'],
            thing,
            prOrIssueId,
        )

    def getMarkReadCommand(self, notification):
        scriptPath = os.path.realpath(__file__)

        return (
            scriptPath,
            'read-notification',
            notification.get('threadId'),
        )

    def __str__(self):
        output = []

        notificationsLink = 'http://github.com/notifications'

        if not self.nbNotifications:
            output.append('No notification | color={} href={}'.format(
                COLORS['inactive'],
                notificationsLink,
            ))
        else:
            output.append('{} notifications | color={} href={}'.format(
                self.nbNotifications,
                COLORS['alternativeText'],
                notificationsLink,
            ))

        for repositoryName, _ in self.repositoryLastActivityDates:
            output.append('--{}'.format(repositoryName))

            notifications = self.notifications[repositoryName]

            for notification in notifications:
                output.append('--{} {} | href={} color={}'.format(
                    self.getReasonEmoji(notification),
                    notification['title'],
                    self.getLink(notification),
                    COLORS['mainText'],
                ))
                output.append('----Read ↗️ | href={} color={}'.format(
                    self.getLink(notification),
                    COLORS['mainText']
                ))

                (command, param1, param2) = self.getMarkReadCommand(notification)
                output.append('----Mark as read| bash={} param1={} param2={} terminal=false refresh=true color={}'.format(
                    command,
                    param1,
                    param2,
                    COLORS['mainText']
                ))

            output.append('-----')

        output.append('---')
        return '\n'.join(output)

    def readNotification(self, notificationId):
        headers = {
            'Authorization': 'bearer ' + self.config['GITHUB_ACCESS_TOKEN'],
        }
        url = 'https://api.github.com/notifications/threads/{}'.format(notificationId)

        req = Request(
            url,
            headers=headers,
        )
        req.get_method = lambda: 'PATCH'

        body =  urlopen(req).read()

        pp.pprint(body)

if __name__ == '__main__':
    config = {}
    config['GITHUB_ACCESS_TOKEN'] = os.getenv('GITHUB_ACCESS_TOKEN')
    config['GITHUB_LOGIN'] = os.getenv('GITHUB_LOGIN')

    args = docopt(help)

    notifications = Notifications(config)
    pullRequests = PullRequests(config)

    if args['<command>'] == 'read-notification':
        notifications.readNotification(args['<param>'])

    notifications.get()
    notificationsTitle = '{}⚑'.format(notifications.nbNotifications) if notifications.nbNotifications else ''

    pullRequests.get()

    print('{}|templateImage={} color={}'.format(
        notificationsTitle,
        GITHUB_LOGO,
        COLORS['mainText'],
    ))
    print('---')

    print(str(notifications))
    print(str(pullRequests))
