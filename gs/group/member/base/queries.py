# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2009, 2010, 2011, 2012, 2016 OnlineGroups.net and
# Contributors.
#
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
from __future__ import absolute_import, unicode_literals, print_function
import sqlalchemy as sa
from gs.database import getTable, getSession


class InvitedMemberQuery(object):
    def __init__(self):
        self.userInvitationTable = getTable('user_group_member_invitation')

    def invited_members(self, siteId, groupId):
        if not siteId:
            raise ValueError('Site ID required')
        if not groupId:
            raise ValueError('Group ID required')
        uit = self.userInvitationTable
        s = sa.select([uit.c.user_id.distinct()])
        s.append_whereclause(uit.c.site_id == siteId)
        s.append_whereclause(uit.c.group_id == groupId)
        s.append_whereclause(uit.c.withdrawn_date == None)
        s.append_whereclause(uit.c.response_date == None)

        session = getSession()
        r = session.execute(s)
        retval = []
        if r.rowcount:
            retval = [x['user_id'] for x in r]
        assert type(retval) == list
        return retval