from travertino.size import at_least

from toga_winforms.libs import WinForms

from .base import Widget


class Table(Widget):
    def create(self):
        self._container = self
        self.native = WinForms.ListView()
        self.native.View = WinForms.View.Details
        self._cache = []
        self._first_item = 0

        dataColumn = []
        for i, (heading, accessor) in enumerate(zip(
                    self.interface.headings,
                    self.interface._accessors
                )):
            dataColumn.append(self._create_column(heading, accessor))

        self.native.FullRowSelect = True
        self.native.MultiSelect = self.interface.multiple_select
        self.native.DoubleBuffered = True
        self.native.VirtualMode = True
        self.native.Columns.AddRange(dataColumn)

        self.native.ItemSelectionChanged += self._native_item_selection_changed
        self.native.RetrieveVirtualItem += self._native_retrieve_virtual_item
        self.native.CacheVirtualItems += self._native_cache_virtual_items
        self.native.VirtualItemsSelectionRangeChanged += self._native_virtual_item_selection_range_changed

    def _native_virtual_item_selection_range_changed(self, sender, e):
        # update selection interface property
        self.interface._selection = self._selected_rows()

        # `Shift` key or Range selection handler
        if e.IsSelected and self.interface.multiple_select and self.interface.on_select:
            # call on select with the last row of the multi selection
            selected = self.interface.data[e.EndIndex]
            self.interface.on_select(self.interface, row=selected)

    def _native_retrieve_virtual_item(self, sender, e):
        # Because ListView is in VirtualMode, it's necessary implement
        # VirtualItemsSelectionRangeChanged event to create ListViewItem when it's needed
        if self._cache and e.ItemIndex >= self._first_item and \
           e.ItemIndex < self._first_item + len(self._cache):
            e.Item = self._cache[e.ItemIndex - self._first_item]
        else:
            e.Item = WinForms.ListViewItem(self.row_data(self.interface.data[e.ItemIndex]))

    def _native_cache_virtual_items(self, sender, e):
        if self._cache and e.StartIndex >= self._first_item and \
           e.EndIndex <= self._first_item + len(self._cache):
            # If the newly requested cache is a subset of the old cache,
            # no need to rebuild everything, so do nothing
            return

        # Now we need to rebuild the cache.
        self._first_item = e.StartIndex
        new_length = e.EndIndex - e.StartIndex + 1
        self._cache = []

        # Fill the cache with the appropriate ListViewItems.
        for i in range(new_length):
            self._cache.append(WinForms.ListViewItem(self.row_data(self.interface.data[i])))

    def _native_item_selection_changed(self, sender, e):
        # update selection interface property
        self.interface._selection = self._selected_rows()

        if e.IsSelected:
            self.interface.on_select(self.interface, row=self.interface.data[e.ItemIndex])

    def _selected_rows(self):
        if not self.native.SelectedIndices.Count:
            return None

        if self.interface.multiple_select:
            selected = [row for i, row in enumerate(self.interface.data) if i in self.native.SelectedIndices]
            return selected
        else:
            return self.interface.data[self.native.SelectedIndices[0]]

    def _create_column(self, heading, accessor):
        col = WinForms.ColumnHeader()
        col.Text = heading
        col.Name = accessor
        return col

    def change_source(self, source):
        self.update_data()

    def row_data(self, item):
        # TODO: Winforms can't support icons in tree cells; so, if the data source
        # specifies an icon, strip it when converting to row data.
        def strip_icon(item, attr):
            val = getattr(item, attr, self.interface.missing_value)

            if isinstance(val, tuple):
                return str(val[1])
            return str(val)

        return [
            strip_icon(item, attr)
            for attr in self.interface._accessors
        ]

    def update_data(self):
        self.native.VirtualListSize = len(self.interface.data)
        self._cache = []

    def insert(self, index, item):
        self.update_data()

    def change(self, item):
        self.interface.factory.not_implemented('Table.change()')

    def remove(self, item):
        self.update_data()

    def clear(self):
        self.update_data()

    def set_on_select(self, handler):
        pass

    def scroll_to_row(self, row):
        self.native.EnsureVisible(row)

    def add_column(self, heading, accessor):
        self.interface.factory.not_implemented('Table.add_column()')

    def remove_column(self, accessor):
        self.interface.factory.not_implemented('Table.remove_column()')

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface.MIN_HEIGHT)

    def remove_column(self, accessor):
        self.native.Columns.RemoveByKey(accessor)

    def add_column(self, heading, accessor):
        self.native.Columns.Add(self._create_column(heading, accessor))
        self.update_data()
