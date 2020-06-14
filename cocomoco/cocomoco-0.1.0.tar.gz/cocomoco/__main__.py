import sys
import argparse
import cocomoco

try:
    import matplotlib.pyplot
    import matplotlib.ticker
except:
    matplotlib.pyplot = None
    matplotlib.ticker = None

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

DEMO_CLOC_RANGE_START =  100000
DEMO_CLOC_RANGE_STOP  =  500000
DEMO_CLOC_RANGE_STEP  =   10000
DEMO_CLOC_RANGE = range(DEMO_CLOC_RANGE_START,
                        DEMO_CLOC_RANGE_STOP + DEMO_CLOC_RANGE_STEP,
                        DEMO_CLOC_RANGE_STEP)

DEMO_MODE_FIGSIZE = (12, 8)
DEMO_MODE_DPI = 300

def demo_mode_check():
    if not matplotlib:
        print('matplotlib required for demo-mode, please install it via pip')
        sys.exit(EXIT_FAILURE)

def demo_mode_basic_line_chart():
    fig, ax = matplotlib.pyplot.subplots(figsize=DEMO_MODE_FIGSIZE, dpi=DEMO_MODE_DPI)
    #fig.tight_layout()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.tick_params(top=False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    vibrant = ('#ee7733',  '#cc3311', '#0077bb', '#009988', '#33bbee',  '#ee3377', '#bbbbbb')
    light = ('#77AADD', '#EE8866', '#EEDD88', '#FFAABB', '#99DDFF', '#44BB99', '#BBCC33', '#AAAA00', '#DDDDDD', '#000000')
    return fig, ax

def demo_calc_linear(x_range, start):
    linear_val = list()
    base = start / x_range[0]
    for x in x_range:
        linear_val.append(x * base)
    return linear_val

def demo_mode_chart_basic_modes():
    models = ['Embedded', 'Semidetached', 'Organic']
    fig, ax = demo_mode_basic_line_chart()
    for modelname in models:
        effort_list = list()
        for cloc in DEMO_CLOC_RANGE:
            model = cocomoco.model_by_name(modelname)
            cm = cocomoco.calculate(cloc, model=model)
            effort_list.append(cm.effort)

        # linear helper line
        linear_effort_list = demo_calc_linear(DEMO_CLOC_RANGE, effort_list[0])
        linear_effort_list_year = [i // 12 for i in linear_effort_list]
        ax.plot(DEMO_CLOC_RANGE, linear_effort_list_year, color='#000000', alpha=.3, linewidth=2., linestyle='dotted')
        # real plot
        effort_list_year = [i // 12 for i in effort_list]
        ax.plot(DEMO_CLOC_RANGE, effort_list_year, label=modelname, linewidth=4.)

    ax.grid(alpha=.2);
    ax.legend(loc='upper left')
    ax.set_xlabel('Source Lines of Code [kilo]')
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: int(x//1000)))
    ax.set_ylabel('Effort [Developer Years]')
    fig.suptitle('Cocomo Metric - Effort for Standard Models')
    fig.tight_layout()
    filename = "cocomo-effort-standard-models.png"
    print(f'saving {filename}')
    matplotlib.pyplot.savefig(filename, transparent=False)


def demo_mode_productivity():
    models = ['Embedded', 'Semidetached', 'Organic']
    fig, ax = demo_mode_basic_line_chart()
    for modelname in models:
        productivity_list = list()
        for cloc in DEMO_CLOC_RANGE:
            model = cocomoco.model_by_name(modelname)
            cm = cocomoco.calculate(cloc, model=model)
            productivity_list.append(cm.sloc_per_staff_month)

        ax.plot(DEMO_CLOC_RANGE, productivity_list, label=modelname, linewidth=4.)

    ax.grid(alpha=.2);
    ax.legend(reversed(matplotlib.pyplot.legend().legendHandles), reversed(models), loc='upper right')
    ax.set_xlabel('Source Lines of Code [kilo]')
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: int(x//1000)))
    ax.set_ylabel('Productivity [Lines of Code per Staff Member and Month]')
    fig.suptitle('Cocomo Metric - Productivity for Standard Models')
    fig.tight_layout()
    filename = "cocomo-productivity-standard-models.png"
    print(f'saving {filename}')
    matplotlib.pyplot.savefig(filename, transparent=False)

def demo_mode():
    print('cocomoco - demo time!')
    demo_mode_check()
    demo_mode_chart_basic_modes()
    demo_mode_productivity()
    return EXIT_SUCCESS

def main(args):
    if args.demo_mode:
        return demo_mode()
    if not args.sloc or args.sloc <= 0:
        print("--sloc must be larger as 0")
        return 1
    model = cocomoco.Organic()
    if args.model == 'semidetached':
         model=cocomoco.Semidetached()
    elif args.model == 'embedded':
         model=cocomoco.Embedded()
    cm = cocomoco.calculate(args.sloc, model=model)
    print('Cocomo Metric')
    print(f'Source Lines of Code: {args.sloc} (KLOC: {args.sloc // 1000})')
    print(f'Effort: {cm.effort:.1f} person-months ({cm.effort / 12.0:.1f} person-years)')
    print(f'Time to Develop: {cm.dtime:.1f} months, Staff:{cm.staff:.1f}')
    print(f'Productivity: {cm.sloc_per_staff_month:.0f} lines of code per staff member and month')
    print(f'Cost: {cm.cost:.2f} with with salary of {cm.salary:.2f}')
    print(f'Used model: {cm.model_name}')
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--sloc", help="source code lines", type=int, default=None)
    parser.add_argument("--model", help="model: organic, semidetached or embedded", default='organic', choices=['organic', 'semidetached', 'embedded'],)
    parser.add_argument("--demo-mode", help="print some graph using different values for cocomoco", action='store_true', default=False)
    args = parser.parse_args()
    sys.exit(main(args) or EXIT_SUCCESS)
