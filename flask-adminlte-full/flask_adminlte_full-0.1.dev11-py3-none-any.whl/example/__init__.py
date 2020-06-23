from types import SimpleNamespace
import json

from datetime import datetime, timedelta

from adminlte_base import Dropdown, Message, Notification, Task, ThemeColor, ThemeLayout, MenuLoader
from adminlte_base.data_types import PageItem
from babel import Locale
from flask import Flask, render_template, url_for, flash, request, abort, current_app, redirect
from flask_babelex import Babel, gettext, Domain
from flask_login import LoginManager, login_user, current_user
from flask_wtf import CSRFProtect, FlaskForm
from wtforms import fields as fld, validators as vd

from .extensions import adminlte, bcrypt
from .models import db, Menu, User
from .cli import init_group
from .routes import auth, site


app = Flask(__name__)
app.config.update({
    'SECRET_KEY': '123',
    'BABEL_DEFAULT_LOCALE': 'en',
    'ADMINLTE_HOME_PAGE': ('/blank', 'Dashboard'),
    # 'ADMINLTE_ALLOW_SOCIAL_AUTH': True,
    # 'ADMINLTE_LAYOUT': ThemeLayout.DEFAULT | ThemeLayout.COLLAPSED_SIDEBAR,
    'ADMINLTE_LAYOUT': ThemeLayout.TOP_NAV | ThemeLayout.COLLAPSED_SIDEBAR | ThemeLayout.FIXED_TOP_NAV,
    # 'ADMINLTE_MAIN_SIDEBAR_ENABLED': False,
    'ADMINLTE_SECOND_SIDEBAR_ENABLED': True,
    'ADMINLTE_SITE_TITLE': 'Demo app',
    'ADMINLTE_MESSAGES_ENABLED': True,
    'ADMINLTE_NOTIFICATIONS_ENABLED': True,
    'ADMINLTE_TASKS_ENABLED': True,
    'ADMINLTE_LEGACY_USER_MENU': True,
    'ADMINLTE_TERMS_ENDPOINT': 'site.terms',
    # 'ADMINLTE_SIDEBAR_LIGHT': True,
    'SQLALCHEMY_DATABASE_URI': 'sqlite:////tmp/test.db',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'SQLALCHEMY_ENGINE_OPTIONS': {
        'execution_options': {
            'autocommit': True,
        }
    }
})


babel = Babel(app, default_domain=Domain(domain='adminlte_full'))
CSRFProtect(app)
login_manager = LoginManager(app)
db.init_app(app)
adminlte.init_app(app)
bcrypt.init_app(app)
app.cli.add_command(init_group)
app.register_blueprint(auth.bp)
app.register_blueprint(site.bp)


@babel.localeselector
@adminlte.manager.current_locale_getter
def get_locale():
    if current_user.is_anonymous or not current_user.locale:
        # print(request.accept_languages)
        return request.accept_languages.best_match(['uk_UA', 'ru_RU', 'en_US'])
    return current_user.locale


@adminlte.manager.available_languages_loader
def load_languages():
    for l in ('ru_RU', 'uk_UA', 'ro_MD', 'en_US'):
        # yield l, Locale.parse(l).get_language_name().title()
        yield l, Locale.parse(l).get_display_name().title()

    # return (
    #     ('ru_RU', 'Русский'),
    #     ('uk_UA', 'Українська'),
    #     ('en_US', 'English'),
    # )
    #
    # return {
    #     'ru_RU': 'Русский',
    #     'uk_UA': 'Українська',
    #     'en_US': 'English',
    # }


@adminlte.manager.menu_loader
class MyMenuLoader(MenuLoader):
    def load(self, program_name):
        return Menu.query.filter_by(program_name=program_name).first()

    def navbar_menu(self, active_path=None):
        data = self.load('navbar_menu')

        if data:
            return self._create(data, active_path)

    def sidebar_menu(self, active_path=None):
        data = self.load('main_menu')

        if data:
            return self._create(data, active_path)


# @adminlte.manager.home_page_getter
# def home_page():
#     if current_user.is_anonymous:
#         return '/', 'Login'
#     return '/', 'Home'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
def index():
    return render_template('adminlte_full/skeleton.html')


@app.route('/change_locale/<locale>')
def change_language(locale):
    name = adminlte.manager.get_available_languages(as_dict=True).get(locale)

    if name is None:
        adminlte.flash.error('The selected language is not supported.')
    elif current_user.is_authenticated:
        current_user.locale = locale
        db.session.commit()
        adminlte.flash.success(f'Language successfully changed to "{name}".')

    return redirect(url_for('blank'))


