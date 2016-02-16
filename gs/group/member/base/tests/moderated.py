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

    @patch('gs.group.member.base.listabc.createObject')
    @patch.object(ModeratedMembers, 'memberIds', new_callable=PropertyMock)
    @patch.object(ModeratedMembers, 'mlistInfo', new_callable=PropertyMock)
    def test_non_member(self, m_mlI, m_mI, m_cO):
        '''Test that a non-member is excluded from the list of moderated members'''
        m_mlI.return_value = self.mailing_list(True, ['b', 'c', ])
        m_mI.return_value = ['b', 'c', 'd', 'e', 'f', ]
        mm = ModeratedMembers(MagicMock())
        r = [userInfo for userInfo in mm]

        self.assertEqual(len(mm), len(r))
        self.assertEqual(2, m_cO.call_count)
