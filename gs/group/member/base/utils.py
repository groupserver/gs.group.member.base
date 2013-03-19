# coding=utf-8
from Products.GSGroup.interfaces import IGSGroupInfo
from Products.CustomUserFolder.interfaces import IGSUserInfo
from Products.GSGroupMember.groupmembership import userInfo_to_user,\
    groupInfo_to_group
import logging
log = logging.getLogger('gs.group.member.base.utils')


def user_member_of_group(u, g):
    '''Is the user the member of the group?

    ARGUMENTS
        "user":  A GroupServer user.
        "group": A GroupServer group.

    RETURNS
        True if the user is the member of the group. False otherwise.
    '''
    group = groupInfo_to_group(g)
    user = userInfo_to_user(u)

    retval = 'GroupMember' in user.getRolesInContext(group)

    # Thundering great sanity check
    memberGroup = member_id(group.getId())
    userGroups = user.getGroups()
    if retval and (memberGroup not in userGroups):
        m = u'(%s) has the GroupMember role for (%s) but is not in  %s' %\
          (user.getId(), group.getId(), memberGroup)
        log.error(m)
    elif not(retval) and (memberGroup in userGroups):
        m = u'(%s) is in %s, but does not have the GroupMember role in (%s)' %\
          (user.getId(), memberGroup, group.getId())
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
    assert IGSUserInfo.providedBy(userInfo), '%s is not a IGSUserInfo' % \
      userInfo
    assert IGSGroupInfo.providedBy(groupInfo)
    ptnCoachId = groupInfo.get_property('ptn_coach_id', '')
    retval = user_member_of_group(userInfo, groupInfo)\
      and (userInfo.id == ptnCoachId)
    assert type(retval) == bool
    return retval
