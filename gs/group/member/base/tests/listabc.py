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
from mock import (MagicMock, )  # patch, PropertyMock)
from unittest import TestCase
from gs.group.member.base.listabc import (MemberListABC, )


class TestListABC(TestCase):
    'Test the ``MemberListABC`` class'
    def test_get_id_str(self):
        m = MemberListABC(MagicMock())
        r = m.get_id('dinsdale')

        self.assertEqual('dinsdale', r)
