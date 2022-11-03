from lib.object.game.Axis import Axis
from lib.object.visual.Text import Text
from re import search


class TextBlock(Text):
    def __init__(self, x=0, y=0, size=Axis.zero(), speed=Axis.zero(), sprite="", glow_scale=2, font_size=20, text="",
                 color=0, limit=100, title="", highlight_color=(255, 255, 255)):
        super().__init__(x, y, size, speed, sprite, glow_scale, font_size, text, color)

        self.limit = limit
        self.title = Text(text=title, x=self.x, y=self.y, font_size=font_size + 10)
        self.title.y -= self.title.get_hitbox_rect()[3] * 1.2

        self.text_list = []
        self.number_of_lines = 0
        self.highlight_color = highlight_color

        self.calculate_text_break()

    
    def write_line(self, line, line_height, offset=0, color=[255, 255, 255]) -> Text:
        text_obj = Text(text=line, font_size=self.font_size, x=self.x + offset,
                        y=self.y + line_height * self.number_of_lines, color=color)
        self.text_list.append(text_obj)

        return text_obj
        

    def calculate_text_break(self):
        x_offset = 0
        line = ""
        line_height = self.font.render(line, True, 0).get_size()[1] * 1.2
        word_list = self.text.split(" ")

        for word in word_list:
            next_line = line + word
            res = self.font.render(next_line, True, 0)
            size = res.get_size()

            # check if there is space left in line
            # if not, write current line and break to the next line  
            if (self.x + x_offset + size[0]) > self.limit:
                self.write_line(line, line_height, x_offset)
                line = ""
                self.number_of_lines += 1
                x_offset = 0

            # check if theres a highlighted word
            # if there is, write the current line 
            # and set an offset for the rest of the line
            if search(r"\*\*[A-zÀ-ú *]+\*\*", word):
                last_text = self.write_line(line, line_height, x_offset)

                word = word.replace("**", "")
                written_word = self.write_line(word, line_height, x_offset + last_text.get_size()[0], color=self.highlight_color)

                x_offset += last_text.get_size()[0] + written_word.get_size()[0]
                line = " "

            # if theres no highlight, add the word to the line normally
            else: 
                line += f"{word} "

        # write last line
        if line != "":
            self.write_line(line, line_height)
        
    def render(self, screen):
        self.title.render(screen, align="none")
        for text in self.text_list:
            text.render(screen, align="none")
