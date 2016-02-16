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
log = getLogger('gs.group.member.base.moderated')


class ModeratedMembers(MemberListABC):
    '''The list of group members that are moderated'''

    @property
    def moderatedMemberIds(self):
        return self.subsetIds

    @Lazy
    def subsetIds(self):
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
