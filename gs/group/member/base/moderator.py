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

#: The logger for this module
log = getLogger('gs.group.member.base.moderator')


class Moderators(MemberListABC):
    '''The list of group members that are moderators'''

    @property
    def moderatorMemberIds(self):
        return self.subsetIds

    @Lazy
    def subsetIds(self):
        retval = set()
        if self.mlistInfo.is_moderated:
            mi = self.mlistInfo.get_property('moderator_members')
            moderatorIds = set(mi if mi else [])
            for uId in moderatorIds.difference(self.memberIds):
                m = 'The user ID %s is listed as a moderator in the group %s (%s) on the '\
                    'site %s (%s), but is  not a member of the group.'
                log.warn(m, uId, self.groupInfo.name, self.groupInfo.id, self.siteInfo.name,
                         self.siteInfo.id)
            retval = self.memberIds.intersection(moderatorIds)
        return retval
