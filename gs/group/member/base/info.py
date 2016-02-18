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
from operator import attrgetter
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from .admins import (SiteAdminMembers, GroupAdminMembers, AdminMembers, )
from .blocked import BlockedMembers
from .invited import InvitedMembers
from .members import (AllMembers, NormalMembers, FullMembers, )
from .moderated import ModeratedMembers
from .moderator import Moderators
from .posting import PostingMembers
from .verified import (VerifiedMembers, UnverifiedMembers, )


class GroupMembersInfo(object):

    def __init__(self, group):
        self.context = self.group = group
        assert self.context

    @Lazy
    def groupInfo(self):
        retval = createObject('groupserver.GroupInfo', self.group)
        return retval

    @Lazy
    def siteInfo(self):
        retval = createObject('groupserver.SiteInfo', self.group)
        return retval

    @Lazy
    def mlistInfo(self):
        retval = createObject('groupserver.MailingListInfo', self.group)
        return retval

    @Lazy
    def normalMembers(self):
        retval = NormalMembers(self.groupInfo.groupObj)
        return retval

    @Lazy
    def members(self):
        retval = self.groupMembers
        return retval

    @Lazy
    def groupMembers(self):
        retval = AllMembers(self.groupInfo.groupObj)
        return retval

    @Lazy
    def sortedMembers(self):
        '''All the users in a group, sorted by name

.. warning:: Can be slow and use memory because it has to pull all the user-objects'''
        retval = list(self.groupMembers)
        retval.sort(key=attrgetter('name'))
        return retval

    @Lazy
    def fullMembers(self):
        retval = FullMembers(self.groupInfo.groupObj)
        return retval

    @Lazy
    def invitedMembers(self):
        retval = InvitedMembers(self.groupInfo.groupObj)
        return retval

    @Lazy
    def ptnCoach(self):
        retval = None
        if self.normalMembers.ptnCoachId:
            retval = createObject('groupserver.UserFromId', self.context,
                                  self.normalMembers.ptnCoachId)
        return retval

    @Lazy
    def groupAdmins(self):
        retval = GroupAdminMembers(self.groupInfo.groupObj)
        return retval

    @Lazy
    def siteAdmins(self):
        retval = SiteAdminMembers(self.groupInfo.groupObj)
        return retval

    @Lazy
    def managers(self):
        retval = AdminMembers(self.groupInfo.groupObj)
        return retval

    @Lazy
    def moderators(self):
        retval = Moderators(self.groupInfo.groupObj)
        return retval

    @Lazy
    def moderatees(self):
        retval = ModeratedMembers(self.groupInfo.groupObj)
        return retval

    @Lazy
    def postingMembers(self):
        retval = PostingMembers(self.groupInfo.groupObj)
        return retval

    @Lazy
    def blockedMembers(self):
        retval = BlockedMembers(self.groupInfo.groupObj)
        return retval

    @Lazy
    def unverifiedMembers(self):
        retval = UnverifiedMembers(self.groupInfo.groupObj)
        return retval

    @Lazy
    def verifiedMembers(self):
        retval = VerifiedMembers(self.groupInfo.groupObj)
        return retval
