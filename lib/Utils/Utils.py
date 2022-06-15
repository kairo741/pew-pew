from pygame import transform


class Utils:
    @staticmethod
    def scale_image(image, scale):
        return transform.smoothscale(image, (image.get_width() * scale, image.get_height() * scale))
