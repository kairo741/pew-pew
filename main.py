from lib.Engine import Engine


if __name__ == '__main__':
    engine = Engine()

    from lib.screen.MenuScreen import MenuScreen
    
    menu = MenuScreen(engine=engine)
    menu.start()
