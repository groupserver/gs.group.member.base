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
from gs.group.member.base.members import (NormalMembers, )


class TestNormalMembers(TestCase):
    'Test the ``ModeratedMembers`` class'

    @patch.object(NormalMembers, 'memberIds', new_callable=PropertyMock)
    @patch.object(NormalMembers, 'ptnCoachId', new_callable=PropertyMock)
    @patch('gs.group.member.base.members.AdminMembers.subsetIds', new_callable=PropertyMock)
    @patch('gs.group.member.base.members.BlockedMembers.subsetIds', new_callable=PropertyMock)
    @patch('gs.group.member.base.members.ModeratedMembers.subsetIds', new_callable=PropertyMock)
    @patch('gs.group.member.base.members.Moderators.subsetIds', new_callable=PropertyMock)
    @patch('gs.group.member.base.members.PostingMembers.subsetIds', new_callable=PropertyMock)
    @patch('gs.group.member.base.members.UnverifiedMembers.subsetIds', new_callable=PropertyMock)
    def test_ptn_coach_removed(self, m_UM_sI, m_PM_sI, m_M_sI, m_MM_sI, m_BM_sI, m_AM_sI,
                               m_ptnCoachId, m_memberIds):
        '''Ensure we remove the participation coach from the list of normal members'''
        m_UM_sI.return_value = m_PM_sI.return_value = m_M_sI.return_value = m_MM_sI.return_value = \
            m_BM_sI.return_value = m_AM_sI.return_value = set()
        m_ptnCoachId.return_value = 'dirk'
        m_memberIds.return_value = set(['dirk', 'dinsdale', ])
        n = NormalMembers(MagicMock())
        r = n.subsetIds

        self.assertEqual(set(['dinsdale', ]), r)

    @patch.object(NormalMembers, 'memberIds', new_callable=PropertyMock)
    @patch.object(NormalMembers, 'ptnCoachId', new_callable=PropertyMock)
    @patch('gs.group.member.base.members.AdminMembers.subsetIds', new_callable=PropertyMock)
    @patch('gs.group.member.base.members.BlockedMembers.subsetIds', new_callable=PropertyMock)
    @patch('gs.group.member.base.members.ModeratedMembers.subsetIds', new_callable=PropertyMock)
    @patch('gs.group.member.base.members.Moderators.subsetIds', new_callable=PropertyMock)
    @patch('gs.group.member.base.members.PostingMembers.subsetIds', new_callable=PropertyMock)
    @patch('gs.group.member.base.members.UnverifiedMembers.subsetIds', new_callable=PropertyMock)
    def test_ptn_coach_absent(self, m_UM_sI, m_PM_sI, m_M_sI, m_MM_sI, m_BM_sI, m_AM_sI,
                              m_ptnCoachId, m_memberIds):
        '''Ensure we cope with no participation coach'''
        m_UM_sI.return_value = m_PM_sI.return_value = m_M_sI.return_value = m_MM_sI.return_value = \
            m_BM_sI.return_value = m_AM_sI.return_value = set()
        m_ptnCoachId.return_value = ''
        m_memberIds.return_value = set(['dirk', 'dinsdale', ])
        n = NormalMembers(MagicMock())
        r = n.subsetIds

        self.assertEqual(set(['dirk', 'dinsdale', ]), r)

    @patch.object(NormalMembers, 'memberIds', new_callable=PropertyMock)
    @patch.object(NormalMembers, 'ptnCoachId', new_callable=PropertyMock)
    @patch('gs.group.member.base.members.AdminMembers.subsetIds', new_callable=PropertyMock)
    @patch('gs.group.member.base.members.BlockedMembers.subsetIds', new_callable=PropertyMock)
    @patch('gs.group.member.base.members.ModeratedMembers.subsetIds', new_callable=PropertyMock)
    @patch('gs.group.member.base.members.Moderators.subsetIds', new_callable=PropertyMock)
    @patch('gs.group.member.base.members.PostingMembers.subsetIds', new_callable=PropertyMock)
    @patch('gs.group.member.base.members.UnverifiedMembers.subsetIds', new_callable=PropertyMock)
    def test_ptn_coach_wrong(self, m_UM_sI, m_PM_sI, m_M_sI, m_MM_sI, m_BM_sI, m_AM_sI,
                             m_ptnCoachId, m_memberIds):
        '''Ensure we cope with poorly-configured participation coach'''
        m_UM_sI.return_value = m_PM_sI.return_value = m_M_sI.return_value = m_MM_sI.return_value = \
            m_BM_sI.return_value = m_AM_sI.return_value = set()
        m_ptnCoachId.return_value = 'piranha'
        m_memberIds.return_value = set(['dirk', 'dinsdale', ])
        n = NormalMembers(MagicMock())
        r = n.subsetIds

        self.assertEqual(set(['dirk', 'dinsdale', ]), r)
