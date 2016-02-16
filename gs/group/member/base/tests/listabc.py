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
from mock import (MagicMock, patch, )  # PropertyMock)
from unittest import TestCase
from gs.group.member.base.listabc import (MemberListABC, )


class TestableList(MemberListABC):
    def __init__(self, g, ids):
        super(TestableList, self).__init__(g)
        self.ids = ids

    @property
    def subsetIds(self):
        retval = self.ids
        return retval


class TestListABC(TestCase):
    'Test the ``MemberListABC`` class'

    def test_len(self):
        m = TestableList(MagicMock(), ['a', 'b', 'c', ])
        r = len(m)

        self.assertEqual(3, r)

    def test_get_id_str(self):
        'Ensure we treat a string like an ID'
        m = TestableList(MagicMock(), [])
        r = m.get_id('dinsdale')

        self.assertEqual('dinsdale', r)

    @patch('gs.group.member.base.listabc.userInfo_to_user')
    def test_get_id_user(self, m_uI_t_u):
        'Ensure we get the user-ID from a user object'
        m = TestableList(MagicMock(), [])
        u = MagicMock()
        u.getId.return_value = 'dinsdale'
        m_uI_t_u.return_value = u
        r = m.get_id(u)

        self.assertEqual('dinsdale', r)

    def test_contains(self):
        m = TestableList(MagicMock(), ['a', 'b', 'c', ])

        self.assertIn('a', m)

    def test_does_not_contain(self):
        m = TestableList(MagicMock(), ['a', 'b', 'c', ])

        self.assertNotIn('d', m)

    @patch('gs.group.member.base.listabc.createObject')
    def test_iter(self, m_cO):
        '''Test that we itterate fine'''
        m = TestableList(MagicMock(), ['a', 'b', 'c', ])
        r = [userInfo for userInfo in m]

        self.assertEqual(len(m), len(r))
        self.assertEqual(3, m_cO.call_count)
