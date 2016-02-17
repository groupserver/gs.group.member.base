# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2016 OnlineGroups.net and Contributors.
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
from .admins import AdminMembers
from .blocked import BlockedMembers
from .invited import InvitedMembers
from .listabc import MemberListABC
from .moderated import ModeratedMembers
from .moderator import Moderators
from .posting import PostingMembers
from .verified import UnverifiedMembers


class FullMembers(MemberListABC):
    '''The list of group members other than those that have been invited to join the group

This is normally what people refer to when they talk about "members".'''

    @property
    def fullMemberIds(self):
        return self.subsetIds

    @Lazy
    def subsetIds(self):
        retval = self.memberIds
        return retval


class AllMembers(MemberListABC):
    '''The list of all the group-members, including those that have been invited'''

    @property
    def allMemberIds(self):
        return self.subsetIds

    @Lazy
    def subsetIds(self):
        retval = self.memberIds.union(InvitedMembers(self.group).subsetIds)
        return retval


class NormalMembers(MemberListABC):
    '''Get all the group-members other than the administrators, those that are blocked,
those that are moderated, the moderators, posting members (where that applies), those
that lack a verified email address, and the participation coach'''
    @Lazy
    def ptnCoachId(self):
        ptnCoachId = self.groupInfo.get_property('ptn_coach_id', '')
        retval = ptnCoachId if (ptnCoachId and (ptnCoachId in self.memberIds)) else None
        return retval

    @Lazy
    def subsetIds(self):
        retval = self.memberIds - AdminMembers(self.group).subsetIds -\
            BlockedMembers(self.group).subsetIds - ModeratedMembers(self.group).subsetIds -\
            Moderators(self.group).subsetIds - PostingMembers(self.group).subsetIds -\
            UnverifiedMembers(self.group).subsetIds
        if self.ptnCoachId:
            retval.remove(self.ptnCoachId)
        return retval
