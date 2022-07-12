from pygame import font
from lib.utils.Constants import Constants


class FPS:
    def __init__(self):
        self.font = font.Font(Constants.FONT_RETRO_GAMING, 20)

    def render(self, display, fps, position):
        text = self.font.render(str(round(fps)), True, (255, 255, 255))
        position.x -= text.get_size()[0]
        display.blit(text,
                     position.to_list())  # todo - deixar dinamico o position (está fazendo  position=(resolution.x-30, 0))
