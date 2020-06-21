#!/usr/bin/env python3

import sys
import os
import datetime
import urwid # Curses interface
import requests # Fetch data from APIs
import ast # Safely parse "python" API output
import syslog
from threading import Thread # To run API requests non-blocking
import appdirs
import configparser
import enum
import simplejson # Exeptions from requests
import time

class Mode(enum.Enum):
    alertlist = 0 # Default
    events = 1
    eventdetails = 2
    ack = 3
    comment = 4
    downtime = 5
    help = 6
    details = 7
    reinventorize = 8
    reschedule = 9
    allhosts = 10
    hostfilter = 11


class FilteredListBox(urwid.ListBox):
    ''' Inherit and override to catch arrow navigation in Listbox '''
    def keypress(self, size, key):
        if key == 'up':
            key = 'k'
        elif key == 'down':
            key = 'j'
        elif key == 'page down':
            key = 'l'
        elif key == 'page up':
            key = 'h'

        return urwid.ListBox.keypress(self, size, key)


class Chk:
    project_name = 'check-commander'
    list_position = 0
    version = '1.3.1'
    mode = Mode.alertlist
    focused_line = None
    status = 'Starting...'
    list_position = 0
    config_path = ''
    api_base_url = ''
    delay = 5
    host = None
    service = None
    url_with_hostname = 'http://wiki.example.com/?q=HOSTNAME'
    terminal_command = 'x-terminal-emulator -e ssh HOSTNAME'
    hostfilter = ''

    @staticmethod
    def fetch_time():
        ''' Return a formated time '''
        return '{0:%H:%M:%S}'.format(datetime.datetime.now())

    @staticmethod
    def parse_time(text):
        ''' Input can be  2h, 100, 4h, 5m, 333s.
        Will return a positive number of seconds or -1 for no time.'''

        time_designators = {'s': 1, 'm': 60, 'h': 3600, 'd': 84600}

        text = text.strip()
        time_designator = ''
        number = text

        # Need more than one character, no spaces please, no negative values
        if len(text) < 2 or ' ' in text or '-' in text:
            return -1

        for td in time_designators:
            if text.endswith(td):
                time_designator = td
                break

        try:
            number = int(text.replace(time_designator,''))
        except ValueError:
            return -1

        try:
            number = number*time_designators[time_designator]
        except KeyError:
            pass

        return number

    @staticmethod
    def scrub_secret (text):
        ''' Check urls for the automation secret and scrubb it away '''
        standin='*redacted*'

        if '_secret' in text:
            secret_start = text.index('_secret=')
            secret_end = len(text)

            try:
                secret_end = text.index('&', secret_start)
            except ValueError:
                pass

            text = text[:secret_start] + standin + text[secret_end:]
        return text

    def validate_config(self):
        ''' If config file exists, load config. Else create a default
            config and use that. '''

        if not self.config_path: # Allow unit testing to pre-set a config
            self.config_path = appdirs.user_config_dir(self.project_name) + '.ini'

        config = configparser.ConfigParser()
        config.read(self.config_path)

        # Create default
        if not os.path.isfile(self.config_path):
            print(f"No config found, creating one at {self.config_path}")

            self.checkmkhost = input("Full address to your checkmk host " + \
                "including 'site', example http://checkmk.example.com/mysite/: ")
            self.checkmkusername = input('Username. Must be a "machine" user ' + \
                'with a secret, not a password: ')
            self.checkmksecret = input('Secret: ')

            config.add_section('main')
            config.set('main', 'host', self.checkmkhost)
            config.set('main', 'username', self.checkmkusername)
            config.set('main', 'secret', self.checkmksecret)
            config.set('main', 'delay', str(self.delay)) # Default refresh value
            config.set('main', 'url_with_hostname', self.url_with_hostname)
            config.set('main', 'terminal_command', self.terminal_command)

            with open(self.config_path, 'w') as f:
                config.write(f)

        # Load existing
        else:
            self.checkmkhost = config.get('main', 'host')
            self.checkmkusername = config.get('main', 'username')
            self.checkmksecret = config.get('main', 'secret')
            self.delay = config.getint('main', 'delay', fallback=5)
            self.url_with_hostname = config.get('main', 'url_with_hostname',
                fallback=self.url_with_hostname)
            self.terminal_command = config.get('main', 'terminal_command',
                fallback=self.terminal_command)

        self.api_base_url = self.checkmkhost + \
            'check_mk/view.py' + \
            '?_transid=-1' + \
            '&_do_actions=yes&_do_confirm=yes' + \
            '&output_format=json&_username=' + \
            self.checkmkusername + \
            '&_secret=' + \
            self.checkmksecret

    def main(self):
        syslog.syslog(f"{self.project_name} version {self.version} started.")

        self.validate_config()

        # Load GUI
        self.setup_view()

        # Color palette
        palette = [ # http://urwid.org/manual/displayattributes.html#foreground-background
            # Name of the display attribute, typically a string
            # Foreground color and settings for 16-color (normal) mode
            # Background color for normal mode
            # Settings for monochrome mode (optional)
            # Foreground color and settings for 88 and 256-color modes (optional, see next example)
            # Background color for 88 and 256-color modes (optional)
            ('header', 'black', 'light gray'),
            ('reveal focus', 'black', 'dark cyan', 'standout'),
            ('CRIT', 'dark red', '', '', '', ''),
            ('WARN', 'yellow', '', '', '', ''),
            ('UNKN', 'dark magenta', '', '', '', ''),
            ('New', 'white', '', '', '', ''),
            ('Old', 'brown', '', '', '', ''),
            ('darker', '', 'dark gray', '', '', ''),
            ('Connected', '', 'dark green', '', '', ''),
            ('Disonnected', '', 'dark red', '', '', '')
        ]

        # Main loop
        self.loop = urwid.MainLoop(
            self.top,
            palette,
            unhandled_input=self.handle_key_input,
            handle_mouse=False
        )
        self.loop.set_alarm_in(
            self.delay, #if self.mode == Mode.alertlist else self.delay*2,
            self.refresh_ui
        )
        self.loop.run()

    def refresh_ui(self, loop=None, data=None, norepeat=False):
        ''' Refresh GUI, and set alarm for next refresh.

            norepeat is a workaround, which allows refreshing UI without setting an
            alarm each time, thus building up a bunch of alarms that keep refreshing. '''

        if self.mode in [Mode.alertlist, Mode.events, Mode.allhosts]:
            self.setup_view()
            self.loop.widget = self.top

        # Hostfilter is a special case. Update in background while showing dialog
        elif self.mode == Mode.hostfilter:
            self.setup_view()
            self.loop.widget = self.top
            self.show_hostfilter()

        if not norepeat:
            self.loop.set_alarm_at(
                time.time() + self.delay,
                self.refresh_ui
            )

    def escape_key(self):
        ''' When Esc pressed, return to default window '''
        if self.mode == Mode.eventdetails: # Escape from event details back to events
            self.mode = Mode.events

        elif self.mode != Mode.alertlist: # Escape from anything else, back to normal list
            self.status = ''
            self.mode = Mode.alertlist

        self.refresh_ui(norepeat=True)

    def list_set_focus(self):
        try:
            self.listbox.set_focus(self.list_position)
        except IndexError: # (empty listbox)
            pass

    def handle_key_input(self, input):
        ''' Handle key presses '''

        # Quit
        if input in ['q', 'Q']:
            raise urwid.ExitMainLoop()

        # Escape from actions
        if input == 'esc':
            self.escape_key()

        # Navigate list
        elif input in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            self.list_position = int(input)
            self.list_set_focus()

        elif input in ('home', 'g'):
            self.list_position = 0
            self.list_set_focus()

        elif input in ('end', 'G'):
            self.list_position = len(self.listbox.body)-1
            self.list_set_focus()

        elif (input == 'k') and len(self.listbox.body) > 0:
            focus_widget, self.list_position = self.listbox.get_focus()
            if self.list_position > 0:
                self.list_position -= 1
            self.list_set_focus()

        elif (input == 'j') and len(self.listbox.body) > 0:
            focus_widget, self.list_position = self.listbox.get_focus()
            if self.list_position+1 < len(self.listbox.body):
                self.list_position += 1
            self.list_set_focus()

        elif input == 'l' and len(self.listbox.body) > 0:
            focus_widget, self.list_position = self.listbox.get_focus()
            if self.list_position+10 < len(self.listbox.body):
                self.list_position += 10
            self.list_set_focus()

        elif input == 'h' and len(self.listbox.body) > 0:
            focus_widget, self.list_position = self.listbox.get_focus()
            if self.list_position-10 > len(self.listbox.body):
                self.list_position -= 10
            else:
                self.list_position = 0
            self.list_set_focus()

        elif input == '?': # Help
            self.show_help()

        elif input == 'a': # Acknowledge
            self.verify_acknowledge()

        elif input == 'c': # Comment
            self.verify_comment()

        elif input == 'd': # Downtime
            self.verify_downtime()

        elif input == 'r': # Reinventorize
            self.verify_reinvetorize()

        elif input == 's': # Reschedule check
            self.verify_reschedule_check()

        elif input == 'b': # Open checkmk website
            self.open_browser()

        elif input == 'e': # Events
            self.mode = Mode.events
            self.refresh_ui(norepeat=True)

        elif input == 'y': # Yank - copy text to clipboard
            self.yank_selection()
            self.refresh_ui(norepeat=True)

        elif input == 'w': # Open host in configurable website
            self.open_url_with_hostname()

        elif input == 't': # Execute command on hostname
            self.open_terminal_to_host()

        elif input == '/': # Search all hosts
            self.show_hostfilter()

        elif input == 'enter': # Handle Enter, which could mean loads of stuff

            # Done with hostfilter, back to allhosts
            if self.mode == Mode.hostfilter:
                self.mode = Mode.allhosts
                self.refresh_ui(norepeat=True)
                return

            # Parse time if a time-related command has been sent
            time = self.commandinput.caption
            try:
                time = int(str(time.split('[')[1]).split(']')[0])
            except IndexError:
                time = None

            # Check if service or host
            if self.service and self.service == 'Host is down':
                self.service = None

            # Verified ack
            if self.mode == Mode.ack:
                self.acknowledge_service(
                    host = self.target,
                    service = self.service,
                    time = time,
                    comment = self.commandinput.get_edit_text())
                self.refresh_ui(norepeat=True)

            # Verified comment
            elif self.mode == Mode.comment:
                self.comment_service(
                    host = self.target,
                    service = self.service,
                    # TODO: time = time,
                    comment = self.commandinput.get_edit_text())
                self.refresh_ui(norepeat=True)

            # Verified downtime
            elif self.mode == Mode.downtime:
                self.downtime_service(
                    host = self.target,
                    service = self.service,
                    time = time,
                    comment = self.commandinput.get_edit_text())
                self.refresh_ui(norepeat=True)

            # Verified reschedule
            elif self.mode == Mode.reschedule:
                self.reschedule_check(
                    host = self.target,
                    service = self.service)

            # Verified reinvent.
            elif self.mode == Mode.reinventorize:
                self.reinventorize_host(self.target)
                self.refresh_ui(norepeat=True)

            # Done with detail, back to alertlist
            elif self.mode == Mode.details:
                self.mode = Mode.alertlist
                self.refresh_ui(norepeat=True)

            else: # Show details
                try:
                    focus_widget, self.list_position = self.listbox.get_focus()
                except IndexError:
                    return

                self.host = focus_widget.base_widget.widget_list[1].text
                try:
                    self.service = focus_widget.base_widget.widget_list[2].text
                    self.output = ''
                    self.output = focus_widget.base_widget.widget_list[3].base_widget.text
                except IndexError:
                    self.output = ''

                # Show last 5 service comments
                comment_list = self.fetch_comments(self.host, self.service)
                comments = "Last five comments:\n"
                for comment_author, comment_comment, comment_time, \
                    _, _ in comment_list[:5]:
                    comments += f"{comment_time} - {comment_author}: {comment_comment}\n"

                if self.mode == Mode.alertlist:
                    self.mode = Mode.details
                elif self.mode == Mode.allhosts:
                    pass #self.mode = Mode.allhosts
                else: # event list
                    self.mode = Mode.eventdetails

                self.dialog([
                        'Service details',
                        f"{self.host} - {self.service}\n",
                        f"{self.output}\n\n",
                        f"{comments}",
                    ]
                )

    def show_hostfilter(self):
        self.mode = Mode.hostfilter
        self.commandinput.set_caption('Hostname > ')
        self.commandinput.set_edit_text(self.hostfilter)

        self.dialog(
            [
                'Search for hostname',
                'Type part of a hostname and hit enter.\n\n',
                'Esc to abort.\n'
            ],
        self.commandinput
        )

    def verify_acknowledge(self):
        try:
            focus_widget, self.list_position = self.listbox.get_focus()
        except IndexError:
            return
        if not focus_widget:
            return

        self.target = focus_widget.base_widget.widget_list[1].text
        self.service = focus_widget.base_widget.widget_list[2].text
        self.mode = Mode.ack
        self.commandinput.set_caption('Ack > ')

        self.dialog(
            [
                'Acknowledge',
                'Ack <%s, %s> ?\n\n' % (self.target, self.service),
                'Type an optional time designator, a required comment and' +
                'hit enter.\n\n I.e. "2h Not in prod yet".\n\n',
                'Esc to abort.\n'
            ],
        self.commandinput
        )

    def verify_comment(self):
        try:
            focus_widget, self.list_position = self.listbox.get_focus()
        except IndexError:
            return
        if not focus_widget:
            return

        self.target = focus_widget.base_widget.widget_list[1].text
        self.service = focus_widget.base_widget.widget_list[2].text
        self.mode = Mode.comment
        self.commandinput.set_caption('Comment > ')

        self.dialog(
            [
                'Comment <%s, %s> ?\n\n' % (self.target, self.service),
                'Type a comment and hit enter.\n\n',
                'Esc to abort.\n'
            ],
            self.commandinput
        )

    def verify_downtime(self):
        try:
            focus_widget, self.list_position = self.listbox.get_focus()
        except IndexError:
            return
        if not focus_widget:
            return

        self.target = focus_widget.base_widget.widget_list[1].text
        self.service = focus_widget.base_widget.widget_list[2].text
        self.mode = Mode.downtime
        self.commandinput.set_caption('Down > ')

        self.dialog(
            [
                'Downtime',
                'Downtime <%s, %s> ?\n\n' % (self.target, self.service),
                'Type an optional time designator, a required comment and' +
                'hit enter.\n\n I.e. "2h Not in prod yet".\n\n',
                'Esc to abort.\n'
            ],
            self.commandinput
        )

    def verify_reinvetorize(self):
        ''' Open a dialog, asking user to verify a reinvetorize '''

        try:
            focus_widget, self.list_position = self.listbox.get_focus()
        except IndexError:
            return
        if not focus_widget:
            return

        self.target = focus_widget.base_widget.widget_list[1].text
        self.service = focus_widget.base_widget.widget_list[2].text
        self.mode = Mode.reinventorize
        self.commandinput.set_caption('Confirm > ')

        self.dialog(
            [
                'Reinventorize',
                'Fix all missing/vanished for <%s>?\n\n' % self.target,
                'Enter to confirm, Esc to abort.\n'
            ],
            self.commandinput
        )

    def verify_reschedule_check(self):
        ''' Open a dialog, asking user to verify a reschedule '''

        try:
            focus_widget, self.list_position = self.listbox.get_focus()
        except IndexError:
            return
        if not focus_widget:
            return

        self.target = focus_widget.base_widget.widget_list[1].text
        self.service = focus_widget.base_widget.widget_list[2].text
        self.mode = Mode.reschedule
        self.commandinput.set_caption('Confirm > ')

        self.dialog(
            [
                'reSchedule',
                'Reschedule check for <%s>?\n\n' % self.target,
                'Enter to confirm, Esc to abort.\n'
            ],
            self.commandinput
        )

    def open_browser(self):
        ''' Open configured checkmk site in browser. '''

        try:
            import webbrowser
        except ModuleNotFoundError:
            self.write_status_and_log("You need webbrowser installed from pip.")
            return

        self.write_status_and_log("Opening checkmk website")
        webbrowser.open(self.checkmkhost, new=2)

    def yank_selection(self):
        ''' Copy selected line to clipboard. Complain if clipboard module is missing. '''

        try:
            import clipboard
        except ModuleNotFoundError:
            self.status = f"{Chk.fetch_time()} You need clipboard installed " \
                + "from pip. And more if on linux: " \
                + "https://pyperclip.readthedocs.io/en/latest/index.html#not-implemented-error"
            return

        if self.mode == Mode.alertlist:
            try:
                focus_widget, self.list_position = self.listbox.get_focus()
            except IndexError:
                return
            if not focus_widget:
                return

            self.target = focus_widget.base_widget.widget_list[1].text
            self.service = focus_widget.base_widget.widget_list[2].text
            description = focus_widget.base_widget.widget_list[3].base_widget.text
            # TODO: include some timestamp

            clipboard.copy(f"{self.target} - {self.service} - {description}")
            self.status = f"{Chk.fetch_time()} Yanked text to clipboard."
            self.refresh_ui(norepeat=True)
        else:
            self.status = f"{Chk.fetch_time()} Yank only implemented in list view."

    def show_help(self):
        ''' Show help dialog '''

        self.mode = Mode.help
        self.dialog(
            [
                'Help - Check Commander version %s' % self.version,
                '? - This dialog\n' +\
                'Esc - Close dialogs\n' +\
                'q - Quit\n' +\
                '←↓→, hjkl, 0-9, Home, End - Select line\n' +\
                'Enter - Show details for selected service\n' +\
                'a - Acknowledge\n' +\
                'r - Reinventorize (fix missing/vanished)\n' +\
                'c - Comment\n' +\
                's - reSchedule check\n' +\
                '/ - search for host\n' +\
                'b - Open checkmk in web Browser\n' +\
                'e - Show host- and service Events\n' +\
                'y - Yank / copy text to clipboard\n' +\
                'w - Open current host in configurable Web site\n' +\
                't - Open Terminal with SSH to current host\n'
            ],
            align = 'left',
        )

    def open_url_with_hostname(self):
        ''' Will attempt to open an url in web browser.
            HOSTNAME will be replaced with current selected host. '''

        try:
            import webbrowser
        except ModuleNotFoundError:
            self.write_status_and_log("You need webbrowser installed from pip.")
            return

        if self.mode != Mode.alertlist:
            return

        try:
            focus_widget, self.list_position = self.listbox.get_focus()
        except IndexError:
            return
        if not focus_widget:
            return
        self.target = focus_widget.base_widget.widget_list[1].text

        url = self.url_with_hostname.replace('HOSTNAME', self.target)

        self.write_status_and_log(f"Opening host in website {url}")
        webbrowser.open(url, new=2)

    def open_terminal_to_host(self):
        ''' Open ssh to host in a new terminal '''

        if self.mode not in (Mode.alertlist, Mode.allhosts):
            return

        try:
            focus_widget, self.list_position = self.listbox.get_focus()
        except IndexError:
            return
        if not focus_widget:
            return
        self.target = focus_widget.base_widget.widget_list[1].text
        cmd = self.terminal_command.replace('HOSTNAME', self.target)
        self.write_status_and_log(f"{Chk.fetch_time()} Opening ssh to host {self.target}. Command {cmd}")

        os.system(cmd)

    def draw_alertlist(self):
        ''' Fetch and build list of alerts '''

        line_number = num_down = 0
        listbox_content = []
        top_right_status = ''

        services = self.fetch_serviceproblems()
        hosts = self.fetch_hostproblems()

        for service_state, host, _, _, _, _, _, _ in hosts:

            listbox_content += urwid.Columns(
            [
                ('weight', 1, urwid.Text(str(line_number))),
                ('weight', 4, urwid.Text(host, wrap='clip')),
                ('weight', 4, urwid.Text('Host is down', wrap='clip')),
                ('weight', 10, urwid.AttrMap(urwid.Text('DOWN', wrap='clip'), service_state)),
                ('weight', 2, urwid.Text('', wrap='clip')),
            ], dividechars=1),
            line_number += 1
            num_down += 1

        num_crit = num_warn = 0
        for service_state, host, service_description, _, svc_plugin_output, \
            svc_state_age, _, _ in services:

            # Format time
            timestamp_style = 'Disconnected'
            if 'm' in svc_state_age: # Younger than an hour
                timestamp_style = 'New'
            if 's' not in svc_state_age \
                and 'm' not in svc_state_age \
                and 'h' not in svc_state_age:
                svc_state_age = svc_state_age.split()[0]

            listbox_content += urwid.Columns(
            [
                ('weight', 1, urwid.Text(str(line_number))),
                ('weight', 4, urwid.Text(host, wrap='clip')),
                ('weight', 4, urwid.Text(service_description, wrap='space')),
                ('weight', 10, urwid.AttrMap(urwid.Text(svc_plugin_output, wrap='clip'), service_state)),
                ('weight', 2, urwid.AttrMap(urwid.Text(svc_state_age, wrap='clip'), timestamp_style))
            ], dividechars=1),
            line_number += 1

            if service_state == 'CRIT':
                num_crit += 1
            elif service_state == 'WARN':
                num_warn += 1

        top_right_status = f'Down: {num_down} Crit: {num_crit} Warn: ' +\
            f'{num_warn} '
        return listbox_content, top_right_status

    def draw_eventlist(self):
        ''' Fetch and build list of events '''

        listbox_content = []
        top_right_status = ''

        events = self.fetch_events()

        for _, log_time, log_type, host, service_description, \
            log_state_type, log_plugin_output in events:
            listbox_content += urwid.Columns(
            [
                ('weight', 1, urwid.Text(log_time, wrap='clip')),
                ('weight', 3, urwid.Text(log_type, wrap='clip')),
                ('weight', 1, urwid.Text(host, wrap='clip')),
                ('weight', 3, urwid.Text(service_description, wrap='clip')),
                ('weight', 1, urwid.Text(log_state_type, wrap='clip')),
                ('weight', 5, urwid.Text(log_plugin_output, wrap='clip')),
            ], dividechars=1),

        top_right_status = f' Fetched events from last ten minutes: {len(events)} '
        return listbox_content, top_right_status

    def draw_allhosts(self):
        ''' Fetch and build list of all hosts '''

        line_number = 0
        listbox_content = []
        top_right_status = 'Filter: %s' % self.hostfilter

        hosts = self.fetch_all_hosts(self.hostfilter)

        # host_state', 'host', 'host_icons', 'num_services_ok', 'num_services_warn', 
        #'num_services_unknown', 'num_services_crit', 'num_services_pending'],

        for host_state, host, _, num_services_ok, num_services_warn, \
            num_services_unknown, num_services_crit, num_services_pending in hosts:
            service_states = f'OK: {num_services_ok}, WARN: {num_services_warn}, ' +\
                f'UNK: {num_services_unknown}, CRIT: {num_services_crit}, PEND: ' +\
                f'{num_services_pending}'
            listbox_content += urwid.Columns(
            [
                #('weight', 1, urwid.Text(str(line_number))),
                ('weight', 1, urwid.Text(host_state, wrap='clip')),
                ('weight', 4, urwid.Text(host, wrap='clip')),
                ('weight', 4, urwid.Text(service_states, wrap='clip')),
            ], dividechars=1),
            line_number += 1

        return listbox_content, top_right_status

    def setup_view(self):
        ''' Draw list based on self.mode '''

        if self.mode == Mode.alertlist:
            listbox_content, top_right_status = self.draw_alertlist()
        elif self.mode in (Mode.allhosts, Mode.hostfilter):
            listbox_content, top_right_status = self.draw_allhosts()
            if self.mode == Mode.hostfilter:
                self.show_hostfilter()

        else: # mode events
            listbox_content, top_right_status = self.draw_eventlist()

        self.listbox = FilteredListBox(urwid.SimpleListWalker([
                urwid.AttrMap(w, None, 'reveal focus') for w in listbox_content]))
        try:
            self.listbox.set_focus(self.list_position)
        except IndexError: # No alerts
            pass

        # Top menu
        return_instructions = ''
        if self.mode != Mode.alertlist:
            return_instructions = ' (Esc to return)'

        self.show_key = urwid.Text([
            ('darker',
            f"{self.project_name} → {self.mode.name} {return_instructions}"),
            f" Updated {Chk.fetch_time()} | {top_right_status}",
            ('darker',' ? for help')
        ], wrap='space')
        head = urwid.AttrMap(self.show_key, 'header')

        # Input box
        self.commandinput = urwid.Edit()
        urwid.connect_signal(self.commandinput, 'postchange', self.command_changed)

        if self.status == 'Starting...':
            # Show site overview on start
            self.status = f'{Chk.fetch_time()} connected to sites: '
            sites = self.fetch_sites()
            for site_name, _ in sites:
                self.status += f"{site_name}, "

        self.statusbar = urwid.Text(('darker', self.status))

        # top : listbox, head
        self.top = urwid.Frame(self.listbox, header=head, footer=self.statusbar)

    def fetch_serviceproblems(self):
        ''' Fetch unhandled service problems
        
            # Example returned: [
            # ['service_state', 'host', 'service_description', 'service_icons', 
            #   'svc_plugin_output', 'svc_state_age', 'svc_check_age', 'perfometer'],
            # ['CRIT',u'laptop1016',u'Memory','themes/facelift/images/icon_menu 
            #   themes/facelift/images/icon_pnp ack comment',u'CRIT - RAM used: 13.5 GB of  ...
         '''
        r = None
        url = self.api_base_url +\
                '&is_service_acknowledged=0' + \
                '&view_name=svcproblems'

        try:
            r = requests.get(url)
        except requests.exceptions.MissingSchema as e:
            print(f"Error fetching service problems. Wrong checkmk url? " \
                + f"Check url in config file {self.config_path}. Error: {e}")
            sys.exit(1)
        except requests.exceptions.ConnectionError:
            self.write_status_and_log(message=f'Temporary error connecting to {url}')
            return ''
        except simplejson.errors.JSONDecodeError:
            self.write_status_and_log(message=f'Temporary error connecting to {url} in fetch_serviceproblems')
            return ''

        if 'ERROR: Invalid automation secret' in r.text:
            print(f"Error fetching service problems. Wrong auth? Check user " \
                + "and sercret in config file {self.config_path}. Error " \
                + "message from server: {r.text}")
            sys.exit(1)

        # Remove first line (header)
        try:
            return r.json()[1::]
        except simplejson.errors.JSONDecodeError:
            self.write_status_and_log(message=f'Temporary error parsing from {url} in fetch_serviceproblems')
            return ''

    def fetch_hostproblems(self):
        ''' Fetch unhandled host problems

            # Example output
            ['DOWN', 'centos7.lxd', 'themes/facelift/ima.../icon_pnp', '37', '5', '0', '2', '0'] '''

        r = None
        url = self.api_base_url + \
                '&is_host_acknowledged=0' + \
                '&view_name=hostproblems'
        try:
            r = requests.get(url)
        except requests.exceptions.ConnectionError:
            self.write_status_and_log(message=f'Temporary error connecting to {url}')
            return ''

        # Remove first line (header) and reverse the list
        try:
            return (r.json()[1::])[::-1]
        except simplejson.errors.JSONDecodeError:
            self.write_status_and_log(message=f'Temporary error connecting to {url} in fetch_hostproblems')
            return ''

    def dialog(self, text, edit = None, align='center'):
        '''
        Overlays a dialog box on top of the console UI
        Args:
            text (list): A list of strings to display. First string will be header
            edit (edit widget): An edit box to type a response in
        '''

        # Header
        header_text = urwid.Text(
            ('banner', f'{self.project_name} - %s' % text[0] ),
            align = 'center'
        )
        header = urwid.AttrMap(header_text, 'banner')

        # Body
        body_text = urwid.Text(text[1:], align = align)
        body_filler = urwid.Filler(body_text, valign = 'top')
        body_padding = urwid.Padding(
            body_filler,
            left = 1,
            right = 1
        )
        body = urwid.LineBox(body_padding)

        try:
            edit.set_edit_pos(100)
        except AttributeError:
            pass
        footer = edit

        # Layout
        layout = urwid.Frame(
            body,
            header = header,
            footer = footer,
            focus_part = 'footer'
        )

        w = urwid.Overlay(
            urwid.LineBox(layout),
            self.top,
            align = 'center',
            valign = 'middle',
            width = 75,
            height = 20
        )
        self.loop.widget = w

    def acknowledge_service(self, host, service = None, time = None, comment=''):
        ''' Ack a service or host problem with optional comment and time '''

        url = self.api_base_url +\
            '&host=' + host + \
            '&_acknowledge=Acknowledge&_ack_sticky=on&_ack_notify=on' + \
            '&_ack_comment=' + comment + \
            '&host=' + host

        if service:
            url += '&view_name=service' + \
                '&service=' + service

        else: # Ack host
            url += '&view_name=hoststatus'

        if time:
            url += '&_ack_expire_minutes=' + str(time//60)

        t = Thread(target = self.background_request, args =(url, f'ack {host} - {service}' )) 
        t.start()

        self.mode = Mode.alertlist
        self.refresh_ui(norepeat=True)

    def comment_service(self, host, service, comment = ''):
        ''' Comment a host or service problem '''

        url = self.api_base_url +\
            '&_acknowledge=Acknowledge&_ack_sticky=on&_ack_notify=on' + \
            '&host=' + host +\
            '&_ack_comment=' + comment +\
            '&_down_comment=' + comment +\
            '&_comment=' + comment +\
            '&_add_comment=Add+comment'

        if service:
            url += '&view_name=service' + \
                '&service=' + service
        else: # Downtime host
            url += '&view_name=hoststatus'


        t = Thread(target = self.background_request, args =(url, f'comment {host} - {service}' )) 
        t.start()

        self.mode = Mode.alertlist
        self.refresh_ui(norepeat=True)

    def downtime_service(self, host, service = None, time = None, comment=''):
        ''' Downtime service or host problem with optional comment and time '''

        url = self.api_base_url +\
            '&_acknowledge=Acknowledge&_ack_sticky=on&_ack_notify=on' + \
            '&host=' + host +\
            '&_ack_comment=' + comment +\
            '&_down_comment=' + comment +\
            '&_comment=' + comment

        if service:
            url += '&view_name=service' + \
                '&service=' + service
        else: # Downtime host
            url += '&view_name=hoststatus'

        if time:
            from_time = datetime.datetime.now()
            to_time = from_time + datetime.timedelta(seconds=time)

            url += '&_down_minutes=' + str(time//60) + \
                '&_down_from_now=From+now+for' + \
                '&_down_from_date=' + '{:%Y-%m-%d}'.format(from_time) + \
                '&_down_from_time=' + '{:%H:%M}'.format(from_time) + \
                '&_down_to_date=' + '{:%Y-%m-%d}'.format(to_time) + \
                '&_down_to_time=' + '{:%H:%M}'.format(to_time)

        t = Thread(target = self.background_request, args =(url, f'downtime {host} - {service}' )) 
        t.start()

        self.mode = Mode.alertlist
        self.refresh_ui(norepeat=True)

    def reschedule_check(self, host, service = None):
        ''' Reschedule check for service or host. '''
        # TODO: Often triggers:
        # > "ERROR - you did an active check on this service - please disable active checks"

        time = datetime.datetime.now()

        url = self.api_base_url +\
            '&host=' + host + \
            '&_resched_checks=Reschedule&_resched_spread=0'+\
            '&filled_in=confirm&actions=yes'+\
            '&_down_from_time=' + '{:%H:%M}'.format(time) +\
            '&_down_to_date=' + '{:%Y-%m-%d}'.format(time) +\
            '&_down_from_date=' + '{:%Y-%m-%d}'.format(time) +\
            '&_down_duration=02:00' +\
            '&_ack_expire_minutes=0' +\
            '&_ack_expire_hours=0' +\
            '&_ack_expire_days=0' +\
            '&_down_minutes=60' +\
            '&_ack_sticky=on'+\
            '&_cusnot_comment=TEST' +\
            '&_ack_notify=on' +\
            '&host=' + host

        if service:
            url += '&view_name=service' + \
                '&service=' + service

        else: # Ack host
            url += '&view_name=hoststatus'

        t = Thread(target = self.background_request, args =(url, f'reschedule {host} - {service}' )) 
        t.start()

        self.mode = Mode.alertlist
        self.refresh_ui(norepeat=True)

    def reinventorize_host(self, host):
        ''' Reinventorize a host, meaning fix all missing/vanished '''
        # discover_services at https://checkmk.com/cms_web_api_references.html

        url = self.checkmkhost + \
            'check_mk/webapi.py' + \
            '?action=discover_services' + \
            '&output_format=python&_username=' + \
            self.checkmkusername + \
            '&_secret=' + \
            self.checkmksecret

        postdata={
                "hostname":host,
                "mode":"fixall"
                }

        t = Thread(target = self.background_request, args =(url, f'Reinv. {host}', 'post', postdata )) 
        t.start()

        self.mode = Mode.alertlist
        self.refresh_ui(norepeat=True)

    def activate_wato_change(self, comment=''):
        ''' Activate a WATO change. Returns result string. '''
        # https://checkmk.com/cms_web_api_references.html#activate_changes

        r = requests.post(self.checkmkhost + \
            'check_mk/webapi.py' + \
            '?action=activate_changes' + \
            '&output_format=python&_username=' + \
            self.checkmkusername + \
            '&_secret=' + \
            self.checkmksecret,
            data={
                "mode": "dirty",
                "allow_foreign_changes": "0",
                "comment": comment
                }
        )

        return ''.join(ast.literal_eval(r.text)['result'])

    def fetch_comments(self, host, service):
        ''' Fetch all comments for a service '''

        r = requests.get(self.api_base_url +\
            '&view_name=comments_of_service' + \
            '&host=' + host + \
            '&service=' + service)

        self.status = f"{Chk.fetch_time()} Found {len(r.json())-1} comments for {host}-{service}."
        return (r.json()[1:])[::-1] # Skip header, sort by latest first

    def fetch_sites(self):
        ''' Fetch sites (this user has access to)'''
        # https://checkmk.com/cms_web_api_references.html

        r = requests.get(self.checkmkhost + \
            'check_mk/webapi.py' + \
            '?action=get_user_sites' + \
            '&output_format=python&_username=' + \
            self.checkmkusername + \
            '&_secret=' + \
            self.checkmksecret)

        return ast.literal_eval(r.text)['result']

    def command_changed(self, widget, text):
        ''' React to changes in the edit box in dialogs '''

        # In ack, comment, downtime, attempt to parse a time from comment
        if self.mode in [Mode.ack, Mode.comment, Mode.downtime]:
            default_caption = '> '
            word = widget.get_edit_text()

            if len(word) < 3 or ' ' not in word:
                widget.set_caption(default_caption)
                return

            time = Chk.parse_time(word.split()[0])
            if time == -1 or time < 60:
                widget.set_caption(default_caption)
            else:
                widget.set_caption(f"(Time: [{time}] seconds) {default_caption}")

        # In allhosts, update list with filter
        if self.mode == Mode.hostfilter:
            default_caption = '> '
            new = widget.get_edit_text()
            if new == self.hostfilter:
                return

            self.hostfilter = widget.get_edit_text()
            self.refresh_ui(norepeat=True)

    def background_request(self, url, description='', request_type='get', postdata=None):
        ''' Run a web request in background, and update status line.
            Assume any POST request needs a WATO activation request after.'''

        self.write_status_and_log(
            message=f"Running {description}...",
            message_short=f'Calling url in background, {url}')

        response = ''
        status_code = 0

        if request_type == 'get':
            r = requests.get(url)
            status_code = r.status_code
            response = r.text.replace(os.linesep, '')
        else:
            r = requests.post(url, data=postdata)
            status_code = r.status_code
            response = str(ast.literal_eval(r.text)['result'])[:60].replace(os.linesep, '')

            syslog.syslog(f"Activating WATO change {description}")
            response += self.activate_wato_change(comment=f"Activate WATO")

        self.write_status_and_log(
            message=f"{description}: {status_code} {response}")

    def write_status_and_log (self, message, message_short = ''):
        ''' Write a short message to status bar, and the full message to log.
            If a short version of message is inclued, it's used for the status bar.
        '''

        message = Chk.scrub_secret(message)
        message_short = Chk.scrub_secret(message_short)

        if len(message_short) == 0:
            message_short = message[:200]

        syslog.syslog(f'{message}')
        self.status = f'{Chk.fetch_time()} {message_short}'

    def fetch_events(self, time=600):
        ''' Fetch host- and service events from the last hour'''
        r = None
        url = self.api_base_url +\
                f'&view_name=events&logtime_from=1&logtime_from_range={time}'

        r = requests.get(url)

        # Remove first line (header) and reverse the list
        return r.json()[1::]

    def fetch_all_hosts(self, filterstring=''):
        ''' Fetch all hosts, optionally filtered. '''
        # Example returned:
        #[['host_state', 'host', 'host_icons', 'num_services_ok', 'num_services_warn', 
        #'num_services_unknown', 'num_services_crit', 'num_services_pending'],
        #['DOWN', 'centos7.lxd', 
        #'themes/facelift/images/icon_menu themes/facelift/images/icon_pnp ack comment',
        # '36', '5', '0', '3', '0'], ['UP', 'laptop', 
        # 'themes/facelift/images/icon_menu themes/facelift/images/icon_pnp',
        # '74', '6', '9', '18', '0'], ['UP', 'omd.lxd', 
        # 'themes/facelift/images/icon_menu themes/facelift/images/icon_pnp', 
        # '20', '0', '0', '0', '0'], ['DOWN', 'web.lxd', 
        # 'themes/facelift/images/icon_menu themes/facelift/images/icon_pnp',
        # '37', '6', '0', '8', '0']]

        r = None
        url = self.api_base_url +\
                '&view_name=allhosts'

        if filterstring:
            url += '&hostalias=' + filterstring

        try:
            r = requests.get(url)
            self.write_status_and_log("Fetched all hosts in %ss." % r.elapsed)
        except requests.exceptions.MissingSchema as e:
            print(f"Error fetching service problems. Wrong checkmk url? " \
                + f"Check url in config file {self.config_path}. Error: {e}")
            sys.exit(1)
        except requests.exceptions.ConnectionError:
            self.write_status_and_log(message=f'Temporary error connecting to {url}')
            return ''
        except simplejson.errors.JSONDecodeError:
            self.write_status_and_log(message=f'Temporary error connecting to {url} in fetch_all_hosts')
            return ''

        return r.json()[1:]


if __name__=="__main__":
    chk = Chk()
    sys.exit(chk.main())
