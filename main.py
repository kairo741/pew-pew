from lib.Engine import Engine
from lib.screen.MenuScreen import MenuScreen

if __name__ == '__main__':
    engine = Engine()
    menu = MenuScreen(engine=engine)
    menu.start()
