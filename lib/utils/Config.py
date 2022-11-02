class Config:
    def __init__(self):
        self.fullscreen = 0
        self.intro = 1
        self.volume = 10

        self.read_config()

    def read_config(self):
        try:
            file = open("config.ini", "r")
            self.lines_to_config(file.readlines())
        except:
            self.create_config()

    def lines_to_config(self, lines):
        for line in lines:
            if "fullscreen=" in line:
                self.fullscreen = int(line.split("=")[1])

            elif "intro=" in line:
                self.intro = int(line.split("=")[1])

            elif "volume=" in line:
                self.volume = int(line.split("=")[1])

    def create_config(self):
        file = open("config.ini", "w")
        lines = [
            "fullscreen=0",
            "intro=1",
            "volume=1",
        ]

        for line in lines:
            file.write(f"{line}\n")
