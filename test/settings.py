from os import environ


SESSION_CONFIGS = [
    dict(
        name='project2',
        display_name="project2",
        app_sequence=['project2', 'payment_info'],
        num_demo_participants=9,
    ),
    dict(
        name='guess_two_thirds',
        display_name="guess_two_thirds",
        app_sequence=['guess_two_thirds', 'payment_info'],
        num_demo_participants=3,
    ),
    
]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=200.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'BDT'
USE_POINTS = True

ROOMS = [
    dict(
        name='ESS_Lab',
        display_name='ESS Lab',
        participant_label_file='_rooms/ess_lab.txt',
    ),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
"""


SECRET_KEY = '2664064226354'

INSTALLED_APPS = ['otree']

DEBUG = False

ALLOWED_HOSTS = ['192.168.2.105']