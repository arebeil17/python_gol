import pygame
import pygame_gui


class GameGui:
    def __init__(self, game_config):

        manager = pygame_gui.UIManager(
            (game_config.window_dim[0], game_config.window_dim[1]), 'menu.json')

        self.background = pygame.Surface(
            (game_config.window_dim[0], game_config.window_dim[1]))

        self.start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((game_config.window_dim[0] // 2 - 100,
                                                                                    game_config.window_dim[1] // 2), (200, 50)),
                                                         text='Start',
                                                         manager=manager)
        self.manager = manager

        self.mode_rect = pygame.Rect((game_config.window_dim[0] // 2 - 100,
                                      game_config.window_dim[1] // 2 + 50), (200, 50))

        self.speed_rect = pygame.Rect((game_config.window_dim[0] // 2 - 100,
                                       game_config.window_dim[1] // 2 + 100), (200, 50))

        self.scale_rect = pygame.Rect((game_config.window_dim[0] // 2 - 100,
                                       game_config.window_dim[1] // 2 + 150), (200, 50))

        self.color_rect = pygame.Rect((game_config.window_dim[0] // 2 - 100,
                                       game_config. window_dim[1] // 2 + 200), (200, 50))

        self.mode_button = pygame_gui.elements.UIButton(self.mode_rect, text=f'Game Mode: {game_config.get_current_selection("mode")[0]}',
                                                        manager=self.manager)

        self.speed_button = pygame_gui.elements.UIButton(self.speed_rect, text=f'Sim Speed: {game_config.get_current_selection("fps")[0]}',
                                                         manager=self.manager)

        self.scale_button = pygame_gui.elements.UIButton(self.scale_rect, text=f'Cell Size: {game_config.get_current_selection("scale")[0]}',
                                                         manager=self.manager)

        self.color_button = pygame_gui.elements.UIButton(self.color_rect, text=f'Color: {game_config.get_current_selection("color")[0]}',
                                                         manager=self.manager)

    def update_setting_button(self, game_config, setting_key, button_rect):
        setting = game_config.selection_dict[setting_key]
        num_settings = len(game_config.setting_dict[setting_key])
        game_config.selection_dict[setting_key] = (setting + 1) % num_settings

        prefix_str = ""
        if setting_key == "mode":
            prefix_str = "Game Mode:"
            pygame_gui.elements.UIButton(button_rect,
                                         text=f'{prefix_str} {game_config.get_current_selection(setting_key)[0]}',
                                         manager=self.manager)
        elif setting_key == "fps":
            prefix_str = "Sim Speed:"
            pygame_gui.elements.UIButton(button_rect,
                                         text=f'{prefix_str} {game_config.get_current_selection(setting_key)[0]}',
                                         manager=self.manager)
        elif setting_key == "scale":
            prefix_str = "Cell Size:"
            pygame_gui.elements.UIButton(button_rect,
                                         text=f'{prefix_str} {game_config.get_current_selection(setting_key)[0]}',
                                         manager=self.manager)
        elif setting_key == "color":
            prefix_str = "Color:"
            pygame_gui.elements.UIButton(button_rect,
                                         text=f'{prefix_str} {game_config.get_current_selection(setting_key)[0]}',
                                         manager=self.manager)

        print(
            f'{setting_key} : {game_config.selection_dict[setting_key]}')

    def create_title_text_bar(self, window_dim):

        color = (46, 83, 205)  # Nice blue
        font_size = 96

        font = pygame.font.SysFont('arial', font_size, True, False)
        text = font.render('Game of Life', True, color, None)

        textRect = text.get_rect()

        textRect.center = (window_dim[0] // 2, (window_dim[1] // 2) // 2)

        return text, textRect

    def create_title_outline_text_bar(self, window_dim, textRect):

        outline_color = (255, 255, 255)
        font_size = 96

        font = pygame.font.SysFont('arial', font_size, True, False)
        text = font.render('Game of Life', True, outline_color, None)

        outline = 2
        outlineSurf = font.render('Game of Life', True, outline_color)
        outlineSize = outlineSurf.get_size()
        textSurf = pygame.Surface(
            (outlineSize[0] + outline*2, outlineSize[1] + 2*outline))
        textRect = textSurf.get_rect()
        offsets = [(ox, oy)
                   for ox in range(-outline, 2*outline, outline)
                   for oy in range(-outline, 2*outline, outline)
                   if ox != 0 or ox != 0]
        for ox, oy in offsets:
            px, py = textRect.center
            textSurf.blit(outlineSurf, outlineSurf.get_rect(
                center=(px+ox, py+oy)))
        innerText = font.render(
            'Game of Life', True, outline_color).convert_alpha()
        textSurf.blit(innerText, innerText.get_rect(
            center=textRect.center))

        textRect.center = (window_dim[0] // 2, (window_dim[1] // 2) // 2)

        return text, textRect

    def create_text_bar(self, window_dim, info_string):

        white = (255, 255, 255)

        font = pygame.font.Font('freesansbold.ttf', 20)

        text = font.render(info_string, True, white, None)

        textRect = text.get_rect()

        textRect.center = (window_dim[0] // 2, window_dim[1] - 20)

        return text, textRect
