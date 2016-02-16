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
from gs.core import to_ascii
from .listabc import MemberListABC

#: The logger for this module
log = getLogger('gs.group.member.base.posting')


class PostingMembers(MemberListABC):
    '''The list of group members that are posting members in an announcement group'''

    @property
    def postingMemberIds(self):
        return self.subsetIds

    @Lazy
    def subsetIds(self):
        # TODO: move to gs.group.type.announcement
        # TOOD: Check that the group is an announcement group
        m = self.mlistInfo.get_property('posting_members')
        postingIds = set(m if m else [])
        sm = set(self.memberIds)
        for uId in postingIds.difference(sm):
            m = 'The user ID %s is listed as a posting member in the group %s (%s) on the '\
                'site %s (%s), but is  not a member of the group.' %\
                (uId, self.groupInfo.name, self.groupInfo.id, self.siteInfo.name,
                 self.siteInfo.id)
            msg = to_ascii(m)
            log.warn(msg)
        retval = postingIds.intersection(sm)
        return retval
