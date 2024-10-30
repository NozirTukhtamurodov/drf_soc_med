from split_settings.tools import optional, include


include(
    'components/base.py',
    'components/apps.py',
    'components/templates.py',
    'components/middlewares.py',
    'components/database.py',
    'components/auth.py',
    'components/rest_framework.py',
    'components/static.py',
    'components/local.py',
    optional('settings/production.py')
)
