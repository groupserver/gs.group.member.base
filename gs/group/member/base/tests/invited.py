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
from gs.group.member.base.invited import (InvitedMembers, )


class TestInvitedMembers(TestCase):
    'Test the ``InvitedMembers`` class'

    @patch.object(InvitedMembers, 'memberIds', new_callable=PropertyMock)
    @patch.object(InvitedMembers, 'siteInfo', new_callable=PropertyMock)
    @patch.object(InvitedMembers, 'groupInfo', new_callable=PropertyMock)
    @patch('gs.group.member.base.invited.InvitedMemberQuery')
    def test_normal(self, m_IMQ, m_sI, m_gI, m_mI):
        m_IMQ().invited_members.return_value = ['a', 'b', 'c', ]
        m_mI.return_value = ['d', 'e', 'f', ]
        m = InvitedMembers(MagicMock())
        r = m.subsetIds

        self.assertEqual(set(['a', 'b', 'c']), r)

    @patch.object(InvitedMembers, 'memberIds', new_callable=PropertyMock)
    @patch.object(InvitedMembers, 'siteInfo', new_callable=PropertyMock)
    @patch.object(InvitedMembers, 'groupInfo', new_callable=PropertyMock)
    @patch('gs.group.member.base.invited.InvitedMemberQuery')
    @patch('gs.group.member.base.invited.log')
    def test_member(self, m_log, m_IMQ, m_sI, m_gI, m_mI):
        m_IMQ().invited_members.return_value = ['a', 'b', 'c', ]
        m_mI.return_value = ['c', 'd', 'e', 'f', ]
        m = InvitedMembers(MagicMock())
        r = m.subsetIds

        self.assertEqual(set(['a', 'b', 'c']), r)
        self.assertEqual(1, m_log.warn.call_count)
