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
    '''An abstract base-class (ABC) for lists of people in a group

:param group: The group to list

The *concrete* classes provide a list of user-identifiers as :
attr:`subsetIds`. This allows the base-class to provide the :meth:`__len__`,
:meth:`__iter__` and :meth:`__contains__` methods. Some other properties are
provided for convenience.'''
    __metaclass__ = ABCMeta

    def __init__(self, group):
        self.group = group

    @abstractproperty
    def subsetIds(self):
        '''The list of the user-ids for the subset of the members.

:returns: A subset of :meth:`memberIds`
:rtype: set

*Concrete* classes must provide this property as :func:`list`.'''

    def __len__(self):
        '''The number of members in the subset.

:returns: The number of members.
:rtype: int'''
        retval = len(self.subsetIds)
        return retval

    def __iter__(self):
        '''The users in the subset.

:returns: A generator that iterates through the users in the subset.
:rtype: Products.CustomUserFolder.interfaces.IGSUserInfo

If an object cannot be instantiated for a member then it is logged as an
error, and the other members are processed.'''
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
        '''Get the identifier for the user.

:param member: The member to get the identifier for, as either a :func:`str`
               (assumed to be an ID), a user-object, or a user-info object.
:returns: The identifier for the user
:rtype: str
:raises TypeError: The identifier could not be found from the member.

The :meth:`__contains__` is flexible to its arguments, because of this
:meth:`get_id` method.'''
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
        '''Does the subset contain a member?

:param member: The member to test, as an string (the identifier), user object,
               or user-info object.
:returns: ``True`` if the subset of members contains the member; ``False``
          otherwise.'''
        memberId = self.get_id(member)
        retval = memberId in self.subsetIds
        return retval

    @Lazy
    def mlistInfo(self):
        '''The mailing-list information'''
        retval = createObject('groupserver.MailingListInfo', self.group)
        return retval

    @Lazy
    def groupInfo(self):
        '''The group information'''
        retval = self.mlistInfo.groupInfo
        return retval

    @Lazy
    def siteInfo(self):
        'The site information'
        retval = createObject('groupserver.SiteInfo', self.group)
        return retval

    @Lazy
    def memberIds(self):
        '''All members of the group

:returns: The identifiers for all members of the group
:rtype: set'''
        retval = set(get_group_userids(self.group, self.group))
        return retval
