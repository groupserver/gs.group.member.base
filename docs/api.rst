===============================
:mod:`gs.group.member.base` API
===============================

.. currentmodule:: gs.group.member.base

The :mod:`gs.group.member.base` API provides utilities_ and
`membership lists_`.

Utilities
=========

The membership utilities are in two broad categories: those that
that delve into `member groups`_, and `check membership`_.

Member groups
-------------

A group in GroupServer is a three-part object: a mailing list, a
web group, and a *member group*. The :func:`member_id` determines
the ID of the member group, and :func:`get_group_userids` gets
the list of user-identifiers stored in the member-group (but most
will be happier with one of the lists_).

.. autofunction:: member_id
.. autofunction:: get_group_userids

.. _check membership:

Checking membership
-------------------

A person can have many roles in a group. These utility functions
check if a user has a particular role. Most can take *either* an
**info** class or an actual instance.

.. autofunction:: user_member_of_group
.. autofunction:: user_member_of_site
.. autofunction:: user_admin_of_group
.. autofunction:: user_group_admin_of_group
.. autofunction:: user_site_admin_of_group
.. autofunction:: user_participation_coach_of_group

.. _lists:

Membership lists
================

All the membership lists are concrete_ implementations of the
`list abstract base-class`_.

List abstract base-class
------------------------

.. currentmodule:: gs.group.member.base.listabc

Concrete implementations of the list abstract base-class needs to
supply one property, the :meth:`MemberListABC.subsetIds`.

.. autoclass:: MemberListABC
   :members:
   :special-members: __len__, __iter__, __contains__

.. _concrete:

Concrete lists
--------------

.. currentmodule:: gs.group.member.base

The concrete lists include those for members_, administrators_,
an `invited members`_.

Members
~~~~~~~

A member may be one of three things: a list of the
:class:`FullMembers`, :class:`AllMembers`, or the
:class:`NormalMembers` of the group.

.. autoclass:: FullMembers
.. autoclass:: AllMembers
.. autoclass:: NormalMembers

Administrators
~~~~~~~~~~~~~~

A person can be an administrator in one of two ways:

#. They are explicitly a group administrator
   (:class:`GroupAdminMembers`) or
#. They are a site administrator that is also a group member
   (:class:`SiteAdminMembers`)

However, most are just concerned with people that are in either
group (:class:`AdminMembers`).

.. autoclass:: GroupAdminMembers
.. autoclass:: SiteAdminMembers
.. autoclass:: AdminMembers

Invited members
~~~~~~~~~~~~~~~

An invited member is rare: they are sort-of a member, but they
are not listed as :class:`FullMembers`.

.. autoclass:: InvitedMembers
