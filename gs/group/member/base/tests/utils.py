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
from mock import (MagicMock, patch)  # , PropertyMock)
from unittest import TestCase
from gs.group.member.base.utils import (
    member_id, groupInfo_to_group, userInfo_to_user, user_member_of_group, user_member_of_site,
    user_group_admin_of_group, user_site_admin_of_group, user_admin_of_group,
    user_participation_coach_of_group, get_group_userids, )


class TestMemberId(TestCase):
    'Test the member_id function'
    def test_not_string(self):
        'Test we raise an error when something other than a string is passed in'
        with self.assertRaises(TypeError):
            member_id(8)

    def test_empty(self):
        'Test we raise an error when an empty-string is passed in'
        with self.assertRaises(ValueError):
            member_id('')

    def test_member_id(self):
        'Test we get an membership-ID back'
        r = member_id('example')

        self.assertEqual(b'example_member', r)


class TestGroupInfoToGroup(TestCase):
    'Test the groupInfo_to_group function'
    def test_empty(self):
        with self.assertRaises(ValueError):
            groupInfo_to_group(None)

    @patch('gs.group.member.base.utils.IGSGroupInfo')
    def test_is_group_info(self, m_IGSGI):
        'Test we get the group-object back from a group info'
        m_IGSGI.providedBy.return_value = True
        groupInfo = MagicMock()
        groupInfo.groupObj = 'This is not a group'
        r = groupInfo_to_group(groupInfo)

        self.assertEqual(groupInfo.groupObj, r)

    @patch('gs.group.member.base.utils.IGSGroupInfo')
    def test_is_group(self, m_IGSGI):
        'Test we get the group from a group'
        m_IGSGI.providedBy.return_value = False
        group = MagicMock()
        group.groupObj = 'This is not a group'
        r = groupInfo_to_group(group)

        self.assertEqual(group, r)


class TestUserInfoToUser(TestCase):
    'Test the ``userInfo_to_user`` function'

    def test_empty(self):
        with self.assertRaises(ValueError):
            userInfo_to_user(None)

    @patch('gs.group.member.base.utils.IGSUserInfo')
    def test_is_user_info(self, m_IGSUI):
        'Test we get the user-object back from a user-info'
        m_IGSUI.providedBy.return_value = True
        userInfo = MagicMock()
        userInfo.user = 'This is not a user'
        r = userInfo_to_user(userInfo)

        self.assertEqual(userInfo.user, r)

    @patch('gs.group.member.base.utils.IGSUserInfo')
    def test_is_user(self, m_IGSUI):
        'Test we get the user from a user'
        user = MagicMock()
        user.user = 'This is not a user'
        r = userInfo_to_user(user)

        self.assertEqual(user.user, r)


class UserTest(TestCase):
    'And ABC for tests involving users'

    @staticmethod
    def user(roles, groups=[]):
        retval = MagicMock()
        retval.getRolesInContext.return_value = roles
        retval.getGroups.return_value = groups
        del(retval.user)  # So we throw an AttributeError on access
        return retval

    @staticmethod
    def group(gId):
        retval = MagicMock()
        retval.getId.return_value = gId
        return retval


class TestUserMemberOfGroup(UserTest):
    'Test the ``user_member_of_group`` function'

    def test_is_member(self):
        user = self.user(['GroupMember', ], ['example_member', ])
        group = self.group('example')
        r = user_member_of_group(user, group)

        self.assertTrue(r)

    def test_non_member(self):
        user = self.user([], ['other_member', ])
        group = self.group('example')
        r = user_member_of_group(user, group)

        self.assertFalse(r)

    @patch('gs.group.member.base.utils.log')
    def test_odd_userGroups(self, m_log):
        '''Test the odd case where a person has the ``GroupMember`` role, but the group is absent
from the list of groups for the member.'''
        user = self.user(['GroupMember', ], ['other_member', ])
        group = self.group('example')
        r = user_member_of_group(user, group)

        self.assertTrue(r)
        self.assertEqual(1, m_log.warn.call_count, 'Failed to raise a warning')

    @patch('gs.group.member.base.utils.log')
    def test_odd_not_userGroups(self, m_log):
        '''Test the odd case where a person lacks the ``GroupMember`` role, but the group is in
the list of groups for the member.'''
        user = self.user([], ['example_member', ])
        group = self.group('example')
        r = user_member_of_group(user, group)

        self.assertFalse(r)
        self.assertEqual(1, m_log.warn.call_count, 'Failed to raise a warning')


class TestUserMemberOfSite(UserTest):
    'Test the ``user_member_of_site`` function'

    @staticmethod
    def site():
        retval = MagicMock()
        del(retval.siteObj)
        return retval

    def test_is_member(self):
        user = self.user(['DivisionMember', ])
        site = self.site()
        r = user_member_of_site(user, site)

        self.assertTrue(r)

    def test_is_member_site_info(self):
        user = self.user(['DivisionMember', ])
        site = MagicMock()  # Needs site.siteObj
        site.getId.return_value = 'example'
        r = user_member_of_site(user, site)

        self.assertTrue(r)
        user.getRolesInContext.assert_called_once_with(site.siteObj)

    def test_non_member(self):
        user = self.user([])
        site = self.site()
        r = user_member_of_site(user, site)

        self.assertFalse(r)


