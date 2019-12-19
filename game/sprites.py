from game.ai_sight import *

vec = pg.math.Vector2


def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.ticks_since_last_reward = 0
        self.sight = Sight()
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.hit_rect = s.PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.reward = 0
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * s.TILESIZE
        self.rot = 0
        self.sight_postions = []

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        move = PLAYER.get_move(self.sight.get_sight(self.pos, self.rot), self.reward)
        if move.left:
            self.rot_speed = s.PLAYER_ROT_SPEED
        if move.right:
            self.rot_speed = -s.PLAYER_ROT_SPEED
        if move.forward:
            self.vel = vec(s.PLAYER_SPEED, 0).rotate(-self.rot)
        if move.backward:
            self.vel = vec(-s.PLAYER_SPEED / 2, 0).rotate(-self.rot)

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.hit_rect.width / 2
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right + self.hit_rect.width / 2
                self.vel.x = 0
                self.hit_rect.centerx = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.hit_rect.height / 2
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom + self.hit_rect.height / 2
                self.vel.y = 0
                self.hit_rect.centery = self.pos.y

    def collide_with_reward_line(self):
        hits = pg.sprite.spritecollide(self, self.game.rewardLines, True, collide_hit_rect)
        if hits:
            self.reward = 10
            self.ticks_since_last_reward = 0
            print(hits)

    def get_sight(self):
        return self.sight.get_sight(self.pos, self.rot)

    def update(self):
        self.ticks_since_last_reward += 1
        if s.SHOW_AI_SIGHT:
            self.sight_postions = self.sight.get_sight_position(self.pos, self.rot)
        self.get_keys()
        self.collide_with_reward_line()
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        self.collide_with_walls('x')
        self.hit_rect.centery = self.pos.y
        self.collide_with_walls('y')
        self.rect.center = self.hit_rect.center


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * s.TILESIZE
        self.rect.y = y * s.TILESIZE


class RewardLine(pg.sprite.Sprite):
    def __init__(self, game, points, num=0):
        self.num = num
        self.groups = game.all_sprites, game.rewardLines
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.transform.scale(game.reward_line_img, (
            round(math.hypot(points[0][0] - points[1][0], points[0][1] - points[1][1])), 5))
        diff = tuple(map(lambda x, y: x - y, points[0], points[1]))
        if diff[0] == 0:
            self.image = pg.transform.rotate(self.image, 90)
        else:
            self.image = pg.transform.rotate(self.image, -math.degrees(math.atan(diff[1] / diff[0])))
        self.x = min(points[0][0], points[1][0])
        self.y = min(points[0][1], points[1][1])
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
