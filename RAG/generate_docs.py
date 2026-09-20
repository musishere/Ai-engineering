from pathlib import Path

OUT_DIR = Path(__file__).parent / "documents"

DOCS = {
    "password_reset": """How to Reset Your Password
To reset your password, go to the login page and click "Forgot password?"
Enter the email address associated with your account and submit the form.
You will receive an email with a password reset link within a few minutes.
Click the link, choose a new password that is at least 8 characters long,
and confirm it. Your new password takes effect immediately, and you will
be logged out of all other active sessions for security.""",

    "password_requirements": """Password Requirements
Passwords must be at least 8 characters long and contain at least one
uppercase letter, one lowercase letter, and one number. Special characters
are allowed but not required. Passwords cannot match your email address
or any of your last 5 previous passwords. We recommend using a password
manager to generate and store a strong, unique password.""",

    "account_locked": """What to Do If Your Account Is Locked
Your account is temporarily locked after 5 failed login attempts within
15 minutes. This is a security measure to prevent unauthorized access.
Locked accounts automatically unlock after 30 minutes. If you need
immediate access, use the "Forgot password?" link on the login page to
reset your password, which also clears the lock.""",

    "two_factor_auth": """Setting Up Two-Factor Authentication
Two-factor authentication (2FA) adds an extra layer of security to your
account. To enable it, go to Account Settings > Security and click
"Enable 2FA". Scan the QR code with an authenticator app such as Google
Authenticator or Authy. Enter the 6-digit code shown in the app to
confirm setup. Once enabled, you will need this code every time you log
in from a new device.""",

    "update_email": """How to Update Your Email Address
Go to Account Settings > Profile and click "Change email". Enter your new
email address and current password to confirm the change. A verification
link will be sent to the new address. Your email is not updated until you
click that verification link. Your old email remains active until
verification is complete.""",

    "account_settings_overview": """Account Settings Overview
The Account Settings page lets you manage your profile, security options,
notification preferences, and connected devices. You can access it from
the dropdown menu in the top-right corner of any page after logging in.
Changes to security settings, such as password or 2FA, may require you to
re-enter your current password.""",

    "billing_update_card": """Updating Your Payment Method
To update your payment method, go to Billing > Payment Methods and click
"Add card". Enter your new card details and click "Save". You can set any
saved card as the default. Removing a card that is currently set as
default will prompt you to choose a replacement before it can be deleted.""",

    "billing_cycle": """Understanding Your Billing Cycle
Subscriptions renew automatically on the same day each month as your
original signup date. You can view your next billing date under
Billing > Overview. If a renewal payment fails, we retry the charge up to
3 times over 7 days before the subscription is downgraded to the free
plan.""",

    "cancel_subscription": """How to Cancel Your Subscription
To cancel your subscription, go to Billing > Manage Plan and click
"Cancel Subscription". Your plan remains active until the end of the
current billing period; you will not be charged again after cancelling.
You can resubscribe at any time from the same page, and your account data
is retained for 90 days after cancellation.""",

    "refund_policy": """Refund Policy
Refunds are available within 14 days of a charge for annual plans, and
7 days for monthly plans. To request a refund, contact support with your
account email and the date of the charge. Refunds are processed to the
original payment method and typically appear within 5-10 business days.""",

    "notification_settings": """Managing Notification Preferences
You can control which emails and in-app notifications you receive from
Account Settings > Notifications. Options include product updates,
security alerts, and billing reminders. Security alerts, such as new
device logins, cannot be fully disabled but can be limited to email only.""",

    "connected_devices": """Managing Connected Devices
Account Settings > Devices shows every device currently signed in to your
account, along with its approximate location and last active time. You
can remotely sign out any device from this list. Signing out a device
does not delete any data associated with your account.""",

    "delete_account": """How to Delete Your Account
To permanently delete your account, go to Account Settings > Privacy and
click "Delete Account". You will be asked to confirm by re-entering your
password. Deletion is permanent after a 30-day grace period, during which
you can cancel the request by logging back in. All data is erased at the
end of the grace period and cannot be recovered.""",

    "api_key_management": """Managing API Keys
Developers can generate API keys from Account Settings > Developer >
API Keys. Each key can be scoped to read-only or read-write access.
Keys are shown only once at creation time, so store them securely.
Revoking a key takes effect immediately and cannot be undone.""",

    "contacting_support": """Contacting Support
If you cannot resolve an issue using the help center, you can contact
support via the "Help" button in the bottom-right corner of any page.
Include your account email and a description of the issue. Support
typically responds within 24 hours on business days.""",
}


def main():
    print(f"[generate] writing {len(DOCS)} documents to {OUT_DIR}")
    OUT_DIR.mkdir(exist_ok=True)
    for i, (slug, text) in enumerate(DOCS.items()):
        path = OUT_DIR / f"doc_{i:02d}_{slug}.txt"
        path.write_text(text.strip() + "\n")
        print(f"[generate] wrote {path.name} ({len(text.split())} words)")
    print(f"[generate] done, {len(DOCS)} documents in {OUT_DIR}")


if __name__ == "__main__":
    main()