class TestUserGroupAdmin(UserTest):
    'Test the ``user_group_admin_of_group`` function'

    def test_user_group_admin(self):
        user = self.user(['GroupAdmin', ])
        group = self.group('example')
        r = user_group_admin_of_group(user, group)

        self.assertTrue(r)

    def test_member(self):
        user = self.user(['GroupMember', ])
        group = self.group('example')
        r = user_group_admin_of_group(user, group)

        self.assertFalse(r)

    def test_site_admin(self):
        user = self.user(['DivisionAdmin', ])
        group = self.group('example')
        r = user_group_admin_of_group(user, group)

        self.assertFalse(r)

    def test_site_admin_group_member(self):
        user = self.user(['DivisionAdmin', 'GroupMember', ])
        group = self.group('example')
        r = user_group_admin_of_group(user, group)

        self.assertFalse(r)

    def test_non_member(self):
        user = self.user([])
        group = self.group('example')
        r = user_group_admin_of_group(user, group)

        self.assertFalse(r)


class TestUserSiteAdminOfGroup(UserTest):
    'Test the ``user_site_admin_of_group`` function'

    def test_user_group_admin(self):
        user = self.user(['GroupAdmin', ])
        group = self.group('example')
        r = user_site_admin_of_group(user, group)

        self.assertFalse(r)

    def test_member(self):
        user = self.user(['GroupMember', ])
        group = self.group('example')
        r = user_site_admin_of_group(user, group)

        self.assertFalse(r)

    def test_site_admin(self):
        user = self.user(['DivisionAdmin', ])
        group = self.group('example')
        r = user_site_admin_of_group(user, group)

        self.assertTrue(r)

    def test_site_admin_group_member(self):
        user = self.user(['DivisionAdmin', 'GroupMember', ])
        group = self.group('example')
        r = user_site_admin_of_group(user, group)

        self.assertTrue(r)

    def test_non_member(self):
        user = self.user([])
        group = self.group('example')
        r = user_site_admin_of_group(user, group)

        self.assertFalse(r)


class TestUserAdminOfGroup(UserTest):
    'Test the ``user_admin_of_group`` function'

    def test_user_group_admin(self):
        user = self.user(['GroupAdmin', 'GroupMember', ])
        group = self.group('example')
        r = user_admin_of_group(user, group)

        self.assertTrue(r)

    def test_member(self):
        user = self.user(['GroupMember', ])
        group = self.group('example')
        r = user_admin_of_group(user, group)

        self.assertFalse(r)

    def test_site_admin(self):
        user = self.user(['DivisionAdmin', ])
        group = self.group('example')
        r = user_admin_of_group(user, group)

        self.assertTrue(r)

    def test_site_admin_group_member(self):
        user = self.user(['DivisionAdmin', 'GroupMember', ])
        group = self.group('example')
        r = user_admin_of_group(user, group)

        self.assertTrue(r)

    def test_non_member(self):
        user = self.user([])
        group = self.group('example')
        r = user_admin_of_group(user, group)

        self.assertFalse(r)


