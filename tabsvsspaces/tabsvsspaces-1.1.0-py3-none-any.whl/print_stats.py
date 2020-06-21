from tabsvsspaces.stats import Statistics


def print_stats(stats: Statistics, by_extension: bool):
    print('spaces:', stats.all_spaces)
    print('tabs:', stats.all_tabs)
    print('mixed:', stats.all_mixed)
    if by_extension:
        for ext in set(stats.space_dict.keys()) | stats.tab_dict.keys() | stats.mixed_line_dict.keys():
            print(ext + ':')
            print('  ', 'spaces:', stats.space_dict[ext])
            print('  ', 'tabs:', stats.tab_dict[ext])
            print('  ', 'mixed:', stats.mixed_line_dict[ext])
    if stats.all_mixed > 0:
        print('files_with_mixed_lines:')
        for file in stats.mixed_files:
            print(' -', file)
