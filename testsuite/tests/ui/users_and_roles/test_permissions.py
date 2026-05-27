"""Tests for user permissions in 3scale"""

import pytest

from testsuite.ui.views.admin.audience.billing import BillingView, BillingSettingsView
from testsuite.ui.views.admin.audience.developer_portal import (
    BotProtection,
    CMSEditPageView,
    CMSNewPageView,
    CMSNewSectionView,
    DeveloperPortalContentView,
)
from testsuite.ui.views.admin.foundation import AccessDeniedView

PERMISSIONS = ["portal", "finance", "settings", "partners", "monitoring", "plans", "policy_registry"]

VIEWS = [
    ("portal", DeveloperPortalContentView),
    ("portal", CMSNewPageView),
    ("portal", CMSNewSectionView),
    ("portal", CMSEditPageView),
    ("portal", BotProtection),
    ("finance", BillingView),
    ("finance", BillingSettingsView),
]


# pylint: disable=too-many-arguments
@pytest.mark.parametrize("user_permission", PERMISSIONS)
@pytest.mark.parametrize("required_permission, page_view", VIEWS)
def test_member_user_permissions_per_section(
    custom_admin_login,
    navigator,
    provider_member_user,
    user_permission,
    required_permission,
    page_view,
):
    """
    Tests user permissions permission per permission section
        - Creates a member user with a specific permission
        - Logs in as that member user
        - Attempts to access a specific UI page
        - If users permission matches page's required permission -> allowed
        - Else, access denied
        - partners, settings, monitoring and policy_registry to be added? More complicated
    """
    member_user = provider_member_user(allowed_sections=user_permission, allowed_services=False)
    custom_admin_login(member_user.entity_name, "123456")

    page = navigator.open(page_view, wait_displayed=False)
    access_denied_view = AccessDeniedView(navigator.browser.root_browser)

    if user_permission == required_permission:
        assert page.is_displayed, f"A user with {user_permission} should be able to access {page_view}"
    else:
        assert (
            access_denied_view.is_displayed
        ), f"A user with {user_permission} should not be able to access {page_view}"
