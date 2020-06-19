# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Range - working Copy without colors(Component):
    """A Range - working Copy without colors component.


Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks.
- width (number; optional): A label that will be printed when this component is rendered.
- height (number; optional)
- notes (list; optional)"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, width=Component.UNDEFINED, height=Component.UNDEFINED, notes=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'width', 'height', 'notes']
        self._type = 'Range - working Copy without colors'
        self._namespace = 'score_component'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'width', 'height', 'notes']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Range - working Copy without colors, self).__init__(**args)
