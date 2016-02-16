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
log = getLogger('gs.group.member.base.siteadmins')


class SiteAdminMembers(MemberListABC):
    'The list of group-members that are site admins'
    @Lazy
    def subsetIds(self):
        adminIds = set([u.getId() for u in self.group.users_with_local_role('DivisionAdmin')])
        retval = set(self.memberIds).intersection(adminIds)
        return retval
