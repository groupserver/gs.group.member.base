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
from __future__ import absolute_import, unicode_literals, print_function
from mock import (MagicMock, patch, PropertyMock)
from unittest import TestCase
from gs.group.member.base.siteadmins import (SiteAdminMembers, )


class TestSiteAdmins(TestCase):
    'Test the ``SiteAdminMembers`` class'

    @staticmethod
    def user(uId):
        retval = MagicMock()
        retval.getId.return_value = uId
        return retval

    @patch.object(SiteAdminMembers, 'memberIds', new_callable=PropertyMock)
    def test_normal(self, m_mI):
        '''Test that the list of site admins is returned'''
        g = MagicMock()
        g.users_with_local_role.return_value = [self.user(u) for u in ['a', 'b', 'c', ]]
        m_mI.return_value = ['a', 'b', 'c', 'd', 'e', 'f', ]
        m = SiteAdminMembers(g)
        r = m.subsetIds

        self.assertEqual(set(['a', 'b', 'c']), r)

    @patch.object(SiteAdminMembers, 'memberIds', new_callable=PropertyMock)
    def test_non_member(self, m_mI):
        '''Test that a non-member is excluded from the list of site admins in the group'''
        g = MagicMock()
        g.users_with_local_role.return_value = [self.user(u) for u in ['a', 'b', 'c', ]]
        m_mI.return_value = ['b', 'c', 'd', 'e', 'f', ]
        m = SiteAdminMembers(g)
        r = m.subsetIds

        self.assertEqual(set(['b', 'c']), r)
