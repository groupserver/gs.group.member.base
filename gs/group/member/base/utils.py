# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2013, 2014 OnlineGroups.net and Contributors.
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
import sys
from gs.core import to_ascii
from Products.CustomUserFolder.interfaces import IGSUserInfo
from Products.GSContent.interfaces import IGSSiteInfo
from Products.GSGroup.interfaces import IGSGroupInfo

log = getLogger('gs.group.member.base.utils')

if (sys.version_info < (3, )):
    aString = basestring
else:
    aString = str


def member_id(groupId):
    '''Get the group membership ID from the group id

:param str groupId: The identifier for the group
:returns: The identifier for the member-group in ``acl_users``
:rtype: str'''
    if not(isinstance(groupId, aString)):
        raise TypeError('Expected string, got {0}'.format(type(groupId)))
    if not groupId:
        raise ValueError('The groupId must be set (is "{0}")'.format(groupId))

    retval = to_ascii('{0}_member'.format(groupId))
    return retval


def groupInfo_to_group(g):
    '''Ensure that we are dealing with a group-instance

:param g: The group-info instance, or a group instance
:returns: A group instance

For many utilities it is useful to be able to take either a group-instance or a
group-info instance. This function ensures is what allows the utilities to be
flexible.'''
    if not g:
        raise ValueError('The group must be set (is "{0}")'.format(g))

    if IGSGroupInfo.providedBy(g):
        retval = g.groupObj
    else:  # Just assume that it is a group
        retval = g
    return retval


def userInfo_to_user(u):
    '''Ensure that we are dealing with a user-instance

:param g: The user-info instance, or a user instance
:returns: A user instance

For many utilities it is useful to be able to take either a user-instance or a
user-info instance. This function ensures is what allows the utilities to be
flexible.'''
    # TODO: Move to gs.profile.base
    if not u:
        raise ValueError('The user must be set (is "{0}")'.format(u))

    if IGSUserInfo.providedBy(u):
        user = u.user
    else:
        user = u
    return user


def user_member_of_group(u, g):
    '''Is the user the member of the group?

:param u:  A GroupServer user.
:param g: A GroupServer group.
:retval: ``True`` if the user is the member of the group; ``False`` otherwise.
:rtype: bool'''
    group = groupInfo_to_group(g)
    user = userInfo_to_user(u)

    retval = 'GroupMember' in user.getRolesInContext(group)
    # Thundering great sanity check
    memberGroup = member_id(group.getId())
    userGroups = user.getGroups()
    if retval and (memberGroup not in userGroups):
        m = '(%s) has the GroupMember role for (%s) but is not in  %s'
        log.warn(m, user.getId(), group.getId(), memberGroup)
    elif not(retval) and (memberGroup in userGroups):
        m = '(%s) is in %s, but does not have the GroupMember role in (%s)'
        log.warn(m, user.getId(), memberGroup, group.getId())

    assert type(retval) == bool
    return retval


def user_member_of_site(u, site):
    '''Is the user the member of the site?

:param u:  A GroupServer user.
:param site: A GroupServer site instance.
:retval: ``True`` if the user is the member of the site; ``False`` otherwise.
:rtype: bool'''
    user = userInfo_to_user(u)
    if hasattr(site, 'siteObj'):
        site = site.siteObj
    retval = 'DivisionMember' in user.getRolesInContext(site)
    assert type(retval) == bool
    return retval


def user_group_admin_of_group(u, g):
    '''Is the user a group administrator for the group?

:param u:  A GroupServer user.
:param site: A GroupServer group.
:retval: ``True`` if the user is a group administrator of the group; ``False`` otherwise.
:rtype: bool'''
    group = groupInfo_to_group(g)
    user = userInfo_to_user(u)
    retval = ('GroupAdmin' in user.getRolesInContext(group))
    #assert type(retval) == bool
    return retval


def user_site_admin_of_group(u, g):
    '''Is the user a site-administrator in the context of the group?

:param u:  A GroupServer user.
:param site: A GroupServer group.
:retval: ``True`` if the user is a site administrator in the context of the group;
         ``False`` otherwise.
:rtype: bool'''
    group = groupInfo_to_group(g)
    user = userInfo_to_user(u)
    retval = ('DivisionAdmin' in user.getRolesInContext(group))
    assert type(retval) == bool
    return retval


#: The term *division* is a synonym for *site* for historical reasons
user_division_admin_of_group = user_site_admin_of_group


def user_admin_of_group(u, g):
    '''Is the user an administrator for the group?

:param u:  A GroupServer user.
:param g: A GroupServer group.
:retval: ``True`` if the user is an administrator of the group; ``False`` otherwise.
:rtype: bool

Sometimes it is enough that the user is *either* a site administrator or a group administrator.
This function tests for that.'''
    group = groupInfo_to_group(g)
    user = userInfo_to_user(u)
    retval = (user_group_admin_of_group(user, group) or user_division_admin_of_group(user, group))
    assert type(retval) == bool
    return retval


def user_participation_coach_of_group(userInfo, groupInfo):
    '''Is the user an participation coach for the group?

:param userInfo:  A GroupServer user.
:param groupInfo: A GroupServer group.
:retval: ``True`` if the user is the participation coach for the group; ``False`` otherwise.
:rtype: bool'''
    if not IGSUserInfo.providedBy(userInfo):
        m = '{0} is not a IGSUserInfo'.format(userInfo)
        raise TypeError(m)
    if not IGSGroupInfo.providedBy(groupInfo):
        m = '{0} is not a IGSGroupInfo'.format(groupInfo)
        raise TypeError(m)

    ptnCoachId = groupInfo.get_property('ptn_coach_id', '')
    retval = (user_member_of_group(userInfo, groupInfo)
              and (userInfo.id == ptnCoachId))
    assert type(retval) == bool
    return retval


def get_group_userids(context, group):
    '''Get the user-identifiers of members of a user group.

:param context: A folder within a GroupServer instance.
:param (str, group, groupInfo) group: A GroupServer group.
:retval: The list of members of a group.
:rtype: list'''
    if not context:
        raise ValueError('No context given (is "{0}")'.format(context))
    if not group:
        raise ValueError('No group given(is "{0}")'.format(context))

    if (isinstance(group, aString)):
        groupId = group
    elif IGSGroupInfo.providedBy(group) or IGSSiteInfo.providedBy(group):
        groupId = group.id
    else:
        m = 'group is a "{0}", not a string, group or site info.'
        msg = m.format(type(group))
        raise TypeError(msg)

    site_root = context.site_root()
    assert site_root, 'No site_root'
    assert hasattr(site_root, 'acl_users'), 'No acl_users at site_root'
    memberGroupId = member_id(groupId)
    memberGroup = site_root.acl_users.getGroupById(memberGroupId, [])
    retval = list(memberGroup.getUsers())

    assert type(retval) == list, 'retval is a "{0}", not a list. ({1})'.format(type(retval), retval)
    return retval
