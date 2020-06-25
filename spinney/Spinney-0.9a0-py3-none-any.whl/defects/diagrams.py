# -*- coding: utf-8 -*-
"""
Implements the creation of the diagrams reporting the
formation energy of point defects as a function
of the electron chemical potential.
"""
from collections import defaultdict
import copy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

cmap = plt.cm.jet
np.random.seed(10)
COLOR_LIST = [cmap(x) for x in np.linspace(0, 1, 20)]
np.random.shuffle(COLOR_LIST)

STYLES_LIST = ['-', '--', '-.', ':']
STYLES_LIST = np.repeat(STYLES_LIST, len(COLOR_LIST))

def set_latex_globally():
    """ Call this function to use latex synthax globally in matplotlip.
    Note that now every string used through matplotlib has to respect latex
    synthax.
    """
    from matplotlib import rcParams
    rcParams['text.usetex'] = True
    rcParams['text.latex.preamble'] = [r'\usepackage{amssymb}']

class Line:
    """ A simple class describing the equation of a line:

    .. math::

        y = m(x-x_0) + q

    where q is the intercept with the y = x0 axis
    """
    def __init__(self, m, q, x0):
        self.m = m
        self.q = q
        self.x0 = x0

    @property
    def equation(self):
        return lambda x: self.m*(x-self.x0) + self.q

