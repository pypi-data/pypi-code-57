# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Masking(Component):
    """A Masking component.


Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks.
- masking_notevalues (list; optional): A label that will be printed when this component is rendered.
- masking_notesizes (list; optional)
- masking_colors (list; optional)
- target_notevalues (list; optional)
- target_notesizes (list; optional)
- target_colors (list; optional)"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, masking_notevalues=Component.UNDEFINED, masking_notesizes=Component.UNDEFINED, masking_colors=Component.UNDEFINED, target_notevalues=Component.UNDEFINED, target_notesizes=Component.UNDEFINED, target_colors=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'masking_notevalues', 'masking_notesizes', 'masking_colors', 'target_notevalues', 'target_notesizes', 'target_colors']
        self._type = 'Masking'
        self._namespace = 'score_component'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'masking_notevalues', 'masking_notesizes', 'masking_colors', 'target_notevalues', 'target_notesizes', 'target_colors']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Masking, self).__init__(**args)
