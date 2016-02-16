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
log = getLogger('gs.group.member.base.admins')


class SiteAdminMembers(MemberListABC):
    'The list of group-members that are site admins'
    @property
    def siteAdminIds(self):
        return self.subsetIds

    @Lazy
    def subsetIds(self):
        adminIds = set([u.getId() for u in self.group.users_with_local_role('DivisionAdmin')])
        retval = set(self.memberIds).intersection(adminIds)
        return retval


class GroupAdminMembers(MemberListABC):
    'The list of group-members that are group admins'
    @property
    def groupAdminIds(self):
        return self.subsetIds

    @Lazy
    def subsetIds(self):
        adminIds = set([u.getId() for u in self.group.users_with_local_role('GroupAdmin')])
        sm = set(self.memberIds)
        for uId in adminIds.difference(sm):
            m = 'The user ID %s is listed as an administrator of the group %s (%s) on the '\
                'site %s (%s), but is  not a member of the group.' %\
                (uId, self.groupInfo.name, self.groupInfo.id, self.siteInfo.name, self.siteInfo.id)
            msg = to_ascii(m)
            log.warn(msg)
        retval = sm.intersection(adminIds)
        return retval


class AdminMembers(MemberListABC):
    @property
    def adminIds(self):
        return self.subsetIds

    @Lazy
    def subsetIds(self):
        siteAdmins = SiteAdminMembers(self.group).siteAdminIds
        groupAdmins = GroupAdminMembers(self.group).groupAdminIds
        retval = siteAdmins.union(groupAdmins)
        return retval
