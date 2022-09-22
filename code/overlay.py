import pygame
import datetime
from settings import *
from timer import Timer


class Overlay:
    def __init__(self, player, day=0):
        self.font = pygame.font.Font('../font/LycheeSoda.ttf', 30)
        # time setup
        self.check_part_of_day = True
        self.day = day
        # general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.timer = Timer(100)

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

        # time
        self.display_day()

    def display_day(self):
        font = pygame.font.Font('freesansbold.ttf', 32)

        # day number
        text = DAYS_OF_WEEK[(self.day % 7)]
        day_number = font.render("Day: " + str(self.day + 1), True, 'White')
        day_name = font.render(text, True, 'White')
        self.display_surface.blit(day_number, (10, 10))
        self.display_surface.blit(day_name, (10, 40))

        # hours and minutes
        self.timer.activate()
        day_time = datetime.datetime.utcfromtimestamp(self.timer.start_time + 28000).strftime("%H:%M %p")
        if day_time == '23:59 PM':
            if self.check_part_of_day:
                self.next_day()
                self.check_part_of_day = False
        if day_time == '01:00 AM':
            self.check_part_of_day = True
        self.display_surface.blit(font.render(day_time, True, 'White'), (10, 80))

        # part of the day
        moment_of_day = self.get_moment_of_day(day_time)
        self.display_surface.blit(font.render(moment_of_day, True, 'White'), (10, 110))

    def get_moment_of_day(self, date):
        day_time = ''
        integer_date = int(date[:2])
        if 5 <= integer_date < 12:
            day_time = TIME_OF_DAY[0]
        elif 12 <= integer_date < 17:
            day_time = TIME_OF_DAY[1]
        elif 17 <= integer_date < 21:
            day_time = TIME_OF_DAY[2]
        elif 21 <= integer_date:
            day_time = TIME_OF_DAY[3]
        elif integer_date < 5:
            day_time = TIME_OF_DAY[3]
        return day_time

    def next_day(self):
        self.day += 1
        self.timer.increase_time()
