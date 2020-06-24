import ipywidgets
import pandas as pd

class Classy:
    grid = None
    html_section = None
    df = None
    current_pos = None
    html_col = None
    target = None
    labels = None
    label_buttons = None
    progress = None

    def __init__(self, df, html_col, target, labels):
        self.df = df
        self.html_col = html_col
        self.target = target
        self.labels = labels
        
        # go to next unfilled row
        self.current_pos = self.df[target].isnull().idxmax()
        
        if self.current_pos is None or self.current_pos > len(self.df):
            self.current_pos = self.df.iloc[0].index
        
        self.progress = ipywidgets.widgets.HTML(grid_area='progress')
        self.update_progress()
        
        # create main section
        self.update_to_pos(self.current_pos)
        
        previous_button = ipywidgets.widgets.Button(
            tooltip='previous',
            icon='arrow-left',
            layout=ipywidgets.Layout(height='auto', width='auto'),
            grid_area='prev'
        )
        next_button = ipywidgets.widgets.Button(
            tooltip='next', 
            icon='arrow-right',
            layout=ipywidgets.Layout(height='auto', width='auto'),
            grid_area='next'
        )
        previous_button.on_click(lambda b: self.move_pos('prev'))
        next_button.on_click(lambda b: self.move_pos('next'))
                
        clear_button = ipywidgets.Button(
            description='Clear',
            layout=ipywidgets.Layout(height='50px', width='auto'), 
            grid_area='clear'
        )    
        clear_button.on_click(lambda b: self.clear())
        
        self.set_button_labels()
        
        self.grid = ipywidgets.GridBox(
            children=[previous_button, self.html_section, next_button, clear_button, self.button_grid, self.progress],
            layout=ipywidgets.Layout(
                max_width='1400px',
                grid_template_rows='auto auto auto',
                grid_template_columns='10% 80% 10%',
                grid_template_areas='''
                    "prev main next"
                    "clear button_grid progress"
                '''
            )
        )
        
    def update_progress(self):
        total_number = len(self.df)
        n_pos = self.df.index.get_loc(self.current_pos)+1
        
        filled_df = self.df.copy(deep=True)
        filled_df.dropna(inplace=True)
        filled_df = filled_df[self.target]
        
        if len(filled_df) != 0:        
            filled_df = filled_df[filled_df != '']
            filled = len(filled_df)
        else:
            filled = 0
        
        self.progress.value = """
            <div style='width:100%; font-weight: bold; font-size: 18px; padding-top: 5px;'>
                &nbsp;{}/{} ({:.0%})
            </div>
        """.format(n_pos, total_number, filled/total_number)
        
    def clear(self):
        self.df.loc[self.current_pos, self.target] = ''
        self.update_to_pos(self.current_pos)

    def move_pos(self, direction):
        if direction == 'next':
            idx = self.get_pos(1)
        elif direction == 'prev':
            idx = self.get_pos(-1)            
        self.update_to_pos(idx)
        
    def get_pos(self, rel_pos):
        idx_list = self.df.index.to_list()
        try:
            idx_pos = idx_list.index(self.current_pos)
            if idx_pos + rel_pos >= len(idx_list):
                return idx_list[0]
            return idx_list[idx_pos+rel_pos]
        except:
            return self.current_pos
    
    
    def set_button_labels(self):
        def on_button_clicked(b):
            self.df.loc[self.current_pos, self.target] = b.description
            self.move_pos('next')
        
        selected_label = self.df.loc[self.current_pos][self.target]
        
        self.label_buttons = []
        for label in self.labels:
            is_selected = label == selected_label
            label_button = ipywidgets.Button(
                description=label, 
                button_style=('success' if is_selected else 'info'),
                layout=ipywidgets.Layout(height='50px', width='auto')
            )
            label_button.on_click(on_button_clicked)
            self.label_buttons.append(label_button)
        
        self.button_grid = ipywidgets.Box(
            children=self.label_buttons, 
            layout=ipywidgets.Layout(display='flex', flex_flow='row wrap', align_items='stretch'), 
            grid_area='button_grid'
        )

        if self.grid:
            self.grid.children = tuple(list(self.grid.children[:4]) + [self.button_grid] + [self.grid.children[-1]])
    
    def update_to_pos(self, pos):
        self.current_pos = pos
        description = self.df.loc[self.current_pos][self.html_col]        
        self.html_section = ipywidgets.widgets.HTML(
            value=description,
            layout=ipywidgets.Layout(height='auto', width='auto', padding='0 10px 10px 10px'), 
            grid_area='main'
        )
        if self.grid:
            self.grid.children = tuple([self.grid.children[0]] + [self.html_section] + list(self.grid.children[2:]))
            
        # iterate over buttons to deselect and reselect        
        self.set_button_labels()
        self.update_progress()
        
    def display(self):
        display(self.grid)
        
    def stats(self, figsize=(10,5)):
        plot_df = self.df.copy(deep=True)
        plot_df.dropna(inplace=True)
        label_series = plot_df[self.target]
        
        if len(label_series) == 0:        
            display('Data not found.')
            return
        
        label_series = label_series[label_series != '']
        
        if len(label_series) == 0:
            display('Data not found.')
            return
        
        counts = label_series.value_counts()
        plot_dict = {}
        for label in self.labels:
            plot_dict[label] = counts.get(label,0)
        
        ax = pd.Series(plot_dict).plot.bar(figsize=figsize)
        ax.set_xlabel(self.target, size=16, labelpad=15)
        ax.set_ylabel('occurences', size=16, labelpad=10)
        
        