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
from gs.group.member.base.moderated import (ModeratedMembers, )


class TestModeratedMembers(TestCase):
    'Test the ``ModeratedMembers`` class'

    def mailing_list(self, moderated, moderatedMembers):
        retval = MagicMock()
        retval.is_moderated = moderated
        retval.get_property.return_value = moderatedMembers
        return retval

    @patch.object(ModeratedMembers, 'mlistInfo', new_callable=PropertyMock)
    def test_len_not_moderated(self, m_mI):
        m_mI.return_value = self.mailing_list(False, ['a', 'b', 'c', ])
        mm = ModeratedMembers(MagicMock())
        r = len(mm)

        self.assertEqual(0, r)

    @patch.object(ModeratedMembers, 'memberIds', new_callable=PropertyMock)
    @patch.object(ModeratedMembers, 'mlistInfo', new_callable=PropertyMock)
    def test_len_moderated(self, m_mlI, m_mI):
        m_mlI.return_value = self.mailing_list(True, ['a', 'b', 'c', ])
        m_mI.return_value = ['a', 'b', 'c', 'd', 'e', 'f', ]
        mm = ModeratedMembers(MagicMock())
        r = len(mm)

        self.assertEqual(3, r)

    @patch.object(ModeratedMembers, 'memberIds', new_callable=PropertyMock)
    @patch.object(ModeratedMembers, 'mlistInfo', new_callable=PropertyMock)
    def test_contains(self, m_mlI, m_mI):
        m_mlI.return_value = self.mailing_list(True, ['a', 'b', 'c', ])
        m_mI.return_value = ['a', 'b', 'c', 'd', 'e', 'f', ]
        mm = ModeratedMembers(MagicMock())

        self.assertIn('a', mm)

    @patch.object(ModeratedMembers, 'memberIds', new_callable=PropertyMock)
    @patch.object(ModeratedMembers, 'mlistInfo', new_callable=PropertyMock)
    def test_does_not_contain(self, m_mlI, m_mI):
        m_mlI.return_value = self.mailing_list(True, ['a', 'b', 'c', ])
        m_mI.return_value = ['a', 'b', 'c', 'd', 'e', 'f', ]
        mm = ModeratedMembers(MagicMock())

        self.assertNotIn('f', mm)

    @patch('gs.group.member.base.moderated.createObject')
    @patch.object(ModeratedMembers, 'memberIds', new_callable=PropertyMock)
    @patch.object(ModeratedMembers, 'mlistInfo', new_callable=PropertyMock)
    def test_iter(self, m_mlI, m_mI, m_cO):
        '''Test that we itterate fine'''
        m_mlI.return_value = self.mailing_list(True, ['a', 'b', 'c', ])
        m_mI.return_value = ['a', 'b', 'c', 'd', 'e', 'f', ]
        mm = ModeratedMembers(MagicMock())
        r = [userInfo for userInfo in mm]

        self.assertEqual(len(mm), len(r))
        self.assertEqual(3, m_cO.call_count)

    @patch('gs.group.member.base.moderated.createObject')
    @patch.object(ModeratedMembers, 'memberIds', new_callable=PropertyMock)
    @patch.object(ModeratedMembers, 'mlistInfo', new_callable=PropertyMock)
    def test_non_member(self, m_mlI, m_mI, m_cO):
        '''Test what happens when a non-member is in the list of moderated members'''
        m_mlI.return_value = self.mailing_list(True, ['b', 'c', ])
        m_mI.return_value = ['b', 'c', 'd', 'e', 'f', ]
        mm = ModeratedMembers(MagicMock())
        r = [userInfo for userInfo in mm]

        self.assertEqual(len(mm), len(r))
        self.assertEqual(2, m_cO.call_count)
