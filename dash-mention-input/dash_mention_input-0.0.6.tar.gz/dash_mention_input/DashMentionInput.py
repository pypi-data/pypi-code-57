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
- isReadOnly (boolean; default False): Mark textarea as readonly for displaying data purpose
- style (dict; default defaultStyle): CSS Style to be applied to input and suggestion controls
- readOnlyStyle (dict; default defaultReadonlyStyle): CSS Style to be applied to input and suggestion controls. READONLY mode"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, value=Component.UNDEFINED, placeholder=Component.UNDEFINED, mentions_config=Component.UNDEFINED, isReadOnly=Component.UNDEFINED, style=Component.UNDEFINED, readOnlyStyle=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'value', 'placeholder', 'mentions_config', 'isReadOnly', 'style', 'readOnlyStyle']
        self._type = 'DashMentionInput'
        self._namespace = 'dash_mention_input'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'value', 'placeholder', 'mentions_config', 'isReadOnly', 'style', 'readOnlyStyle']
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