class TestUserParticipationCoachOfGroup(TestCase):
    'Test the ``user_participation_coach_of_group`` function'

    @patch('gs.group.member.base.utils.IGSGroupInfo')
    @patch('gs.group.member.base.utils.IGSUserInfo')
    def test_no_context(self, m_IGSUI, m_IGSGI):
        m_IGSGI.providedBy.return_value = False
        m_IGSUI.providedBy.return_value = True
        with self.assertRaises(TypeError):
            user_participation_coach_of_group(MagicMock(), MagicMock())

    @patch('gs.group.member.base.utils.IGSGroupInfo')
    @patch('gs.group.member.base.utils.IGSUserInfo')
    def test_no_user(self, m_IGSUI, m_IGSGI):
        m_IGSGI.providedBy.return_value = True
        m_IGSUI.providedBy.return_value = False
        with self.assertRaises(TypeError):
            user_participation_coach_of_group(MagicMock(), MagicMock())

    @patch('gs.group.member.base.utils.IGSGroupInfo')
    @patch('gs.group.member.base.utils.IGSUserInfo')
    def test_neither_group_user(self, m_IGSUI, m_IGSGI):
        m_IGSGI.providedBy.return_value = False
        m_IGSUI.providedBy.return_value = False
        with self.assertRaises(TypeError):
            user_participation_coach_of_group(MagicMock(), MagicMock())

    @patch('gs.group.member.base.utils.IGSGroupInfo')
    @patch('gs.group.member.base.utils.IGSUserInfo')
    @patch('gs.group.member.base.utils.user_member_of_group')
    def test_coach(self, m_umog, m_IGSUI, m_IGSGI):
        m_umog.return_value = True
        m_IGSGI.providedBy.return_value = True
        m_IGSUI.providedBy.return_value = True
        groupInfo = MagicMock()
        groupInfo.get_property.return_value = 'example'
        userInfo = MagicMock()
        userInfo.id = 'example'
        r = user_participation_coach_of_group(userInfo, groupInfo)

        self.assertTrue(r)

    @patch('gs.group.member.base.utils.IGSGroupInfo')
    @patch('gs.group.member.base.utils.IGSUserInfo')
    @patch('gs.group.member.base.utils.user_member_of_group')
    def test_coach_non_member(self, m_umog, m_IGSUI, m_IGSGI):
        m_umog.return_value = False
        m_IGSGI.providedBy.return_value = True
        m_IGSUI.providedBy.return_value = True
        groupInfo = MagicMock()
        groupInfo.get_property.return_value = 'example'
        userInfo = MagicMock()
        userInfo.id = 'example'
        r = user_participation_coach_of_group(userInfo, groupInfo)

        self.assertFalse(r)

    @patch('gs.group.member.base.utils.IGSGroupInfo')
    @patch('gs.group.member.base.utils.IGSUserInfo')
    @patch('gs.group.member.base.utils.user_member_of_group')
    def test_non_coach_member(self, m_umog, m_IGSUI, m_IGSGI):
        m_umog.return_value = True
        m_IGSGI.providedBy.return_value = True
        m_IGSUI.providedBy.return_value = True
        groupInfo = MagicMock()
        groupInfo.get_property.return_value = 'other'
        userInfo = MagicMock()
        userInfo.id = 'example'
        r = user_participation_coach_of_group(userInfo, groupInfo)

        self.assertFalse(r)


class TestGetGroupUserIds(TestCase):
    '''Test the ``get_group_userids`` function'''
    def test_no_context(self):
        with self.assertRaises(ValueError):
            get_group_userids(None, MagicMock())

    def test_no_group(self):
        with self.assertRaises(ValueError):
            get_group_userids(MagicMock(), None)

    @patch('gs.group.member.base.utils.IGSGroupInfo')
    def test_not_group_or_site(self, m_IGSGI):
        m_IGSGI.providedBy.return_value = False
        with self.assertRaises(TypeError):
            get_group_userids(MagicMock(), MagicMock())

    @patch('gs.group.member.base.utils.IGSGroupInfo')
    def test_unicode(self, m_IGSGI):
        'Test getting the group-members when we pass in a unicode-string'
        m_IGSGI.providedBy.return_value = False
        context = MagicMock()
        group = context.site_root().acl_users.getGroupById()
        expected = ['member0', 'member1', ]
        group.getUsers.return_value = expected
        r = get_group_userids(context, 'example')

        self.assertEqual(expected, r)
        context.site_root().acl_users.getGroupById.assert_any_call('example_member', [])

    @patch('gs.group.member.base.utils.IGSGroupInfo')
    def test_str(self, m_IGSGI):
        'Test getting the group-members when we pass in a byte-string'
        m_IGSGI.providedBy.return_value = False
        context = MagicMock()
        group = context.site_root().acl_users.getGroupById()
        expected = ['member0', 'member1', ]
        group.getUsers.return_value = expected
        r = get_group_userids(context, b'example')

        self.assertEqual(expected, r)
        context.site_root().acl_users.getGroupById.assert_any_call('example_member', [])

    @patch('gs.group.member.base.utils.IGSGroupInfo')
    def test_groupInfo(self, m_IGSGI):
        'Test getting the group-members when we pass in a groupInfo'
        m_IGSGI.providedBy.return_value = False

        context = MagicMock()
        group = context.site_root().acl_users.getGroupById()
        expected = ['member0', 'member1', ]
        group.getUsers.return_value = expected

        groupInfo = MagicMock()
        del(groupInfo.getId)  # So we look like an info-object
        groupInfo.id = 'example'

        r = get_group_userids(context, groupInfo)

        self.assertEqual(expected, r)
        context.site_root().acl_users.getGroupById.assert_any_call('example_member', [])

    @patch('gs.group.member.base.utils.IGSGroupInfo')
    def test_siteInfo(self, m_IGSGI):
        'Test getting the group-members when we pass in a siteInfo'
        m_IGSGI.providedBy.return_value = True

        context = MagicMock()
        group = context.site_root().acl_users.getGroupById()
        expected = ['member0', 'member1', ]
        group.getUsers.return_value = expected

        siteInfo = MagicMock()
        del(siteInfo.getId)  # So we look like an info-object
        siteInfo.id = 'example'

        r = get_group_userids(context, siteInfo)

        self.assertEqual(expected, r)
        context.site_root().acl_users.getGroupById.assert_any_call('example_member', [])
