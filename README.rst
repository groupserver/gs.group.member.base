========================
``gs.group.member.base``
========================
~~~~~~~~~~~~~~~~~~~~~~~~~~
The base group member code
~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2015-01-30
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
`Creative Commons Attribution-Share Alike 4.0 International License`_
  by `OnlineGroups.net`_.

..  _Creative Commons Attribution-Share Alike 4.0 International License:
    http://creativecommons.org/licenses/by-sa/4.0/

Introduction
============

This module contains a few utilities_ that are used by the rest
of the membership code in GroupServer.

Utilities
=========

There are eight functions defined by this product.

``member_id``
-------------

:Synopsis: ``member_id(groupId)``
:Description: Construct the group-membership identifier.
:Arguments: ``groupId``:
                The identifier of a group.
:Returns: The identifier of the member-group.
:Example: ``userGroupId = member_id(self.groupInfo.id)``


``user_member_of_group``
------------------------

:Synopsis: ``user_member_of_group(user, group)``
:Description: Tests to see if a user is a member of a group.
:Arguments: ``user``:
              A user-info or a user-object.
            ``group``:
              A group-info or a group-object.
:Returns: ``True`` if the user is a member of the group. ``False`` otherwise.
:Example: ``user_member_of_group(self.loggedInUser, self.groupInfo)``

``user_member_of_site``
-----------------------

:Synopsis: ``user_member_of_site(user, site)``
:Description: Tests to see if a user is a member of a site.
:Arguments: ``user``:
              A user-info or a user-object.
            ``site``:
              A site-info or a site object.
:Returns: ``True`` if the user is a member of the site. ``False`` otherwise.
:Example: ``user_member_of_site(self.loggedInUser, self.siteInfo)``

``user_admin_of_group``
-----------------------

:Synopsis: ``user_admin_of_group(user, group)``
:Description: Tests to see if a user is an administrator of a group.
:Arguments: ``user``:
              A user-info or a user-object.
            ``group``:
              A group-info or a group.
:Returns: ``True`` if the user is either a site administrator or group
          administrator of the group. ``False`` otherwise.
:Example: ``user_admin_of_group(self.loggedInUser, self.groupInfo)``
:See also: user_group_admin_of_group_, user_site_admin_of_group_

``user_group_admin_of_group``
-----------------------------

:Synopsis: ``user_group_admin_of_group(user, group)``
:Description: Tests to see if a user is a group administrator of a group.
:Arguments: ``user``:
              A user-info or a user-object.
            ``group``:
              A group-info or a group.
:Returns: ``True`` if the user is a group administrator of the
          group. ``False`` otherwise (including if the user is a site
          administrator).
:Example: ``user_group_admin_of_group(self.loggedInUser, self.groupInfo)``
:See also: user_admin_of_group_, user_site_admin_of_group_

``user_site_admin_of_group``
-----------------------------

:Synopsis: ``user_site_admin_of_group(user, group)``
:Description: Tests to see if a user is a site administrator in a group.
:Arguments: ``user``:
              A user-info or a user-object.
            ``group``:
              A group-info or a group.
:Returns: ``True`` if the user is a site administrator. ``False`` otherwise
          (including if the user is a group administrator).
:Example: ``user_site_admin_of_group(self.loggedInUser, self.groupInfo)``
:See also: user_admin_of_group_, user_group_admin_of_group_
:Note: The historical function ``user_division_admin_of_group`` is the same
       as this function.

``user_participation_coach_of_group``
-------------------------------------

:Synopsis: ``user_participation_coach_of_group(user, group)``
:Description: Tests to see if a user is a participation coach in a group.
:Arguments: ``user``:
              A user-info or a user-object.
            ``group``:
              A group-info or a group.
:Returns: ``True`` if the user is the participation coach. ``False``
          otherwise.
:Example: ``user_participation_coach_of_group(self.loggedInUser, self.groupInfo)``

``get_group_userids``
---------------------

:Synopsis: ``get_group_userids(context, group)``
:Description: Gets the identifiers of all the group members.
:Arguments: ``context``:
              The context, used to acquire ``acl_users``.
            ``group``:
              Either the group identifier, a group-info, or a **site** info.
:Returns: A list of identifiers.
:Example: ``get_group_userids(self.context, self.groupInfo)``


Resources
=========

- Code repository: https://github.com/groupserver/gs.group.member.base
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17
