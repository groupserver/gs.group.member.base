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
from gs.group.member.base.members import (NormalMembers, AllMembers, )


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

    @patch('gs.group.member.base.members.log.warn')
    @patch.object(NormalMembers, 'memberIds', new_callable=PropertyMock)
    @patch.object(NormalMembers, 'ptnCoachId', new_callable=PropertyMock)
    @patch.object(NormalMembers, 'groupInfo', new_callable=PropertyMock)
    @patch.object(NormalMembers, 'siteInfo', new_callable=PropertyMock)
    @patch('gs.group.member.base.members.AdminMembers.subsetIds', new_callable=PropertyMock)
    @patch('gs.group.member.base.members.BlockedMembers.subsetIds', new_callable=PropertyMock)
    @patch('gs.group.member.base.members.ModeratedMembers.subsetIds', new_callable=PropertyMock)
    @patch('gs.group.member.base.members.Moderators.subsetIds', new_callable=PropertyMock)
    @patch('gs.group.member.base.members.PostingMembers.subsetIds', new_callable=PropertyMock)
    @patch('gs.group.member.base.members.UnverifiedMembers.subsetIds', new_callable=PropertyMock)
    def test_ptn_coach_wrong(self, m_UM_sI, m_PM_sI, m_M_sI, m_MM_sI, m_BM_sI, m_AM_sI,
                             m_siteInfo, m_groupInfo, m_ptnCoachId, m_memberIds, m_warn):
        '''Ensure we cope with poorly-configured participation coach'''
        m_UM_sI.return_value = m_PM_sI.return_value = m_M_sI.return_value = m_MM_sI.return_value = \
            m_BM_sI.return_value = m_AM_sI.return_value = set()
        m_ptnCoachId.return_value = 'piranha'
        m_memberIds.return_value = set(['dirk', 'dinsdale', ])
        m_groupInfo().id = 'ethel'
        m_groupInfo().name = 'Ethel the Frog'
        m_siteInfo().id = 'example'
        m_siteInfo().name = 'Example site'

        n = NormalMembers(MagicMock())
        r = n.subsetIds

        self.assertEqual(set(['dirk', 'dinsdale', ]), r)
        self.assertEqual(1, m_warn.call_count)


class TestAllMembers(TestCase):
    'Test the ``AllMembers`` class'

    @patch('gs.group.member.base.members.InvitedMembers.subsetIds', new_callable=PropertyMock)
    @patch.object(AllMembers, 'memberIds', new_callable=PropertyMock)
    def test_no_invite(self, m_memberIds, m_Invited_subsetIds):
        'Cope with no invited members'
        m_Invited_subsetIds.return_value = set()
        m_memberIds.return_value = set(['dirk', 'dinsdale', ])

        a = AllMembers(MagicMock())
        r = a.subsetIds

        self.assertEqual(set(['dirk', 'dinsdale', ]), r)

    @patch('gs.group.member.base.members.InvitedMembers.subsetIds', new_callable=PropertyMock)
    @patch.object(AllMembers, 'memberIds', new_callable=PropertyMock)
    def test_invite(self, m_memberIds, m_Invited_subsetIds):
        'Cope with invited members'
        m_Invited_subsetIds.return_value = set(['dirk', 'piranah', ])
        m_memberIds.return_value = set(['dirk', 'dinsdale', ])

        a = AllMembers(MagicMock())
        r = a.subsetIds

        self.assertEqual(set(['dirk', 'dinsdale', 'piranah', ]), r)
