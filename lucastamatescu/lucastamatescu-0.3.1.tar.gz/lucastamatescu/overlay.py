
class video_overlay_class:
    import cv2
    import numpy as np


    def __init__(self,overlay_image_name,window_name):
        import cv2
        import numpy as np
        cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        # # get the size of the screen
        # screen = screeninfo.get_monitors()[0]
        # width, height = screen.width, screen.height
        overlay_t_img = cv2.imread(overlay_image_name, -1)  # Load with transparency
        overlay_mask = overlay_t_img[:, :, 3:]  # And the alpha plane
        # Split out the transparency mask from the colour info

        overlay_img = overlay_t_img[:, :, :3]  # Grab the BRG planes
        # Again calculate the inverse mask
        background_mask = 255 - overlay_mask
        background_mask = cv2.cvtColor(background_mask, cv2.COLOR_GRAY2BGR)

        # Turn the masks into three channel, so we can use them as weights
        overlay_mask = cv2.cvtColor(overlay_mask, cv2.COLOR_GRAY2BGR)
        overlay_part = (overlay_img * (1 / 255.0)) * (overlay_mask * (1 / 255.0))

        self.__overlay_part = overlay_part
        self.__background_mask = background_mask
    def overlay_image(self,input_frame):
        import cv2
        import numpy as np
        print(input_frame.shape)
        height, width, depth = input_frame.shape
        # Display the resulting frame
        overlay_part = cv2.resize(self.__overlay_part, (width, height))
        background_mask = cv2.resize(self.__background_mask, (width, height))
        # Logo set up for 1920x1080
        # Create a masked out face image, and masked out overlay
        # We convert the images to floating point in range 0.0 - 1.0
        temporary_frame = (input_frame * (1 / 255.0)) * (background_mask * (1 / 255.0))
        # And finally just add them together, and rescale it back to an 8bit integer image
        output_frame = np.uint8(cv2.addWeighted(temporary_frame, 255.0, overlay_part, 255.0, 0.0))
        return output_frame


