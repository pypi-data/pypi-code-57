
class BoundaryBox:

    def __init__(self, xmin: float, ymin: float, xmax: float, ymax: float):
        """
        Construct BoundaryBox object
        :param obj: with float elements 'XMin', 'YMin', 'XMax', 'YMax'
        """
        self.data = [{'x': xmin, 'y': ymin}, {'x': xmax, 'y': ymax}]

    def scale_coordinates(self, image_width: int, image_height: int):
        """
        Scales up relative coordinates from range [0; 1] to image size
        :param image_width: in pixels
        :param image_height: in pixels
        """
        if any(v['x'] > 1 or v['y'] > 1 for v in self.data):
            return
        for v in self.data:
            v['x'] = v['x'] * image_width
            v['y'] = v['y'] * image_height
