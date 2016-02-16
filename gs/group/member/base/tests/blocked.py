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
from gs.group.member.base.blocked import (BlockedMembers, )


class TestBlockedMembers(TestCase):
    'Test the ``BlockedMembers`` class'

    def mailing_list(self, blockedMembers):
        retval = MagicMock()
        retval.get_property.return_value = blockedMembers
        return retval

    @patch.object(BlockedMembers, 'memberIds', new_callable=PropertyMock)
    @patch.object(BlockedMembers, 'mlistInfo', new_callable=PropertyMock)
    def test_normal(self, m_mlI, m_mI):
        m_mlI.return_value = self.mailing_list(['a', 'b', 'c', ])
        m_mI.return_value = ['a', 'b', 'c', 'd', 'e', 'f', ]
        m = BlockedMembers(MagicMock())
        r = m.subsetIds

        self.assertEqual(set(['a', 'b', 'c']), r)

    @patch('gs.group.member.base.blocked.log')
    @patch.object(BlockedMembers, 'siteInfo', new_callable=PropertyMock)
    @patch.object(BlockedMembers, 'groupInfo', new_callable=PropertyMock)
    @patch.object(BlockedMembers, 'memberIds', new_callable=PropertyMock)
    @patch.object(BlockedMembers, 'mlistInfo', new_callable=PropertyMock)
    def test_non_member(self, m_mlI, m_mI, m_gI, m_sI, m_l):
        '''Test that a non-member is excluded from the list of blocked members'''
        m_mlI.return_value = self.mailing_list(['a', 'b', 'c', ])
        m_mI.return_value = ['b', 'c', 'd', 'e', 'f', ]
        m = BlockedMembers(MagicMock())
        r = m.subsetIds

        self.assertEqual(set(['b', 'c']), r)
        self.assertEqual(1, m_l.warn.call_count)