@app.route('/layout/<layout>.html')
def layouts_options(layout):
    layout = layout.upper().replace('-', '_')

    title = layout.title().replace('_', ' ')
    layout = getattr(ThemeLayout, layout, set())

    if ThemeLayout.TOP_NAV <= layout:
        layout |= ThemeLayout.COLLAPSED_SIDEBAR
    else:
        layout |= ThemeLayout.DEFAULT

    return render_template('pages/layouts_options.html', layout=layout, title=title)


@app.route('/error/<int:code>')
def error_page(code):
    abort(code)


@app.route('/search')
def search():
    return render_template('adminlte_full/search_results.html', q=request.args['q'])


@app.route('/widgets')
def widgets():
    return render_template('pages/widgets.html')


@app.route('/UI/general')
def ui_general():
    return render_template('pages/UI/general.html')


@app.route('/tables/simple')
def tables_simple():
    context = {
        'task_table': {
            'headers': ['Task', 'Progress', 'Label'],
            'data': [
                {'task': 'Update software', 'progress': 55, 'color': ThemeColor.PRIMARY},
                {'task': 'Clean database', 'progress': 70, 'color': ThemeColor.WARNING},
                {'task': 'Cron job running', 'progress': 30, 'color': ThemeColor.DANGER},
                {'task': 'Fix and squish bugs', 'progress': 90, 'color': ThemeColor.SUCCESS}
            ]
        },
        'user_table': {
            'headers': {
                'id': 'ID',
                'user': 'User',
                'date': 'Date',
                'status': 'Status',
                'reason': 'Reason'
            },
            'data': json.load(open('users.json')),
        },
        'pages': [PageItem('&laquo;'), PageItem(1), PageItem(2), PageItem(3), PageItem('&raquo;')],
    }
    return render_template('pages/tables/simple.html', **context)


@app.route('/tables/data')
def tables_data():
    headers = {
        'engine': 'Rendering engine',
        'browser': 'Browser',
        'platform': 'Platform(s)',
        'version': 'Engine version',
        'grade': 'CSS grade'
    }

    data = json.load(open('data.json'))
    data_dict = [dict(zip(headers, v)) for v in data]

    context = {
        'browser_table': {
            'headers': headers,
            'data': data,
            'data_dict': data_dict,
        }
    }

    return render_template('pages/tables/data.html', **context)


@app.route('/blank')
def blank():
    flash('%s SQL statements were executed.' % 666, 'debug')
    flash('SQL statements were executed.')
    flash('Three credits remain in your account.', 'info')
    flash('Profile details updated.', 'success')
    flash('Your account expires in three days.', 'warning')
    flash('Document deleted.', 'error')
    return render_template('adminlte_full/base.html')


@app.route('/profile')
def profile():
    return f'{current_user}'


# @app.route('/registration', endpoint='auth.registration')
# def registration():
#     return render_template('adminlte_full/recover_password.html')
#     return render_template('adminlte_full/forgot_password.html')


@app.route('/lockscreen.html', endpoint='auth.lockscreen', methods=['GET', 'POST'])
def lockscreen():
    return render_template('adminlte_full/lockscreen.html')


@adminlte.manager.messages_loader
def load_messages():
    messages = Dropdown('#', 15)

    if current_user.is_authenticated:
        now = datetime.now()
        sender = current_user

        messages.add(Message(sender, 'Тестовое сообщение 1', '#', sent_at=now - timedelta(seconds=16)),)
        messages.add(Message(sender, 'Тестовое сообщение 2', '#', sent_at=now - timedelta(weeks=2)),)
        messages.add(Message(sender, 'Тестовое сообщение 3', '#'))

    return messages


@adminlte.manager.notifications_loader
def load_notifications():
    notifications = Dropdown('#', 10)
    notifications.add(Notification(
        '4 new messages',
        datetime.now() - timedelta(seconds=16),
        icon='fas fa-envelope',
        color=ThemeColor.SUCCESS
    ))
    notifications.add(Notification(
        '8 friend requests',
        datetime.now() - timedelta(hours=3),
        icon='fas fa-users'
    ))
    notifications.add(Notification(
        '3 new reports',
        icon='fas fa-file',
        color=ThemeColor.DANGER
    ))

    return notifications


@adminlte.manager.tasks_loader
def load_tasks():
    tasks = Dropdown('#')
    tasks.add(Task('Design some buttons', 20, '#'))
    tasks.add(Task('Create a nice theme', 40, '#', color=ThemeColor.SUCCESS))
    tasks.add(Task('Some task I need to do', 60, '#', color=ThemeColor.DANGER))
    tasks.add(Task('Make beautiful transitions', 80, '#', color=ThemeColor.WARNING))
    return tasks


db.create_all(app=app)
