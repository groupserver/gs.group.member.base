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
from gs.group.member.base.verified import (VerifiedMembers, UnverifiedMembers, )


class VerificationTest(TestCase):
    @staticmethod
    def get_user(factoryName, context, uId):
        retval = MagicMock()
        retval.id = uId
        return retval


class TestVerifiedMembers(VerificationTest):
    @patch.object(VerifiedMembers, 'memberIds', new_callable=PropertyMock)
    @patch('gs.group.member.base.verified.EmailUser.get_verified_addresses')
    @patch('gs.group.member.base.verified.createObject')
    def test_verified(self, m_cO, m_g_v_a, m_mI):
        'Test that people that are verified are listed'
        m_mI.return_value = set(['a', 'b', 'c', 'd'])
        # --=mpj17=-- For the test it does not matter that it is always the
        # same address
        m_g_v_a.return_value = ['address@example.com', ]
        m_cO.side_effect = self.get_user
        v = VerifiedMembers(MagicMock())
        r = v.subsetIds

        self.assertEqual(4, len(r))
        self.assertEqual(set(['a', 'b', 'c', 'd']), r)

    @patch.object(VerifiedMembers, 'memberIds', new_callable=PropertyMock)
    @patch('gs.group.member.base.verified.EmailUser.get_verified_addresses')
    @patch('gs.group.member.base.verified.createObject')
    def test_unverified(self, m_cO, m_g_v_a, m_mI):
        'Test that people that lack a verified email address are excluded'
        m_mI.return_value = set(['a', 'b', 'c', 'd'])
        m_g_v_a.return_value = []
        m_cO.side_effect = self.get_user
        v = VerifiedMembers(MagicMock())
        r = v.subsetIds

        self.assertEqual(0, len(r))


class TestUnverifiedMembers(VerificationTest):
    # --=mpj17=-- Yes, I am patching the class for the verified-members
    @patch.object(UnverifiedMembers, 'memberIds', new_callable=PropertyMock)
    @patch.object(VerifiedMembers, 'memberIds', new_callable=PropertyMock)
    @patch('gs.group.member.base.verified.EmailUser.get_verified_addresses')
    @patch('gs.group.member.base.verified.createObject')
    def test_verified(self, m_cO, m_g_v_a, m_V_mI, m_U_mI):
        'Test that people that lack a verified email address are excluded'
        m_U_mI.return_value = m_V_mI.return_value = set(['a', 'b', 'c', 'd'])
        # --=mpj17=-- For the test it does not matter that it is always the
        # same address
        m_g_v_a.return_value = ['address@example.com', ]
        m_cO.side_effect = self.get_user
        v = UnverifiedMembers(MagicMock())
        r = v.subsetIds

        self.assertEqual(0, len(r))

    @patch.object(UnverifiedMembers, 'memberIds', new_callable=PropertyMock)
    @patch.object(VerifiedMembers, 'memberIds', new_callable=PropertyMock)
    @patch('gs.group.member.base.verified.EmailUser.get_verified_addresses')
    @patch('gs.group.member.base.verified.createObject')
    def test_unverified(self, m_cO, m_g_v_a, m_V_mI, m_U_mI):
        'Test that people that lack a verified email address are included'
        m_U_mI.return_value = m_V_mI.return_value = set(['a', 'b', 'c', 'd'])
        m_g_v_a.return_value = []
        m_cO.side_effect = self.get_user
        v = UnverifiedMembers(MagicMock())
        r = v.subsetIds

        self.assertEqual(4, len(r))
        self.assertEqual(set(['a', 'b', 'c', 'd']), r)
