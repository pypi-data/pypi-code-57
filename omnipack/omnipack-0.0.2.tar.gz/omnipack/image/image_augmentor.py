from PIL import Image
from .transformer import Transformer
import omnipack
import os.path as osp


class ImageAugmentor(object):

    def __init__(self, img):
        if isinstance(img, str):
            self._imgs = [img]
        elif isinstance(img, (tuple, list)):
            self._imgs = img
        else:
            raise TypeError(
                'Argument img must be a string or a tuple/list of string')

        self._augmentation = []

    def get(self, idx: int):
        """
        Get image path by index
        """
        return self._imgs[idx]

    def add(self, transformer: Transformer):
        """
        Add a transformer module to augmentation pipeline
        """
        assert isinstance(transformer, Transformer)
        self._augmentation.append(transformer)

    def run(self, times: int, output_path: str):
        """
        Run augmentation by a number of times defined by argument
        times and save to output_path
        """
        assert isinstance(times, int) and times > 0
        assert isinstance(output_path, str)

        omnipack.mkdir(output_path)

        for img_id, img_path in enumerate(self._imgs):
            img = Image.open(img_path)
            img_name = osp.basename(img_path)
            for i in range(times):
                img_temp = img.copy()
                for trans in self._augmentation:
                    img_temp, _ = trans(img_temp)
                img_save_path = osp.join(
                    output_path, '{}_{}_{}'.format(img_id, i, img_name))

                img_temp.save(img_save_path)
