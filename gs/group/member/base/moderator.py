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
from zope.component import createObject
from gs.core import to_ascii
from .listabc import MemberListABC

#: The logger for this module
log = getLogger('gs.group.member.base.moderator')


class Moderators(MemberListABC):

    def __len__(self):
        retval = len(self.moderatorIds)
        return retval

    def __iter__(self):
        for uId in self.moderatorIds:
            retval = createObject('groupserver.UserFromId', self.group, uId)
            yield retval

    def __contains__(self, member):
        memberId = self.get_id(member)
        retval = memberId in self.moderatorIds
        return retval

    @Lazy
    def moderatorIds(self):
        retval = []
        if self.mlistInfo.is_moderated:
            mi = self.mlistInfo.get_property('moderator_members')
            moderatorIds = set(mi if mi else [])
            moderatorButNotMember = moderatorIds - set(self.memberIds)
            for uId in moderatorButNotMember:
                m = 'The user ID %s is listed as a moderator in the group %s (%s) on the '\
                    'site %s (%s), but is  not a member of the group.' %\
                    (uId, self.groupInfo.name, self.groupInfo.id, self.siteInfo.name,
                     self.siteInfo.id)
                msg = to_ascii(m)
                log.warn(msg)
            retval = moderatorIds - moderatorButNotMember
        return retval