class PointDefectLines:
    """
    This class holds the information to represent a line on the formation
    energy diagrams of point defects.

    Parameters
    ----------
    defect_name : string
        the name of the defect

    e_form_min_dict : dict
        {charge_state1 : formation_energy1_at_VBM, ...}

        charge_state1 is an integer describing the defect charge
        state;
        formation_energy1_at_VBM is a floating-point number
        indicating the formation energy of that defect for an
        electron chemical potential equal to the valence band
        maximum (VBM) of the host material.
        This VBM value must be stored in :attr:`gap_range`

    gap_range : array of 2 elements
        (valence_band_maximum, conduction_band_minimum)
        representing the allowed range for the electron
        chemical potential.
        Note that the VBM to which *e_form_dict* refers to is
        gap_range[0]

    extended_gap_range : array of 2 elements
        an extended range for the band gap.
        This value can be used for example when *gap_range* is the
        underestimated DFT band gap and we want to evaluate the
        defect formation energy lines on a different gap.

    Attributes
    ----------
    lines : dict
        {charge_state1 : line1, ...}
        for each defect charge state of the instance.
        line1 is a Line instance.

    intersections :  dict of dicts
        For each charge state of the defect, one has the dictionary
        containing the coordinates of the intersection point between
        the line corresponding to that charge state and the lines of all
        other charge states and band edges as well.

    lines_limits :  defaultdict
        {defect_charge_state1 : [y_0, y_1], ...}
        y_0 and y_1 are two numpy arrays with two elements each:

            the values of the electron chemical potential
            and those of the defect formation energy corresponding to
            the two points between which the formation
            energy of defect_charge_state1 is the lowest one among all
            other defect charge states.

    transition_levels : dict
        Returns the transition levels among the possible
        charge states as a dictionary:

        .. code-block::

            {charge_state1 : {charge_state2 : transition_level,
                              charge_state3 : transition_level, ...}, ...}

        transition_level is the electrom chemical potential value at the
        transition level between charge states.
        For a complete list of intersection between all defect lines,
        use :attr:`self.intersections`
    """
    def __init__(self, defect_name, e_form_min_dict, gap_range,
                 extended_gap_range=None):
        if not isinstance(e_form_min_dict, dict):
            raise TypeError('The formation energies values have to be '
                            'given as a dictionary!')
        for key in e_form_min_dict.keys():
            if not isinstance(key, int):
                raise TypeError('The defect formal charges must be integers '
                                'not {:s}'.format(str(type(key))))
        self.defect_name = defect_name
        self.formation_energies_map = copy.copy(e_form_min_dict)
        self.gap_range = tuple(gap_range)
        if extended_gap_range is not None:
            self.extended_range = tuple(extended_gap_range)
        else:
            self.extended_range = None
        if self.extended_range is None:
            vbm = self.gap_range[0]
            cbm = self.gap_range[1]
        else:
            if self.extended_range[0] <= self.gap_range[0]:
                vbm = self.extended_range[0]
            else:
                vbm = self.gap_range[0]
            if self.extended_range[1] >= self.gap_range[1]:
                cbm = self.extended_range[1]
            else:
                cbm = self.gap_range[1]
        self.vbm = vbm
        self.cbm = cbm

    def _prepare_lines(self):
        """The attribute *self._lines* is a dictionary
        {charge_state1 : line1, ...}
        for each defect charge state of the instance.
        line1 is a Line instance.
        """
        lines = {}
        for key, value in self.formation_energies_map.items():
            lines[key] = self._make_line(key, value, self.gap_range[0])
        self._lines = lines

    @property
    def lines(self):
        if not hasattr(self, '_lines'):
            self._prepare_lines()
        return copy.deepcopy(self._lines)

    @property
    def intersections(self):
        """ Returns a dictionary of dictionaries.
        For each charge state of the defect, one has the dictionary
        containing the coordinates of the intersection point between the line
        corresponding to that charge state and all other charge states and
        band edges as well.
        """
        if not hasattr(self, '_intersections'):
            self._calculate_all_intersections()
        return copy.deepcopy(self._intersections)

    @property
    def lines_limits(self):
        """
         The attribute *_lines_limits* is a defaultdict:

            {defect_charge_state1 : [y_0, y_1], ...}
            y_0 and y_1 are two numpy arrays with two elements each:
            the values of the electron chemical potential
            and those of the defect formation energy corresponding to
            the two points between which the formation
            energy of *defect_charge_state1* is the lowest one among all
            other defect charge states.

            This is a subset of *self._intersections*
        """
        if not hasattr(self, '_lines_limits'):
            self._find_limits()
        return copy.deepcopy(self._lines_limits)

    def _prepare_transition_levels(self):
        t_levels = defaultdict(dict)
        for chg1, values in self.intersections.items():
            for chg2, value in values.items():
                if isinstance(chg2, int):
                    if len(self.lines_limits[chg1]) > 0:
                        point1, point2 = self.lines_limits[chg1]
                        if (np.allclose(value, point1, 1e-9) or
                                np.allclose(value, point2, 1e-9)):
                            t_levels[chg1][chg2] = value[0]

        self._transition_levels = t_levels

    @property
    def transition_levels(self):
        """ Returns the transition levels among the possible
        charge states as a dictionary:

            {charge_state1 : {charge_state2 : transition_level,
                              charge_state3 : transition_level, ...}, ...}

        transition_level is the electrom chemical potential value at the
        transition level between charge states.
        For a complete list of intersection between all defect lines,
        use :attr:`self.intersections`
        """
        if not hasattr(self, '_transition_levels'):
            self._prepare_transition_levels()
        return copy.deepcopy(self._transition_levels)

    def _make_line(self, charge_state, formation_energy_at_vbm, x0):
        """ Creates a line as a function of the electron chemical potential.

        Parameters
        ----------
        charge_state : int
            the line slope

        formation_energy_at_vbm : float
            the line intercept with the energy-axis

        x0 : float
            the value of the independent variable such that:
            line(x0) = formation_energy_at_vbm

        Returns
        -------
        line :  A :class:`Line` object
        """
        return Line(charge_state, formation_energy_at_vbm, x0)

    def _calculate_lines_crossing(self, line1, line2):
        """ Finds the intercept between two lines.

        line1 and line2 are two instances of :class:`Line`
        """
        # coefficients of the linear system
        coeff_matrix = np.array([[line1.m, -1],
                                 [line2.m, -1]])
        #constant terms of the linear system
        b = np.array([line1.m*line1.x0 - line1.q,
                      line2.m*line2.x0 - line2.q])

        return np.linalg.solve(coeff_matrix, b)

    def _calculate_all_intersections(self):
        """ For each pair of charge states, calculates the intercepts between
        the two lines representing the defects in those charge states.

        Returns
        -------
        crossings : dict
            {charge_state1 : {charge_state2:crossing1-2,
                              charge_state3:crossing1-3, ...},
            charge_state2 : {charge_state1:crossing2-1}, ...},
            ...}

        Note
        ----
        For N different charge states, there will be N!/((N-2)! 2!) crossings.
        Here, we however report all the N!/(N-2)! of them.
        """
        intersections = {}
        for i, line_i in self.lines.items():
            intersections[line_i.m] = {}
            for j, line_j in self.lines.items():
                if i != j:
                    intersections[line_i.m][line_j.m] = (
                        self._calculate_lines_crossing(line_i, line_j))

        # add the intersections with self.gap_range[0] and self.gap_range[1]
        # vertical lines, or with the extended range
        for key, line in self.lines.items():
            intersections[key]['VBM'] = np.array([self.vbm,
                                                  line.equation(self.vbm)])
            intersections[key]['CBm'] = np.array([self.cbm,
                                                  line.equation(self.cbm)])
        self._intersections = intersections

    def _find_limits(self):
        """ For each defect charge state, finds the limit points of the line
        segment where the defect has the lowest formation energy among
        all charge states
        """
        crossings = self.intersections
        limits = defaultdict(list)

        possible_charge_states = set(crossings.keys())

        # look for the 2 intersection points with the lowest energy
        for charge_state1, values in crossings.items():
            avail_states = possible_charge_states.difference([charge_state1])
            for charge_state2, point in values.items():
                point_mu, point_energy = point
                # skip values outside *self.gap_range*
                if (point_mu < self.vbm or
                        point_mu > self.cbm):
                    continue
                # calculate the energies of all possible charge states at
                # the electron chemical potential *point_mu*
                energies = []
                if len(avail_states) > 0:
                    for state in avail_states:
                        energies.append(self.lines[state].equation(point_mu))
                else: # in case no charge states are available, we just
                      # use the intersections with the band edges
                    energies += [crossings[charge_state1]['VBM'][1],
                                 crossings[charge_state1]['CBm'][1]]
                if (point_energy - np.min(energies)) <= 1e-6:
                    limits[charge_state1].append(point)
                    crossings[charge_state1][charge_state2] = [point_mu,
                                                               np.inf]

        self._lines_limits = limits

    def plot_lines(self, ax='auto', **kwargs):
        """ Given an existing axes, plots the defect formation energy lines

        Parameters
        ----------
        ax : :class:`matplotlib.axes.Axes` instance
            the axes where the lines should be plotted

        kwargs : dict
            additional key:value pairs taken by matplotlib.pyplot.plot
        """
        if ax == 'auto':
            ax = plt.gca()

        label = kwargs.pop('label', None)
        unique_label = kwargs.pop('unique_label', True)

        i = 0
        for charge_state, points in self.lines_limits.items():
            mu_list, energy_list = list(zip(*points))
            if label is None:
                label = self.defect_name + ' ' + str(charge_state)

            if unique_label:
                if i == 0:
                    label = label
                else:
                    label = ''
                i += 1
            ax.plot(mu_list, energy_list, label=label, **kwargs)

