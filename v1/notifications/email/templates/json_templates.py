from v1.notifications.email import events

TEMPLATES = {
    events.EVENT_FORGOT_PASSWORD: {
        'subject': 'Your password reset request',
        'title': 'Reset your password',
        'body': 'Click the below link or copy paste in a browser to reset your password. \n {link}'
    },
    events.EVENT_USER_VERIFICATION: {
        'subject': 'Please verify your Tandora Byo Link account',
        'title': 'Verify your account',
        'body': 'Your Tandora Byo Link account is created. Click or copy/paste the following link to verify '
                'your email {link}'
    }
}
