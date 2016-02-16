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
from zope.component import createObject
from .utils import (get_group_userids, userInfo_to_user, )


class MemberListABC(object):

    def __init__(self, group):
        self.group = group

    @Lazy
    def mlistInfo(self):
        retval = createObject('groupserver.MailingListInfo', self.group)
        return retval

    @Lazy
    def memberIds(self):
        retval = get_group_userids(self.group, self.group)
        return retval

    @staticmethod
    def get_id(member):
        if isinstance(member, basestring):
            retval = member
        else:
            u = userInfo_to_user(member)
            try:
                retval = u.getId()
            except AttributeError:
                m = 'Expected a string, a user-info, or a user, got a "{0}"'
                msg = m.format(member)
                raise TypeError(msg)
        return retval
