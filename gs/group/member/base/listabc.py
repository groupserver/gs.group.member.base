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
from abc import ABCMeta, abstractproperty
from logging import getLogger
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from .utils import (get_group_userids, userInfo_to_user, )

#: The logger for the member-list
log = getLogger('gs.group.member.base.listabc')


class MemberListABC(object):
    __metaclass__ = ABCMeta

    def __init__(self, group):
        self.group = group

    @abstractproperty
    def subsetIds(self):
        '''The list of the user-ids for the subset of the members'''

    def __len__(self):
        retval = len(self.subsetIds)
        return retval

    def __iter__(self):
        for uId in self.subsetIds:
            retval = createObject('groupserver.UserFromId', self.group, uId)
            if retval.anonymous:
                log.error('Could not create a user-info for the user-identifier "%s" in the '
                          'group %s (%s) on %s (%s)', uId, self.groupInfo.name, self.groupInfo.id,
                          self.siteInfo.name, self.siteInfo.id)
                continue
            yield retval

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

    def __contains__(self, member):
        memberId = self.get_id(member)
        retval = memberId in self.subsetIds
        return retval

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

    @Lazy
    def memberIds(self):
        retval = set(get_group_userids(self.group, self.group))
        return retval
