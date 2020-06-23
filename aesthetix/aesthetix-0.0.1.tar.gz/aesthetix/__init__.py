import sys

def progress_bar(header, curr_iteration, total_iterations, num_bars=30, output_vals={}, jump_line = True):
    """
        Shows a progress bar when called inside a loop
        params:
            header : display message for the bar
            curr_iteration, total_iterations : what you think they mean
            num_bars
            output_vals: dictionary of values to be displayed
    """
    num_bars = min(num_bars, total_iterations)
    total_iter = total_iterations
    total_iterations -= total_iterations%num_bars
    percent = min(100*curr_iteration/(total_iterations-1), 100.00)
    bars = round((num_bars*percent)/100)
    done = '[' + bars*'='
    todo = (num_bars - bars)*'~' + ']'
    valstring = ""
    for i, val in enumerate(output_vals):
        valstring += val + " : " + f"{(output_vals[val]):.2f}" + " "
    print(f"\r{header}:{done+todo}({percent:3.2f}%)  {valstring}", end = "")
    sys.stdout.flush()

    if(curr_iteration == total_iter-1) and jump_line:
        sys.stdout.flush()
        print()