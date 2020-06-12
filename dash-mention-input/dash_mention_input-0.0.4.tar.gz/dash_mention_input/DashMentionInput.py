# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashMentionInput(Component):
    """A DashMentionInput component.
DashMentionInput is a text area component with @mention support.

Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks.
- value (string; default ''): The value displayed in the input.
- placeholder (string; optional): Initial hine (placeholder) to be shown in the area.
- mentions_config (list; optional): The list of mentions configurations.
- style (dict; default {
    control: {
        backgroundColor: '#fff',

        fontSize: 14,
        fontWeight: 'normal',
    },

    highlighter: {
        overflow: 'hidden',
    },

    input: {
        margin: 0,
    },

    '&singleLine': {
        control: {
            display: 'inline-block',

            width: 130,
        },

        highlighter: {
            padding: 1,
            border: '2px inset transparent',
        },

        input: {
            padding: 1,

            border: '2px inset',
        },
    },

    '&multiLine': {
        control: {
            fontFamily: 'monospace',
            border: '1px solid silver',
        },

        highlighter: {
            padding: 9,
        },

        input: {
            padding: 9,
            minHeight: 63,
            outline: 0,
            border: 0,
        },
    },

    suggestions: {
        list: {
            backgroundColor: 'white',
            border: '1px solid rgba(0,0,0,0.15)',
            fontSize: 14,
        },

        item: {
            padding: '5px 15px',
            borderBottom: '1px solid rgba(0,0,0,0.15)',

            '&focused': {
                backgroundColor: '#aaaaaa',
            },
        },
    },
})"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, value=Component.UNDEFINED, placeholder=Component.UNDEFINED, mentions_config=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'value', 'placeholder', 'mentions_config', 'style']
        self._type = 'DashMentionInput'
        self._namespace = 'dash_mention_input'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'value', 'placeholder', 'mentions_config', 'style']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DashMentionInput, self).__init__(**args)
