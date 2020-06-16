import abc
import csv
import json
import os
import os.path
import tempfile

from bytegain.custom.iox.file.wofs import Wofs

GCS_BUCKET = 's3://al-bytegain'
GCS_PROJECT = 'bg-rest-api'

class BaseModelSpec(object, metaclass=abc.ABCMeta):

    def __init__(self, model_name, path):
        assert '/' not in model_name, "model_name may not contain '/'"
        self._model_name = model_name
        self._path = path
        if self._path is None:
            self._path = tempfile.mkdtemp("model")

        if len(self._path) > 0 and self._path[-1] != '/':
            self._path += '/'

    @property
    def model_name(self):
        return self._model_name

    @abc.abstractmethod
    def get_all_files(self, for_prod):
        pass

    def _create_name(self, extension):
        return "%s%s.%s" % (self._path, self._model_name, extension)

    def get_model_file(self):
        return self._create_name("model")

    def get_row_handler_file(self):
        return self._create_name("rh")

    def get_decile_file(self):
        return self._create_name("decile")

    def get_validation_file(self):
        return self._create_name("v.csv")

    def get_json_file(self):
        return self._create_name("json")

    def save(self, model, row_handler, results):
        model.save(self.get_model_file())
        row_handler.save(self.get_row_handler_file())
        save_deciles(self.get_decile_file(), results)
        save_results_as_csv(self.get_validation_file(), "id", "pred", results)

    def download(self, dir_path=None, for_prod=True):
        """
        Download model files from dir_path into the local files referenced this ModelSpec
        :param dir_path: The dir containing the files to download.  If None, defaults to ``GCS_BUCKET/self.model_name``.
        :param for_prod:
        :return: self
        """
        if dir_path is None:
            dir_path = GCS_BUCKET + '/' + self.model_name
        wofs = Wofs(
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"]
        )
        for filepath in self.get_all_files(for_prod=for_prod):
            basename = os.path.basename(filepath)
            wofs.download(os.path.join(dir_path, basename), filepath)

    def upload(self, dir_path=None):
        # type: (str) -> None
        """
        Copy the model files into dir_path.  For dir_path in S3, profile 'model-writer' is used.
        :param dir_path: A dirname path in the syntax of bytegain.io.file.wofs, e.g.,
         s3://bucket/k/e/y or /tmp/junk.  If None, defaults to ``GCS_BUCKET/self.model_name``.
        :return: None
        """
        if dir_path is None:
            dir_path = GCS_BUCKET + '/' + self.model_name
        wofs = Wofs(
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"]
        )
        for filepath in self.get_all_files(for_prod=False):
            basename = os.path.basename(filepath)
            wofs.upload(filepath, os.path.join(dir_path, basename))


class ModelSpec(BaseModelSpec):
    def __init__(self, model_name, path):
        super(ModelSpec, self).__init__(model_name, path)

    def get_model_meta_file(self):
        return self._create_name("model.meta")

    def get_all_files(self, for_prod=True):
        files = [self.get_model_file(), self.get_model_meta_file(), self.get_row_handler_file(), self.get_decile_file()]
        if not for_prod:
            files.append(self.get_validation_file())
        return files


class XgbModelSpec(BaseModelSpec):
    def __init__(self, model_name, path):
        super(XgbModelSpec, self).__init__(model_name, path)

    def get_all_files(self, for_prod=True):
        files = [self.get_model_file(), self.get_row_handler_file(), self.get_decile_file()]
        if not for_prod:
            files.append(self.get_validation_file())
        return files


def save_deciles(filename, results):
    vals = []
    results.reverse()
    for result in results:
        vals.append(result['probability'])
    length = len(vals)
    with open(filename, 'w') as output:
        output.write("0.0, ")
        for i in range(1, 100):
            val = vals[int(length * i / 100)]
            output.write("%6.4f," % val)
        output.write("1.0\n")


def save_results_as_csv(filename, id_header, prediction_header, results):
    with open(filename, "w") as f:
        out = csv.writer(f)
        #out.writerow(['user_id', 'rental_id', 'predicted_score'])
        out.writerow(['event_id', 'predicted_score'])
        for result in results:
            # user_id, property_id = result['id'].split('p')
            # out.writerow([user_id, 'p%s' % property_id, result['probability']])
            out.writerow([result['id'], result['probability']])


def save_json_spec(filename, model_name, row_handler):
    feature_spec = row_handler.get_feature_spec()
    feature_spec["model"] = model_name
    with open(filename, 'w') as output:
        json.dump(feature_spec, fp=output, sort_keys=True, indent=4)
