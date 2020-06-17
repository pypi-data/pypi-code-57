#!/usr/bin/env python3
from time import sleep
from behave import step
from dogtail.rawinput import typeText, pressKey, keyCombo, absoluteMotion, click
from qecore.utility import get_application, get_application_root
from qecore.get_node import GetNode, get_center
from qecore.step_matcher import use_step_matcher

__author__ = """
Filip Pokryvka <fpokryvk@redhat.com>,
Michal Odehnal <modehnal@redhat.com>
"""

use_step_matcher("qecore")  # to stop using "qecore" matcher use matcher "parse"

"""
This allows multiple decorator definitions on one line separated by ' | '
EXAMPLE:
This decorator:
    @step('Item "{name}" "{role_name}" | with description "{description}" | that is "{attr}"')

matches for example the following steps:
    * Item "foo" "push button"
    * Item "foo" "push button" with description "something useful"
    * Item "foo" "push button" with description "something useful" that is "visible"
    * Item "foo" "push button" that is "visible"

And also any permutation of decorator parts except the first part, so this is also valid step:
    * Item "foo" "push button" that is "visible" with description "something useful"

WARNING:
"qecore" matcher does not work well with unquoted decorator arguments, use "parse" instead
"""

SIZE_DEC = "".join([' | has size at least "{size_low}"',
                    ' | has size at most "{size_high}"'])
POS_DEC = "".join([' | that is at least "{position_low}" from topleft',
                   ' | that is at most "{position_high}" from topleft'])
SIZE_POS_DEC = SIZE_DEC + POS_DEC


@step('{m_btn} click "{name}" "{role_name}" | with description "{description}" | that is "{attr}" | in "{a11y_root_name}"' + SIZE_POS_DEC)
def mouse_click(context, retry=True, expect_positive=True, **kwargs):
    with GetNode(context, **kwargs, retry=retry, expect_positive=expect_positive) as (data, node):
        node.click(data.m_btn)


@step('Mouse over "{name}" "{role_name}" | with description "{description}" | that is "{attr}" | in "{a11y_root_name}"' + SIZE_POS_DEC)
def mouse_over(context, retry=True, expect_positive=True, **kwargs):
    with GetNode(context, **kwargs, retry=retry, expect_positive=expect_positive) as (_, node):
        absoluteMotion(*(get_center(node)))


@step('Make an action "{action}" for "{name}" "{role_name}" | with description "{description}" | that is "{attr}" | in "{a11y_root_name}"' + SIZE_POS_DEC)
def make_action(context, action, retry=True, expect_positive=True, **kwargs):
    with GetNode(context, **kwargs, retry=retry, expect_positive=expect_positive) as (_, node):
        node.doActionNamed(action)


@step('Item "{name}" "{role_name}" | found | with description "{description}" | is "{attr}" | in "{a11y_root_name}"' + SIZE_POS_DEC)
def node_attribute(context, retry=True, expect_positive=True, **kwargs):
    with GetNode(context, **kwargs, retry=retry, expect_positive=expect_positive) as (_, node):
        assert node is not None, "Node was not found, it should be!"


@step('Item "{name}" "{role_name}" | was not found | with description "{description}" | is not "{attr}" | in "{a11y_root_name}"' + SIZE_POS_DEC)
def node_not_attribute(context, retry=True, expect_positive=False, **kwargs):
    with GetNode(context, **kwargs, retry=retry, expect_positive=expect_positive) as (_, node):
        assert node is None, "Node was found, it should not be!"


@step('Item "{name}" "{role_name}" | with description "{description}" | has text "{text}" | in "{a11y_root_name}"' + SIZE_POS_DEC)
def node_with_text(context, text, retry=True, expect_positive=True, **kwargs):
    with GetNode(context, **kwargs, retry=retry, expect_positive=expect_positive) as (_, node):
        assert text in node.text, "".join((
            f"Found node should have text: {text}\n",
            f"Instead the node has text: {node.text}"
        ))


@step('Item "{name}" "{role_name}" | with description "{descr}" | does not have text "{text}" | in "{a11y_root_name}"' + SIZE_POS_DEC)
def node_without_text(context, text, retry=True, expect_positive=True, **kwargs):
    with GetNode(context, **kwargs, retry=retry, expect_positive=expect_positive) as (_, node):
        assert not text in node.text, "".join((
            f"Found node should have text: {text}\n",
            f"Node was found with text: {node.text}"
        ))


@step('Item "{name}" "{role_name}" | does not have description "{description}" | that is "{attr}" | in "{a11y_root_name}"' + SIZE_POS_DEC)
def node_without_description(context, description, retry=True, expect_positive=True, **kwargs):
    with GetNode(context, **kwargs, retry=retry, expect_positive=expect_positive) as (_, node):
        assert not description in node.description, "".join((
            f"Found node should not have description: {description}\n",
            f"Instead the node has description: {node.description}"
        ))


@step('Wait until "{name}" "{role_name}" | with description "{descr}" | is "{attr}" | in "{a11y_root_name}"' + SIZE_POS_DEC)
def wait_until_attr(context, retry=True, expect_positive=True, **kwargs):
    with GetNode(context, **kwargs, retry=retry, expect_positive=expect_positive) as (_, node):
        for _ in range(30):
            if not node.sensitive:
                sleep(0.2)
            else:
                return


