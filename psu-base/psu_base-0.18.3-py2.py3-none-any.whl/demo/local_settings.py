# -----------------------------------------------------------------------------
# REQUIRED VALUES
# -----------------------------------------------------------------------------
# Environment choices: {DEV, TEST, PROD}
ENVIRONMENT = 'DEV'

# Name of machine running the application
ALLOWED_HOSTS = ['localhost']

# Debug mode (probably only true in DEV)
DEBUG = True

# SSO URL
CAS_SERVER_URL = 'https://sso-stage.oit.pdx.edu/idp/profile/cas/login'

# `````````````````
# FINTI
# `````````````````
# REQUIRED: Finti URL and Token (uncomment these):
FINTI_TOKEN = "2144402c-586e-44fc-bd0c-62b31e98394d"
FINTI_URL = 'https://ws-test.oit.pdx.edu'

# Finti URLs (for reference)
# -  http://localhost:8888
# -  https://ws-test.oit.pdx.edu
# -  https://ws.oit.pdx.edu

# As-of psu-base 0.11.0, Finti responses can be cached for offline development
FINTI_SAVE_RESPONSES = True    # Save/record actual Finti responses for offline use?
FINTI_SIMULATE_WHEN_POSSIBLE = True

# Email Settings
EMAIL_HOST_USER = 'cefr-app-mail'
EMAIL_HOST_PASSWORD = 'EuDFxamEfm7y'

# -----------------------------------------------------------------------------
# OPTIONAL VALUES
# -----------------------------------------------------------------------------

# You may want to disable elevated developer access while running locally
# ELEVATE_DEVELOPER_ACCESS = False

# You may want to extend session expiration during local development
# SESSION_COOKIE_AGE = 4 * 60 * 60  # 4 hours
