import pygame
from settings import *


class Overlay:
    def __init__(self, player, day=0):
        self.font = pygame.font.Font('../font/LycheeSoda.ttf', 30)
        self.day = day
        # general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player

        # imports
        overlay_path = '../graphics/overlay/'
        self.tools_surf = {tool: pygame.image.load(f'{overlay_path}{tool}.png').convert_alpha() for tool in
                           player.tools}
        self.seeds_surf = {seed: pygame.image.load(f'{overlay_path}{seed}.png').convert_alpha() for seed in
                           player.seeds}

    def display(self):
        # tool
        tool_surf = self.tools_surf[self.player.selected_tool]
        tool_rect = tool_surf.get_rect(midbottom=OVERLAY_POSITIONS['tool'])
        self.display_surface.blit(tool_surf, tool_rect)

        # seeds
        seed_surf = self.seeds_surf[self.player.selected_seed]
        seed_rect = seed_surf.get_rect(midbottom=OVERLAY_POSITIONS['seed'])
        self.display_surface.blit(seed_surf, seed_rect)

        # seeds number
        if self.player.selected_seed == 'corn':
            seed = self.player.seed_inventory.get('corn')
            seed_surface = self.font.render(f'owned: {seed}', False, 'White')
            seed_rectangle = seed_surface.get_rect(midright=OVERLAY_POSITIONS['seed_amount'])
            self.display_surface.blit(seed_surface, seed_rectangle)
        else:
            seed = self.player.seed_inventory.get('tomato')
            seed_surface = self.font.render(f'owned: {seed}', False, 'White')
            seed_rectangle = seed_surface.get_rect(midright=OVERLAY_POSITIONS['seed_amount'])
            self.display_surface.blit(seed_surface, seed_rectangle)

        # day number
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = WEEKDAYS[(self.day % 7)]
        day_number = font.render("Day: " + str(self.day + 1), True, 'White')
        day_name = font.render(text, True, 'White')
        self.display_surface.blit(day_number, (10, 10))
        self.display_surface.blit(day_name, (10, 40))

    def next_day(self):
        self.day += 1
