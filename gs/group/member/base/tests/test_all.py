# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2016 OnlineGroups.net and Contributors.
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
from unittest import TestSuite, main as unittest_main
from gs.group.member.base.tests.admins import (TestSiteAdmins, TestGroupAdmins, TestAdmins, )
from gs.group.member.base.tests.blocked import (TestBlockedMembers, )
from gs.group.member.base.tests.listabc import TestListABC
from gs.group.member.base.tests.moderated import TestModeratedMembers
from gs.group.member.base.tests.moderator import TestModerators
from gs.group.member.base.tests.posting import TestPostingMembers
from gs.group.member.base.tests.utils import (
    TestMemberId, TestGroupInfoToGroup, TestUserInfoToUser, TestUserMemberOfGroup,
    TestUserMemberOfSite, TestUserGroupAdmin, TestUserSiteAdminOfGroup, TestUserAdminOfGroup,
    TestUserParticipationCoachOfGroup, TestGetGroupUserIds, )
from gs.group.member.base.tests.verified import (TestVerifiedMembers, TestUnverifiedMembers, )

testCases = (
    TestMemberId, TestGroupInfoToGroup, TestUserInfoToUser, TestUserMemberOfGroup,
    TestUserMemberOfSite, TestUserGroupAdmin, TestUserSiteAdminOfGroup, TestUserAdminOfGroup,
    TestUserParticipationCoachOfGroup, TestGetGroupUserIds, TestListABC, TestModeratedMembers,
    TestModerators, TestSiteAdmins, TestGroupAdmins, TestAdmins, TestPostingMembers,
    TestBlockedMembers, TestVerifiedMembers, TestUnverifiedMembers, )


def load_tests(loader, tests, pattern):
    suite = TestSuite()
    for testClass in testCases:
        tests = loader.loadTestsFromTestCase(testClass)
        suite.addTests(tests)
    return suite

if __name__ == '__main__':
    unittest_main()
