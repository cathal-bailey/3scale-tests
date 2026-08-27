"""
Conftest for messages tests.

These tests require email notifcations to be enabled.
"""

import pytest


@pytest.fixture(scope="session", autouse=True)
def enable_notifications(openshift):
    """
    Enable notification preferences for all provider admin users.

    After porta PR #4039, notifications use a per-user NotificationPreferences model
    instead of account-level settings. In fresh deployments, notifications default to disabled.
    """
    rails_command = (
        "Account.providers.each { |p| "
        "p.admins.each { |a| "
        "a.notification_preferences.enabled_notifications |= "
        '["account_created", "application_created", "service_contract_created", "account_deleted", "service_deleted"]; '
        "a.notification_preferences.save! }; "
        "p.settings.service_plans_ui_visible = true; "
        "p.settings.save! }; "
        'puts "Notification preferences enabled for #{Account.providers.count} provider(s)"'
    )

    ocp = openshift()

    print("\n=== ENABLING NOTIFICATIONS FIXTURE ===")

    try:
        result = ocp.do_action(
            "exec",
            [
                "deployment/system-app",
                "-c",
                "system-master",
                "--",
                "bash",
                "-c",
                f"cd /opt/system && bundle exec rails runner '{rails_command}'",
            ],
        )
        print(f"Fixture result: {result.out()}")
        print(f"Fixture errors: {result.err()}")
    except Exception as e:
        print(f"ERROR in enable_notifications fixture: {e}")
        raise

    print("=== NOTIFICATIONS ENABLED ===\n")

    yield
