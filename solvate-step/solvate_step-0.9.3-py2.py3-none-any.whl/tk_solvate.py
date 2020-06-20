# -*- coding: utf-8 -*-

"""The graphical part of a Solvate step"""

import logging
import seamm
import seamm_widgets as sw
import Pmw
import tkinter as tk
import tkinter.ttk as ttk

logger = logging.getLogger(__name__)


class TkSolvate(seamm.TkNode):
    """Graphical interface for solvating the system
    """

    def __init__(
        self,
        tk_flowchart=None,
        node=None,
        canvas=None,
        x=None,
        y=None,
        w=200,
        h=50
    ):
        """Initialize a node

        Parameters
        ----------
        """

        self.dialog = None

        super().__init__(
            tk_flowchart=tk_flowchart,
            node=node,
            canvas=canvas,
            x=x,
            y=y,
            w=w,
            h=h
        )

    def create_dialog(self):
        """Create the dialog!"""
        self.dialog = Pmw.Dialog(
            self.toplevel,
            buttons=('OK', 'Help', 'Cancel'),
            master=self.toplevel,
            title='Edit Solvate step',
            command=self.handle_dialog
        )
        self.dialog.withdraw()

        frame = ttk.Frame(self.dialog.interior())
        frame.pack(expand=tk.YES, fill=tk.BOTH)
        self['frame'] = frame

        # Create all the widgets
        P = self.node.parameters
        for key in P:
            self[key] = P[key].widget(frame)

        self['submethod'].combobox.configure(width=50)

        self['solvent'].combobox.bind(
            "<<ComboboxSelected>>", self.reset_dialog
        )
        self['solvent'].combobox.bind("<Return>", self.reset_dialog)
        self['solvent'].combobox.bind("<FocusOut>", self.reset_dialog)
        self['method'].combobox.bind("<<ComboboxSelected>>", self.reset_dialog)
        self['method'].combobox.bind("<Return>", self.reset_dialog)
        self['method'].combobox.bind("<FocusOut>", self.reset_dialog)
        self['submethod'].combobox.bind(
            "<<ComboboxSelected>>", self.reset_dialog
        )
        self['submethod'].combobox.bind("<Return>", self.reset_dialog)
        self['submethod'].combobox.bind("<FocusOut>", self.reset_dialog)

        self.reset_dialog()

    def reset_dialog(self, widget=None):
        solvent = self['solvent'].get()
        method = self['method'].get()
        submethod = self['submethod'].get()

        logger.debug('reset_dialog: {}'.format(solvent))

        frame = self['frame']
        for slave in frame.grid_slaves():
            slave.grid_forget()

        row = 0
        self['solvent'].grid(row=row, column=0, columnspan=2, sticky=tk.W)
        row += 1

        if solvent == 'water' or solvent[0] == '$':
            self['water_model'].grid(row=row, column=1, sticky=tk.W)
            row += 1

        self['method'].grid(row=row, column=0, columnspan=2, sticky=tk.EW)
        if method == "within a sphere of solvent":
            raise NotImplementedError(
                'Solvating with a sphere not implemented yet!'
            )
        else:
            self['submethod'].grid(row=row, column=3, sticky=tk.W)
            if submethod == (
                "fixing the volume and adding a given number of molecules"
            ):
                row += 1
                self['number of molecules'].grid(
                    row=row, column=1, sticky=tk.EW
                )
            elif submethod == "fixing the volume and filling to a density":
                row += 1
                self['density'].grid(
                    row=row, column=1, columnspan=2, sticky=tk.EW
                )
            elif submethod == (
                "with the density and number of molecules of solvent"
            ):
                row += 1
                self['density'].grid(
                    row=row, column=1, columnspan=3, sticky=tk.W
                )
                row += 1
                self['number of molecules'].grid(
                    row=row, column=1, columnspan=3, sticky=tk.W
                )
                sw.align_labels([self['density'], self['number of molecules']])
            elif submethod == (
                "with the density and approximate number of atoms of "
                "solvent"
            ):
                row += 1
                self['density'].grid(row=row, column=1, sticky=tk.EW)
                row += 1
                self['approximate number of atoms'].grid(
                    row=row, column=1, sticky=tk.EW
                )
                sw.align_labels(
                    [self['density'], self['approximate number of atoms']]
                )
            row += 1
        frame.columnconfigure(0, minsize=60)

    def right_click(self, event):
        """Probably need to add our dialog...
        """

        super().right_click(event)
        self.popup_menu.add_command(label="Edit..", command=self.edit)

        self.popup_menu.tk_popup(event.x_root, event.y_root, 0)

    def edit(self):
        """Present a dialog for editing the Solvate input
        """
        if self.dialog is None:
            self.create_dialog()

        result = self.dialog.activate(geometry='centerscreenfirst')

        if result is not None:
            if result == "OK":
                # Shortcut for parameters
                P = self.node.parameters

                for key in P:
                    P[key].set_from_widget()
            else:
                raise RuntimeError(
                    "Don't recognize dialog result '{}'".format(result)
                )

    def handle_dialog(self, result):
        if result is None or result == 'Cancel':
            self.dialog.deactivate(None)
            return

        if result == 'Help':
            # display help!!!
            return

        self.dialog.deactivate(result)

    def handle_help(self):
        print('Help')
