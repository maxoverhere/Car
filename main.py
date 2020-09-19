import sys
import time
from game.sprites import *
from game.tilemap import *
from players.ai_table import QLearning
from os import path


class Game:
    def __init__(self):
        pg.init()
        self.rewardLines = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.dt = 1 / FPS
        self.clock = pg.time.Clock()
        self.load_data()
        self.skip_visuals = SKIP_VISUALS
        self.limit_frames = LIMIT_FRAMES

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        map_folder = path.join(game_folder, 'maps')
        self.map = Map(path.join(map_folder, MAP_SELECTED))
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))
        self.reward_line_img = pg.image.load(path.join(img_folder, REWARD_LINE_IMG)).convert_alpha()

    def wipe_board(self):
        self.player.kill()
        all_rewards = self.rewardLines.sprites()
        for reward_line in all_rewards:
            reward_line.kill()
        if type(PLAYER) is QLearning:
            PLAYER.set_last_move_to_null()

    def reset_game(self):
        if hasattr(self, 'player'):
            self.wipe_board()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == 'P':
                    self.player = Player(self, col, row)
        for reward_line in REWARD_LINES:
            RewardLine(self, reward_line)

    def new(self):
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
        self.reset_game()
        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        while True:
            if self.limit_frames:
                self.dt = self.clock.tick(FPS) * 0.001
            self.events()
            self.update()
            if not self.skip_visuals:
                self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()
        if DIE_WITHOUT_REWARD:
            if self.player.ticks_since_last_reward == FPS * 2:
                self.reset_game()
        self.camera.update(self.player)

    def draw(self):
        self.screen.fill(BGCOLOR)
        for sight_point in self.player.sight_postions:
            pg.draw.circle(self.screen, RED, (sight_point[0] - 30, sight_point[1] - 30), 20)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_o:
                    if type(PLAYER) is QLearning:
                        PLAYER.save_data()
                        print("saved data")
                    self.quit()
                if event.key == pg.K_p:
                    print(self.player.get_sight())
                if event.key == pg.K_l:
                    time.sleep(5)
                if event.key == pg.K_k:
                    self.skip_visuals = not self.skip_visuals
                if event.key == pg.K_i:
                    self.limit_frames = not self.limit_frames
                    self.dt = 1 / FPS


g = Game()
while True:
    g.new()
    g.run()
