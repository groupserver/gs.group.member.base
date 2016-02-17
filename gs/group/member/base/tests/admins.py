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
from gs.group.member.base.admins import (SiteAdminMembers, GroupAdminMembers, AdminMembers, )


class AdminTest(TestCase):
    @staticmethod
    def user(uId):
        retval = MagicMock()
        retval.getId.return_value = uId
        return retval


class TestSiteAdmins(AdminTest):
    'Test the ``SiteAdminMembers`` class'

    @patch.object(SiteAdminMembers, 'memberIds', new_callable=PropertyMock)
    def test_normal(self, m_mI):
        '''Test that the list of site admins is returned'''
        g = MagicMock()
        g.users_with_local_role.return_value = [self.user(u) for u in ['a', 'b', 'c', ]]
        m_mI.return_value = set(['a', 'b', 'c', 'd', 'e', 'f', ])
        m = SiteAdminMembers(g)
        r = m.subsetIds

        self.assertEqual(set(['a', 'b', 'c']), r)

    @patch.object(SiteAdminMembers, 'memberIds', new_callable=PropertyMock)
    def test_non_member(self, m_mI):
        '''Test that a non-member is excluded from the list of site admins in the group'''
        g = MagicMock()
        g.users_with_local_role.return_value = [self.user(u) for u in ['a', 'b', 'c', ]]
        m_mI.return_value = set(['b', 'c', 'd', 'e', 'f', ])
        m = SiteAdminMembers(g)
        r = m.subsetIds

        self.assertEqual(set(['b', 'c']), r)


class TestGroupAdmins(AdminTest):
    'Test the ``GroupAdminMembers`` class'

    @staticmethod
    def user(uId):
        retval = MagicMock()
        retval.getId.return_value = uId
        return retval

    @patch.object(GroupAdminMembers, 'memberIds', new_callable=PropertyMock)
    def test_normal(self, m_mI):
        '''Test that the list of site admins is returned'''
        g = MagicMock()
        g.users_with_local_role.return_value = [self.user(u) for u in ['a', 'b', 'c', ]]
        m_mI.return_value = set(['a', 'b', 'c', 'd', 'e', 'f', ])
        m = GroupAdminMembers(g)
        r = m.subsetIds

        self.assertEqual(set(['a', 'b', 'c']), r)

    @patch('gs.group.member.base.admins.log')
    @patch.object(GroupAdminMembers, 'siteInfo', new_callable=PropertyMock)
    @patch.object(GroupAdminMembers, 'groupInfo', new_callable=PropertyMock)
    @patch.object(GroupAdminMembers, 'memberIds', new_callable=PropertyMock)
    def test_non_member(self, m_mI, m_gI, m_sI, m_l):
        '''Test that a non-member is excluded from the list of site admins in the group'''
        g = MagicMock()
        g.users_with_local_role.return_value = [self.user(u) for u in ['a', 'b', 'c', ]]
        m_mI.return_value = set(['b', 'c', 'd', 'e', 'f', ])
        m = GroupAdminMembers(g)
        r = m.subsetIds

        self.assertEqual(set(['b', 'c']), r)
        self.assertEqual(1, m_l.warn.call_count)


class TestAdmins(AdminTest):
    @patch.object(SiteAdminMembers, 'memberIds', new_callable=PropertyMock)
    @patch.object(GroupAdminMembers, 'memberIds', new_callable=PropertyMock)
    def test_normal(self, m_GAM_mI, m_SAM_mI):
        '''Test that the list of admins is returned'''
        g = MagicMock()
        g.users_with_local_role.side_effect = ([self.user(u) for u in ['a', 'b', ]],
                                               [self.user(u) for u in ['c', 'd', ]], )
        m_GAM_mI.return_value = m_SAM_mI.return_value = set(['a', 'b', 'c', 'd', 'e', 'f', ])
        m = AdminMembers(g)
        r = m.subsetIds

        self.assertEqual(set(['a', 'b', 'c', 'd', ]), r)

    @patch.object(SiteAdminMembers, 'memberIds', new_callable=PropertyMock)
    @patch.object(GroupAdminMembers, 'memberIds', new_callable=PropertyMock)
    def test_dupe(self, m_GAM_mI, m_SAM_mI):
        '''Test that the list of admins is returned is someone is both a site and group admin'''
        g = MagicMock()
        g.users_with_local_role.side_effect = ([self.user(u) for u in ['a', 'b', ]],
                                               [self.user(u) for u in ['b', 'c', ]], )
        m_GAM_mI.return_value = m_SAM_mI.return_value = set(['a', 'b', 'c', 'd', 'e', 'f', ])
        m = AdminMembers(g)
        r = m.subsetIds

        self.assertEqual(set(['a', 'b', 'c', ]), r)
