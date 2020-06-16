import argparse
import csv
import tempfile

from bytegain.zap.utils import gcs
from google.cloud import storage


def _extract_date(filename):
    return filename.rsplit('/', 1)[-1].split('_')[4]


def combine_predictions_csv(gs_path, output, project='tough-hologram-156002'):
    """
    Reads predictions csv files from GCP and writes them into one big csv

    :param gs_path: path to csv files with predictions
    :param output: local path to a big csv
    :param project: GCP project
    :return:
    """
    print('Getting list of files from GCP')
    gcs_client = storage.Client(project=project)
    bucket, path = gcs.parse_gs_url(gs_path)
    bucket = gcs_client.bucket(bucket)
    blobs = list(bucket.list_blobs(prefix=path))
    blobs_csv = []
    # Get all blobs with predictions
    for blob in blobs:
        filename = blob.name
        if filename.endswith('with_emails.csv'):
            # Don't include predictions made in January (some data was missing)!
            month = _extract_date(filename).split('-')[1]
            if not month.startswith('01'):
                blobs_csv.append(blob)

    print('Sorting files')
    blobs_csv_sorted = sorted(blobs_csv, key=lambda x: x.name)

    local_tmp_path = tempfile.mkdtemp() + '/'
    from_date = '-'.join(_extract_date(blobs_csv_sorted[0].name).split('-')[:3])
    to_date = '-'.join(_extract_date(blobs_csv_sorted[-1].name).split('-')[-3:])
    output_filename = '%s_%s_%s.csv' % (output, from_date, to_date)
    print('Writing to %s' % output_filename)
    with open(output_filename, "w") as to_file:
        writer = csv.writer(to_file, delimiter=',')
        for blob_csv in blobs_csv_sorted:
            print('Reading file %s' % blob_csv.name)
            date = _extract_date(blob_csv.name)
            local_file_path = local_tmp_path + date + '.csv'
            blob_csv.download_to_filename(local_file_path)
            with open(local_file_path, mode='r') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    row.append(date)
                    writer.writerow(row)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('')
    parser.add_argument('--gs_dir', required=True, help='Path to gs with predictions',
                        default='gs://bg-dataflow/apartmentlist/user_value/predictions')
    parser.add_argument('--output', required=True, help='Path to local file where to save all predictions',
                        default='predictions.csv')

    args = parser.parse_args()

    combine_predictions_csv(args.gs_dir, args.output)
