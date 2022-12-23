import pygame, sys, time
from sprites import *

pygame.init()
fps = 60
fpsClock = pygame.time.Clock()
width = WINDOW_WIDTH
height = WINDOW_HEIGHT

screen = pygame.display.set_mode((width, height))

BLUE_1 = '#003366'
BLUE_2 = '#004C99'


class Button:
	def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None):
		self.onclickFunction = onclickFunction
		self.buttonSurface = pygame.Surface((width, height))
		self.buttonRect = pygame.Rect(x, y, width, height)
		font = pygame.font.Font('../graphics/font/Braxton-Regular.ttf', 60)
		self.buttonSurf = font.render(buttonText, True, (20, 20, 20))

	def process(self):
		mouse_pos = pygame.mouse.get_pos()
		self.buttonSurface.fill(BLUE_1)
		if self.buttonRect.collidepoint(mouse_pos):
			self.buttonSurface.fill(BLUE_2)
			if pygame.mouse.get_pressed(num_buttons=3)[0]:
				self.onclickFunction()

		self.buttonSurface.blit(self.buttonSurf, [
			self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
			self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
		])
		screen.blit(self.buttonSurface, self.buttonRect)


class Menu:
	def __init__(self):
		pygame.display.set_caption("Menu")

		# text
		self.font = pygame.font.Font('../graphics/font/VerberaC.ttf', 60)

		# music
		self.music = pygame.mixer.Sound('../sounds/MUSIC.mp3')
		self.music.play(loops=-1)

	def draw(self):
		start_button = Button(180, 230, 320, 100, "Start game", start)
		exit_button = Button(180, 100, 320, 100, "Exit", exit_func)
		while True:
			bg_image = pygame.image.load('../graphics/environment/background.png').convert()
			background_height = bg_image.get_height()
			scale_factor = WINDOW_HEIGHT / background_height
			full_height = bg_image.get_height() * scale_factor
			full_width = bg_image.get_width() * scale_factor
			full_sized_image = pygame.transform.scale(bg_image, (full_width, full_height))
			screen.blit(full_sized_image, (0, 0))

			screen.blit(pygame.image.load('../graphics/environment/ground.png').convert_alpha(), [0, height - 69])
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			start_button.process()
			exit_button.process()
			pygame.display.flip()


class Game:
	def __init__(self):
		# setup
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		pygame.display.set_caption('Fly-jump-die')
		self.clock = pygame.time.Clock()
		self.active = True

		# sprite
		self.all_sprites = pygame.sprite.Group()
		self.collision_sprites = pygame.sprite.Group()

		# scale_factor
		bg_height = pygame.image.load('../graphics/environment/background.png').get_height()
		self.scale_factor = WINDOW_HEIGHT / bg_height

		# sprite setup
		Background(self.all_sprites, self.scale_factor)
		Ground([self.all_sprites, self.collision_sprites], self.scale_factor)
		self.player = Player(self.all_sprites, self.scale_factor / 2)

		# timer
		self.obstacle_timer = pygame.USEREVENT + 10
		pygame.time.set_timer(self.obstacle_timer, 1200)

		# text
		self.font = pygame.font.Font('../graphics/font/VerberaC.ttf', 60)
		self.score = 0
		self.start_offset = pygame.time.get_ticks()

		# menu#
		self.play_val = True
		self.restart_button = Button(200, 200, 300, 100, "restart", self.restart)
		self.menu_button = Button(200, 320, 300, 100, "menu", self.to_menu)

	def collisions(self):
		if pygame.sprite.spritecollide(self.player, self.collision_sprites, False, pygame.sprite.collide_mask)\
			or self.player.rect.top <= 0:
			for sprite in self.collision_sprites.sprites():
				if sprite.sprite_type == 'obstacle':
					sprite.kill()
			self.active = False
			self.player.kill()

	def display_score(self):
		if self.active:
			self.score = (pygame.time.get_ticks() - self.start_offset) // 1200
			y = WINDOW_HEIGHT / 100
			x = WINDOW_WIDTH - 110
		else:
			y = 130
			x = WINDOW_WIDTH / 2

		score_surf = self.font.render(f"Score: " + str(self.score), True, 'red')
		score_rect = score_surf.get_rect(midtop=(x, y))
		self.display_surface.blit(score_surf, score_rect)

	def run(self):
		last_time = time.time()
		while self.play_val:
			# delta time
			dt = time.time() - last_time
			last_time = time.time()

			# event loop
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if self.active:
						self.player.jump()
					if not self.active:
						self.player = Player(self.all_sprites, self.scale_factor / 1.7)
						self.active = True
						self.start_offset = pygame.time.get_ticks()

				if event.type == self.obstacle_timer and self.active:
					Obstacle([self.all_sprites, self.collision_sprites], self.scale_factor * 1)

			# game logic
			self.all_sprites.update(dt)
			self.all_sprites.draw(self.display_surface)
			self.display_score()

			if self.active:
				self.collisions()
			else:
				self.restart_button.process()
				self.menu_button.process()

			pygame.display.update()
			self.clock.tick(FRAMERATE)

	def restart(self):
		game = Game()
		game.run()


	def to_menu(self):
		self.play_val = False


def start():
	game = Game()
	game.run()


def exit_func():
	exit()


if __name__ == '__main__':
	menu = Menu()
	menu.draw()
