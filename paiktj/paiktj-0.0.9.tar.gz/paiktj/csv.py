from paiktj.multiprocessing import pool
import csv


def save_csv_map_multi(func, iterable, path, column, batch=1000, processes=None):
    assert len(func(iterable[0])) == len(column)
    with open(path, 'w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(column)
        for start_pt in range(0, len(iterable), batch):
            print('calculating start points : ', start_pt)
            end_pt = min(start_pt + batch, len(iterable))
            result = pool(func, iterable[start_pt: end_pt], processes, end_pt - start_pt)
            writer.writerows(result)