@step('Wait until "{name}" "{role_name}" | appears | with description "{description}" | in "{root}"')
def wait_until_in_root(context, name=None, role_name=None, description=None, m_btn=None, attr=None, root=None, retry=True, expect_positive=True):
    try:
        application_a11y_instance = get_application(context, root).instance # from sandbox/application
    except AssertionError:
        application_a11y_instance = get_application_root(context, root) # from a11y tree

    for _ in range(30):
        if application_a11y_instance.findChildren(lambda x: \
            ((name is None) or name in repr(x.name)) and \
            ((role_name is None) or role_name == x.roleName) and \
            ((description is None) or description in x.description)) == []:
            sleep(0.2)
        else:
            return


@step('Start another instance of "{application}" | via "{start_via}" | via command "{command}" | via command | in "{session}"')
def start_another_instance_of_application(context, application=None, start_via="command", command=None, session=None, kill=False):
    start_application(context, application, start_via, command, session, kill)


@step('Start {application} via {start_via}') # behave-common-steps decorator
@step('Start "{application}" via command in {session}') # behave-common-steps decorator
@step('Start application "{application}" | via "{start_via}" | via command "{command}" | via command | in "{session}"')
def start_application(context, application=None, start_via="command", command=None, session=None, kill=True):
    application = get_application(context, application)
    if start_via == "menu":
        try:
            application.start_via_menu(kill=kill)
        except Exception:
            application.start_via_menu(kill=kill)
    elif start_via == "command":
        try:
            application.start_via_command(command=command, in_session=session, kill=kill)
        except RuntimeError as error:
            assert False, error
        except Exception:
            application.start_via_command(command=command, in_session=session, kill=kill)
    else:
        raise AssertionError("Only defined options are 'command' and 'menu'.")


use_step_matcher("parse")  # stop using qecore matcher


@step('Close app via gnome panel') # behave-common-steps decorator
@step('Close application "{application}" via "{close_via}"')
def application_in_not_running(context, application=None, close_via="gnome panel"):
    application = get_application(context, application)
    if close_via == "gnome panel":
        context.execute_steps(f'* Left click "{application.name}" "menu" in "gnome-shell"')
        sleep(0.5)
        context.execute_steps('* Left click "Quit" "label" in "gnome-shell"')

    elif close_via == "application menu":
        if context.sandbox.distribution == "Fedora":
            application.instance.children[0][0].click(3)
            sleep(0.5)
            context.execute_steps(f'* Left click "Close" "label" in "gnome-shell"')

        else: # context.sandbox.distribution == "Red Hat Enterprise Linux":
            context.execute_steps(f'* Left click "File" "menu" in "{application.component}"')
            sleep(0.5)
            application.instance.findChild(lambda x: ("Close" in x.name or "Quit" in x.name)\
                and x.roleName == "menu item" and x.sensitive).click()

    elif close_via == "shortcut":
        application.close_via_shortcut()

    elif close_via == "kill command":
        application.kill_application()

    else:
        raise AssertionError("".join((
            "Only defined options are:\n",
            "'gnome panel', 'application menu', 'shortcut' and 'kill command'."
        )))


@step('{application} shouldn\'t be running anymore') # behave-common-steps decorator
@step('Application "{application}" is no longer running')
def application_is_not_running(context, application):
    application = get_application(context, application)
    if application.is_running():
        application.wait_before_app_closes(15)


@step('{application} should start') # behave-common-steps decorator
@step('Application "{application}" is running')
def application_is_running(context, application):
    application = get_application(context, application)
    application.already_running()
    if not application.is_running():
        application.wait_before_app_starts(15)


@step('Click "{target_name}" in GApplication menu') # behave-common-steps decorator
def click_gapp_menu(context, target_name):
    assert context.sandbox.default_application is not None, \
        "You need to define a default application if you are using steps without root."
    context.execute_steps(f'* Left click "{context.sandbox.default_application.name}" "menu" in "gnome-shell"')
    sleep(0.5)
    context.execute_steps(f'* Left click "{target_name}" "label" in "gnome-shell"')


@step('Type text: "{text}"')
def type_text(context, text):
    typeText(text)


@step('Press key: "{key_name}"')
def press_key(context, key_name):
    pressKey(key_name)


@step('Press "{combo_name}"') # behave-common-steps decorator
@step('Key combo: "{combo_name}"')
def key_combo(context, combo_name):
    keyCombo(combo_name)


@step('Wait {number} second before action')
@step('Wait {number} seconds before action')
def wait_up(context, number):
    sleep(int(number))


@step('Move mouse to: x: "{position_x}", y: "{position_y}"')
def absolutie_motion(context, position_x, position_y):
    absoluteMotion(int(position_x), int(position_y))


@step('{button} click on: x: "{position_x}", y: "{position_y}"')
def click_on_position(context, button, position_x, position_y):
    buttons = dict(Left=1, Middle=2, Right=3)
    click(int(position_x), int(position_y), buttons[button])
