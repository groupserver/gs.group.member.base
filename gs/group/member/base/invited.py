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
from logging import getLogger
from zope.cachedescriptors.property import Lazy
from .listabc import MemberListABC
from .queries import InvitedMemberQuery

#: The logger for this module
log = getLogger('gs.group.member.base.moderated')


class InvitedMembers(MemberListABC):
    '''The list of group members that have been invited to join the group'''

    @Lazy
    def query(self):
        retval = InvitedMemberQuery()
        return retval

    @property
    def invitedMemberIds(self):
        return self.subsetIds

    @Lazy
    def subsetIds(self):
        retval = set()

        invitedIds = set(self.query.invited_members(self.siteInfo.id, self.groupInfo.id))
        for uId in invitedIds.intersection(self.memberIds):
            m = 'The user ID %s is listed as an invited member in the group %s (%s) on the '\
                'site %s (%s), but is already a member of the group.'
            log.warn(m, uId, self.groupInfo.name, self.groupInfo.id, self.siteInfo.name,
                     self.siteInfo.id)
        # The Manage members page relies on all the invited members being returned
        retval = invitedIds  # invitedIds.difference(self.memberIds)
        return retval
