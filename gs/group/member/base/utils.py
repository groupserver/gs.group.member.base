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
from __future__ import absolute_import, unicode_literals
from Products.CustomUserFolder.interfaces import IGSUserInfo
from Products.GSContent.interfaces import IGSSiteInfo
from Products.GSGroup.interfaces import IGSGroupInfo
from Products.GSGroupMember.groupmembership import userInfo_to_user,\
    groupInfo_to_group
import logging
log = logging.getLogger('gs.group.member.base.utils')


def user_member_of_group(u, g):
    '''Is the user the member of the group?

:param u:  A GroupServer user.
:param g: A GroupServer group.
:retval: ``True`` if the user is the member of the group. ``False``
         otherwise.
    '''
    group = groupInfo_to_group(g)
    user = userInfo_to_user(u)

    retval = 'GroupMember' in user.getRolesInContext(group)

    # Thundering great sanity check
    memberGroup = member_id(group.getId())
    userGroups = user.getGroups()
    if retval and (memberGroup not in userGroups):
        m = '(%s) has the GroupMember role for (%s) but is not in  %s' %\
            (user.getId(), group.getId(), memberGroup)
        log.error(m)
    elif not(retval) and (memberGroup in userGroups):
        m = '(%s) is in %s, but does not have the GroupMember role in '\
            '(%s)' % (user.getId(), memberGroup, group.getId())
        log.error(m)

    assert type(retval) == bool
    return retval


def user_member_of_site(u, site):
    user = userInfo_to_user(u)
    if hasattr(site, 'siteObj'):
        site = site.siteObj
    retval = 'DivisionMember' in user.getRolesInContext(site)
    assert type(retval) == bool
    return retval


def user_admin_of_group(u, g):
    group = groupInfo_to_group(g)
    user = userInfo_to_user(u)
    retval = (user_group_admin_of_group(user, group) or
              user_division_admin_of_group(user, group))
    assert type(retval) == bool
    return retval


def user_group_admin_of_group(u, g):
    group = groupInfo_to_group(g)
    user = userInfo_to_user(u)
    retval = ('GroupAdmin' in user.getRolesInContext(group))
    assert type(retval) == bool
    return retval


def user_site_admin_of_group(u, g):
    group = groupInfo_to_group(g)
    user = userInfo_to_user(u)
    retval = ('DivisionAdmin' in user.getRolesInContext(group))
    assert type(retval) == bool
    return retval

user_division_admin_of_group = user_site_admin_of_group


def member_id(groupId):
    assert type(groupId) == str
    assert groupId != ''
    retval = '%s_member' % groupId
    assert type(retval) == str
    return retval


def user_participation_coach_of_group(userInfo, groupInfo):
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
    'Get the user Ids of members of a user group.'
    if not context:
        raise ValueError('No context given')
    if not group:
        raise ValueError('No group given')

    if type(group) == str:
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

    assert type(retval) == list, \
        'retval is a {0}, not a list.'.format(retval)
    return retval
