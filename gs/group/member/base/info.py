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
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from zope.interface import implements
from Products.XWFCore.XWFUtils import sort_by_name
from Products.GSGroupMember.groupmembership import GroupMembers, InvitedGroupMembers
from Products.GSGroupMember.interfaces import IGSGroupMembersInfo
from .admins import (SiteAdminMembers, GroupAdminMembers, AdminMembers, )
from .blocked import BlockedMembers
from .members import AllMembers
from .moderated import ModeratedMembers
from .moderator import Moderators
from .posting import PostingMembers
from .verified import (VerifiedMembers, UnverifiedMembers, )

import logging
log = logging.getLogger('GSGroupMembersInfo')


class GSGroupMembersInfo(object):
    implements(IGSGroupMembersInfo)

    def __init__(self, group):
        self.context = self.group = group
        assert self.context

    @Lazy
    def mlistInfo(self):
        retval = createObject('groupserver.MailingListInfo', self.group)
        return retval

    @Lazy
    def groupInfo(self):
        retval = self.mlistInfo.groupInfo
        return retval

    @Lazy
    def siteInfo(self):
        retval = createObject('groupserver.SiteInfo', self.group)
        return retval

    # TODO: Add a "normalMembers" property (full members - ptnCoach - admin)

    @Lazy
    def groupMembers(self):
        retval = GroupMembers(self.context)
        return retval

    @Lazy
    def sortedMembers(self):
        retval = self.fullMembers
        retval.sort(sort_by_name)
        return retval

    @Lazy
    def fullMembers(self):
        members = self.groupMembers.members
        return members

    @property
    def fullMemberCount(self):
        retval = len(self.groupMembers)
        return retval

    @Lazy
    def invitedMembers(self):
        retval = InvitedGroupMembers(self.context, self.siteInfo).members
        return retval

    @property
    def invitedMemberCount(self):
        return len(self.invitedMembers)

    @Lazy
    def members(self):
        retval = AllMembers(self.groupInfo.group)
        return retval

    @Lazy
    def memberIds(self):
        retval = [m.id for m in self.members]
        return retval

    @Lazy
    def ptnCoach(self):
        ptnCoachId = self.groupInfo.get_property('ptn_coach_id', '')
        retval = None
        if ptnCoachId and (ptnCoachId in self.memberIds):
            retval = createObject('groupserver.UserFromId', self.context, ptnCoachId)
        return retval

    @Lazy
    def groupAdmins(self):
        retval = GroupAdminMembers(self.groupInfo.group)
        return retval

    @Lazy
    def siteAdmins(self):
        retval = SiteAdminMembers(self.groupInfo.group)
        return retval

    @Lazy
    def managers(self):
        retval = AdminMembers(self.groupInfo.group)
        return retval

    @Lazy
    def moderators(self):
        retval = Moderators(self.groupInfo.group)
        return retval

    @Lazy
    def moderatees(self):
        retval = ModeratedMembers(self.groupInfo.group)
        return retval

    @Lazy
    def postingMembers(self):
        retval = PostingMembers(self.groupInfo.group)
        return retval

    @Lazy
    def blockedMembers(self):
        retval = BlockedMembers(self.groupInfo.group)
        return retval

    @Lazy
    def unverifiedMembers(self):
        retval = UnverifiedMembers(self.groupInfo.group)
        return retval

    @Lazy
    def verifiedMembers(self):
        retval = VerifiedMembers(self.groupInfo.group)
        return retval
