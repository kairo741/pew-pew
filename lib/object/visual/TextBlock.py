from lib.object.game.Axis import Axis
from lib.object.visual.Text import Text


class TextBlock(Text):
    def __init__(self, x=0, y=0, size=Axis.zero(), speed=Axis.zero(), sprite="", glow_scale=2, font_size=20, text="", color=0, limit=100, title=""):
        super().__init__(x, y, size, speed, sprite, glow_scale, font_size, text, color)

        self.limit = limit
        self.title = Text(text=title, x=self.x, y=self.y, font_size=font_size+10)
        self.title.y -= self.title.get_hitbox_rect()[3]*1.2

        self.text_list = []

        self.calculate_text_break()


    def calculate_text_break(self):
        phrase = ""
        line_height = self.font.render(phrase, True, 0).get_size()[1]*1.2
        word_list = self.text.split(" ")

        for word in word_list:
            next_phrase = phrase + word
            res = self.font.render(next_phrase, True, 0)
            size = res.get_size()

            if (self.x + size[0]) > self.limit:
                text_obj = Text(text=phrase, font_size=self.font_size, x=self.x, y=self.y + line_height*len(self.text_list))
                self.text_list.append(text_obj)
                phrase = f"{word} "

            else:
                phrase += f"{word} "

        text_obj = Text(text=phrase, font_size=self.font_size, x=self.x, y=self.y + line_height*len(self.text_list))
        self.text_list.append(text_obj)
                


    def render(self, screen):
        self.title.render(screen, align="none")
        for text in self.text_list:
            text.render(screen, align="none")
        
