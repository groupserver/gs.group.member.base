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
from gs.profile.email.base.emailuser import EmailUser
from .listabc import MemberListABC


class VerifiedMembers(MemberListABC):
    '''The list of group members that have a verified email address'''

    @property
    def verifiedMemberIds(self):
        return self.subsetIds

    @Lazy
    def subsetIds(self):
        retval = set()
        for uId in self.memberIds:
            userInfo = createObject('groupserver.UserFromId', self.group, uId)
            emailUser = EmailUser(self.group, userInfo)
            if emailUser.get_verified_addresses():
                retval.add(userInfo.id)
        return retval


class UnverifiedMembers(MemberListABC):
    '''The list of group members that lack a verified email address'''

    @property
    def unverifiedMemberIds(self):
        return self.subsetIds

    @Lazy
    def subsetIds(self):
        retval = self.memberIds - VerifiedMembers(self.group).subsetIds
        return retval
