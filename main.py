if __name__ == '__main__':
    from lib.utils.Config import Config
    from lib.Engine import Engine
    config = Config()
    engine = Engine(config.fullscreen)

    from lib.screen.MenuScreen import MenuScreen
    
    menu = MenuScreen(engine=engine)
    menu.start(intro=config.intro)
