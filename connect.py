#!/usr/bin/env python

import datetime
import sys
from collections import defaultdict

from mailsnake import MailSnake
from rapleafApi import RapleafApi

def main(mailchimp_key, list_id, rapleaf_key):
    
    thirty_days_ago = datetime.datetime.now() - datetime.timedelta(days=30)
    ms = MailSnake(mailchimp_key)
    rapleaf = RapleafApi.RapleafApi(rapleaf_key)
    
    members = ms.listMembers(id=list_id, limit=1500)['data']
    
    active_members = []
    for member in members:
        member_activity = ms.listMemberActivity(id=list_id, email_address=member['email'])
        actions = [action for action in member_activity['data'][0] if action['action'] == 'open']
        if actions:
            last_action = actions[0]
            last_event = datetime.datetime.strptime(last_action['timestamp'], "%Y-%m-%d %H:%M:%S")
            if last_event > thirty_days_ago:
                active_members.append(member['email'])
    
    age_map = defaultdict(int)
    for active_member in active_members:
        try:
            response = rapleaf.query_by_email(active_member)
            age = response.get("age")
            age_map[age] += 1
            # for k, v in response.iteritems():
            #     print '%s = %s' % (k, v)
        except Exception as e:
          print e
    for x, y in age_map.iteritems():
        print x, y

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print "Needs Mailchimp API key, List ID, and Rapleaf API key"
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])