class Diagram:
    """ A diagram represent the formation energies of various point defects,
    in various charge states, as a function of the electron chemical potential,
    whose value ranges from the valence band maximum to the conduction band
    minimum of the host material.

    This class is basically a composition of PointDefectLines instances
    with some tools for plotting the final diagram.

    Parameters
    ----------
    defects_dictionary : dict of dicts
        for each point defect named "defect", the value is a dictionary
        in the form: {charge_state1 : formation_energy_at_VBM, ...}

        Example:

            For vacancy and N center in diamond:

            >>> defects_dictionary = {
                    '$V$' : {-1 : value1, 0 : value2, 1 : value3},
                    r'$N_C$' : {0 : value4}
                    }

            The value of VBM must be consistent with gap_range[0]

    gap_range : array of 2 elements
        the band gap range. The first value must be consistent with the
        valence band maximum (VBM) used to calculate the defect formation
        energy in :data:`defect_dictionary`

    extended_gap_range : array of 2 elements
        an extended range for the band gap.
        This value can be used for example when :data:`gap_range` is the
        underestimated DFT band gap and we want to plot the defect
        formation energy lines on a wider gap.
        In this case, the difference between the extended region and the
        original region will be plotted in gray.

    electrom_mu : float
        pinned value of the electron chemical potential wrt the valence
        band maximum (:data:`gap_range[0]`)

    Attributes
    ----------
    labels : dict
        {defect_name : defect_label, ...}
        where defect_name is one of the top keys if :data:`defects_dictionary`

    defects : dict
        {defect_name : Line instance representing that defect type, ...}
    """
    def __init__(self, defects_dictionary, gap_range, extended_gap_range=None,
                 electron_mu=None):
        self.gap_range = tuple(gap_range)
        if extended_gap_range is not None:
            self.extended_gap_range = tuple(extended_gap_range)
        else:
            self.extended_gap_range = None
        if self.extended_gap_range is None:
            vbm = self.gap_range[0]
            cbm = self.gap_range[1]
        else:
            if self.extended_gap_range[0] <= self.gap_range[0]:
                vbm = self.extended_gap_range[0]
            else:
                vbm = self.gap_range[0]
            if self.extended_gap_range[1] >= self.gap_range[1]:
                cbm = self.extended_gap_range[1]
            else:
                cbm = self.gap_range[1]

        self.vbm = vbm
        self.cbm = cbm

        self.electron_mu = electron_mu

        self._defects = {}
        self._labels = {}
        for key, values in defects_dictionary.items():
            self._defects[key] = PointDefectLines(key, values,
                                                  self.gap_range,
                                                  self.extended_gap_range)
            self._labels[key] = key

    @property
    def labels(self):
        return copy.copy(self._labels)
    @labels.setter
    def labels(self, values):
        """ Set the labels that will be used for plotting in case the defect
        names are not suitable.

        Parameters
        ----------
        values : dict
            a dictionary in the form {defect_name : defct_label}
            where defect_name has to be the same string used as a key of
            the defects_dictionary parameter in :meth:`__init__`
        """
        for key, value in values.items():
            self._labels[key] = value

    @property
    def defects(self):
        return copy.deepcopy(self._defects)

    def _find_transition_levels(self):
        indices = []
        levels_values = []
        for key, value in self.defects.items():
            levels = []
            for chg1, dict_chg in value.transition_levels.items():
                for chg2, tlevel in dict_chg.items():
                    lvalue = sorted((chg1, chg2))
                    lvalue = [str(x) for x in lvalue]
                    if not lvalue in levels:
                        levels.append(lvalue)
                        indices.append((key, '/'.join(lvalue)))
                        levels_values.append(tlevel)
        # build series and sort values
        index = pd.MultiIndex.from_tuples(indices, names=['#Defect type', "q/q'"])
        series = pd.Series(levels_values, index=index)
        series = series.reset_index(name='transition level')
        series.sort_values(by=['#Defect type', 'transition level'], inplace=True)
        series.set_index(['#Defect type', "q/q'"], inplace=True)
        series = pd.Series(series['transition level'].values.ravel(), index=series.index)
        series.name = 'transition level'
        self._transition_levels_series = series

    @property
    def transition_levels(self):
        if hasattr(self, '_transition_levels_series'):
            return self._transition_levels_series
        self._find_transition_levels()
        return self._transition_levels_series

    def write_transition_levels(self, file_name):
        """ Writes the charge transition levels of the system
        on a txt file.

        Parameters
        ----------
        file_name : string
            the name of the file where the transition levels
            will be written
        """
        with open(file_name, 'w') as f:
            series = self.transition_levels.to_string()
            f.write(series)

    def plot(self, **kwargs):
        """ Plot the diagram.

        Parameters
        ----------
        kwargs : dict
            optional key:values pair for plotting the diagram
        """
        figsize = kwargs.pop('figsize', (8, 12))
        try:
            colors_dict = kwargs.pop('colors_dict')
        except KeyError:
            colors_dict = {}
            for i, defect_name in enumerate(self.defects):
                colors_dict[defect_name] = COLOR_LIST[i]
        try:
            styles_dict = kwargs.pop('styles_dict')
        except KeyError:
            styles_dict = {}
            for i, defect_name in enumerate(self.defects):
                styles_dict[defect_name] = STYLES_LIST[i]
        linewidth = kwargs.pop('linewidth', 2)
        x_label = kwargs.pop('x_label', r'$\mu_e$ (eV)')
        y_label = kwargs.pop('y_label', r'$\Delta E_f$ (eV)')
        title = kwargs.pop('title', 'Diagram')
        save_title = kwargs.pop('save_title', title)
        title_size = kwargs.pop('title_size', 24)
        show_legend = kwargs.pop('legend', False)
        font_size = kwargs.pop('font_size', 18)
        save_flag = kwargs.pop('save_flag', False)
        y_limits = kwargs.pop('y_limits', None)
        legend_ncol = kwargs.pop('legend_ncol', 1)

        fig = plt.figure(figsize=figsize)
        fig.suptitle(title, fontsize=title_size)
        ax = plt.gca()

        plt.xticks(fontsize=font_size)
        plt.yticks(fontsize=font_size)

        x = np.linspace(self.vbm, self.cbm)
        ax.set_xlim(self.vbm, self.cbm)
        if y_limits:
            ax.set_ylim(y_limits[0], y_limits[1])
        ax.set_xlabel(x_label, fontsize=font_size)
        ax.set_ylabel(y_label, fontsize=font_size)

        if self.extended_gap_range is not None:
            if self.gap_range != self.extended_gap_range:
                if self.extended_gap_range[0] <= self.gap_range[0]:
                    ax.axvspan(self.extended_gap_range[0], self.gap_range[0],
                               alpha=0.4, color='gray')
                else:
                    ax.axvline(x=self.extended_gap_range[0], linestyle='-',
                               color='gray', alpha=0.4)
                if self.extended_gap_range[1] >= self.gap_range[1]:
                    ax.axvspan(self.gap_range[1], self.extended_gap_range[1],
                               alpha=0.4, color='gray')
                else:
                    ax.axvline(x=self.extended_gap_range[1], linestyle='-',
                               color='gray', alpha=0.4)

        ax.plot(x, np.zeros(len(x)), linestyle='--', color='black')

        for defect_name in self.defects.keys():
            defect = self.defects[defect_name]
            label = self.labels[defect_name]
            defect.plot_lines(ax=ax, color=colors_dict[defect_name],
                              linestyle=styles_dict[defect_name],
                              linewidth=linewidth, label=label,
                              unique_label=True)

        if self.electron_mu:
            y_lim_ = ax.get_ylim()
            pa = y_lim_[1]
            pp = y_lim_[0]
            ax.text(self.electron_mu, pp + 0.01*(pa-pp), r'$E_F$',
                    fontsize=font_size)
            ax.axvline(x=self.electron_mu, linestyle='--', color='black',
                       alpha=0.5)

        if show_legend:
            ax.legend(prop={'size' : font_size-6}, ncol=legend_ncol)

        if save_flag:
            fig.savefig(save_title + '.pdf',
                        bbox_inches='tight', dpi=300)
        fig.clf()

def extract_formation_energies_from_file(file_name):
    ''' Read a file with the format:

    ::

        # arbitrary number of comment lines
        defect_name    defect_charge_state   defect_formation_energy

    Parameters
    ----------
    file_name : string
        the file with the data
    
    Returns
    -------
    diagram_dict : defaultdict(dict)
        dictionary containing the information necessary to initialize an
        :class:`~spinney.defects.diagrams.Diagram` instance.
    '''
    diagram_dict = defaultdict(dict)
    with open(file_name, 'r') as f:
        for line in f:
            if not (line.startswith('#')):
                data = line.strip().split()
                defect = data[0]
                charge = int(data[1])
                form_energy = float(data[-1])
                diagram_dict[defect][charge] = form_energy
    return diagram_dict
