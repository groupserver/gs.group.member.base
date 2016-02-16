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
from zope.component import createObject
from gs.core import to_ascii
from .utils import (get_group_userids, userInfo_to_user, )

#: The logger for this module
log = getLogger('gs.group.member.info.moderated')


class MemberList(object):

    def __init__(self, group):
        self.group = group

    @Lazy
    def mlistInfo(self):
        retval = createObject('groupserver.MailingListInfo', self.group)
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


class ModeratedMembers(MemberList):
    def __len__(self):
        retval = len(self.moderatedMemberIds)
        return retval

    def __iter__(self):
        for uId in self.moderatedMemberIds:
            retval = createObject('groupserver.UserFromId', self.group, uId)
            yield retval

    def __contains__(self, member):
        memberId = self.get_id(member)
        retval = memberId in self.moderatedMemberIds
        return retval

    @Lazy
    def memberIds(self):
        retval = get_group_userids(self.group, self.group)
        return retval

    @Lazy
    def moderatedMemberIds(self):
        retval = []
        if self.mlistInfo.is_moderated:
            m = self.mlistInfo.get_property('moderated_members')
            moderatedIds = set(m if m else [])
            moderatedButNotMember = moderatedIds - set(self.memberIds)

            for uId in moderatedButNotMember:
                m = 'The user ID %s is listed as a moderated member in the group %s (%s) on the '\
                    'site %s (%s), but is  not a member of the group.' %\
                    (uId, self.groupInfo.name, self.groupInfo.id, self.siteInfo.name,
                     self.siteInfo.id)
                msg = to_ascii(m)
                log.warn(msg)
            retval = moderatedIds - moderatedButNotMember
        return retval

    # --=mpj17=-- The old code used to moderate *everyone* if there was no one explicitly moderated,
    # and moderation was not set to ``moderate_new``. This is likely to be a bug rather than a
    # feature. Just in case it is not, here is the logic from the old code

    #elif not(self.mlistInfo.is_moderate_new):
        #for u in self.fullMembers:
            #isPtnCoach = self.ptnCoach and (self.ptnCoach.id == u.id)\
                #or False
            #isGrpAdmin = u.id in [a.id for a in self.groupAdmins]
            #isSiteAdmin = u.id in [a.id for a in self.siteAdmins]
            #isModerator = u.id in [m.id for m in self.moderators]
            #isBlocked = u.id in [m.id for m in self.blockedMembers]
            #if (not(isSiteAdmin) and not(isGrpAdmin) and
                #not(isPtnCoach) and not(isModerator) and
                #not(isBlocked)):
                        #retval.append(u)
