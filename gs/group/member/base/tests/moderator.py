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
from gs.group.member.base.moderator import (Moderators, )


class TestModerators(TestCase):
    'Test the ``Moderators`` class'

    def mailing_list(self, moderated, moderatorMembers):
        retval = MagicMock()
        retval.is_moderated = moderated
        retval.get_property.return_value = moderatorMembers
        return retval

    @patch.object(Moderators, 'mlistInfo', new_callable=PropertyMock)
    def test_len_not_moderated(self, m_mI):
        m_mI.return_value = self.mailing_list(False, ['a', 'b', 'c', ])
        m = Moderators(MagicMock())
        r = len(m)

        self.assertEqual(0, r)

    @patch.object(Moderators, 'memberIds', new_callable=PropertyMock)
    @patch.object(Moderators, 'mlistInfo', new_callable=PropertyMock)
    def test_len_moderators(self, m_mlI, m_mI):
        m_mlI.return_value = self.mailing_list(True, ['a', 'b', 'c', ])
        m_mI.return_value = ['a', 'b', 'c', 'd', 'e', 'f', ]
        m = Moderators(MagicMock())
        r = len(m)

        m_mlI().get_property.assert_called_once_with('moderator_members')
        self.assertEqual(3, r)

    @patch.object(Moderators, 'memberIds', new_callable=PropertyMock)
    @patch.object(Moderators, 'mlistInfo', new_callable=PropertyMock)
    def test_contains(self, m_mlI, m_mI):
        m_mlI.return_value = self.mailing_list(True, ['a', 'b', 'c', ])
        m_mI.return_value = ['a', 'b', 'c', 'd', 'e', 'f', ]
        m = Moderators(MagicMock())

        self.assertIn('a', m)

    @patch.object(Moderators, 'memberIds', new_callable=PropertyMock)
    @patch.object(Moderators, 'mlistInfo', new_callable=PropertyMock)
    def test_does_not_contain(self, m_mlI, m_mI):
        m_mlI.return_value = self.mailing_list(True, ['a', 'b', 'c', ])
        m_mI.return_value = ['a', 'b', 'c', 'd', 'e', 'f', ]
        m = Moderators(MagicMock())

        self.assertNotIn('f', m)

    @patch('gs.group.member.base.listabc.createObject')
    @patch.object(Moderators, 'memberIds', new_callable=PropertyMock)
    @patch.object(Moderators, 'mlistInfo', new_callable=PropertyMock)
    def test_iter(self, m_mlI, m_mI, m_cO):
        '''Test that we itterate fine'''
        m_mlI.return_value = self.mailing_list(True, ['a', 'b', 'c', ])
        m_mI.return_value = ['a', 'b', 'c', 'd', 'e', 'f', ]
        m = Moderators(MagicMock())
        r = [userInfo for userInfo in m]

        self.assertEqual(len(m), len(r))
        self.assertEqual(3, m_cO.call_count)

    @patch('gs.group.member.base.listabc.createObject')
    @patch.object(Moderators, 'memberIds', new_callable=PropertyMock)
    @patch.object(Moderators, 'mlistInfo', new_callable=PropertyMock)
    def test_non_member(self, m_mlI, m_mI, m_cO):
        '''Test that a non-member is excluded from the list of moderated members'''
        m_mlI.return_value = self.mailing_list(True, ['b', 'c', ])
        m_mI.return_value = ['b', 'c', 'd', 'e', 'f', ]
        m = Moderators(MagicMock())
        r = [userInfo for userInfo in m]

        self.assertEqual(len(m), len(r))
        self.assertEqual(2, m_cO.call_count)
