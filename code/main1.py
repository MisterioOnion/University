import sys
import time
from sprites import *
from save import *
from parameters import *

pygame.init()

fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))


class Button:
	def __init__(self, x, y, width, height, buttonText = 'Button', onclickFunction = None):
		self.onclickFunction = onclickFunction
		self.buttonSurface = pygame.Surface((width, height))
		self.buttonRect = pygame.Rect(x, y, width, height)
		font = pygame.font.Font('../graphics/font/Braxton-Regular.ttf', 50)
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
	def __init__(self, ground_form, background_form):
		pygame.display.set_caption("Menu")
		self.ground_from = ground_form
		self.background_form = background_form

		# music
		self.music = pygame.mixer.Sound('../sounds/MUSIC.mp3')
		self.music.play(loops=-1)

	def draw_menu(self):

		exit_button = Button(180, 120, 320, 85, "Exit", exit_func)
		start_button = Button(180, 250, 320, 85, "Start game", start)
		optional_button = Button(180, 380, 320, 85, "Optional", optional_func)

		while True:
			bg_image = pygame.image.load(self.background_form).convert()
			background_height = bg_image.get_height()
			scale_factor = WINDOW_HEIGHT / background_height
			full_height = bg_image.get_height() * scale_factor
			full_width = bg_image.get_width() * scale_factor
			full_sized_image = pygame.transform.scale(bg_image, (full_width, full_height))
			screen.blit(full_sized_image, (0, 0))

			screen.blit(pygame.image.load(self.ground_from).convert_alpha(), [0, height - 69])

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			start_button.process()
			exit_button.process()
			optional_button.process()

			pygame.display.flip()
			pygame.display.update()


class Optional:
	def __init__(self):
		self.show_menu = None
		pygame.display.set_caption("Optional")

		self.player_form = {"frames_count": 6, "frames_name": "pica", "sound": "../sounds/jump_pikachu.mp3"}
		self.grass_form = '../graphics/environment/ground0.png'
		self.background_form = '../graphics/environment/background.png'

		self.font = pygame.font.Font('../graphics/font/VerberaC.ttf', 50)
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

	def display_text(self):
		if True:
			x = WINDOW_WIDTH / 2

			self.text_1 = "Whose side are you on?"
			y1 = WINDOW_HEIGHT / 20 - 15

			score_surf = self.font.render(self.text_1, True, 'red')
			score_rect = score_surf.get_rect(midtop=(x, y1))
			self.display_surface.blit(score_surf, score_rect)

			self.text_2 = "What kind of land do you want?"
			y2 = WINDOW_HEIGHT - 460

			score_surf = self.font.render(self.text_2, True, 'red')
			score_rect = score_surf.get_rect(midtop=(x, y2))
			self.display_surface.blit(score_surf, score_rect)

			self.text_3 = "Сhoose background for your game?"
			y3 = WINDOW_HEIGHT - 300

			score_surf = self.font.render(self.text_3, True, 'red')
			score_rect = score_surf.get_rect(midtop=(x, y3))
			self.display_surface.blit(score_surf, score_rect)

	def draw_optional(self):

		self.picachu_button = Button(100, 80, 200, 85, "Pikachu", self.set_pikachu_form)
		self.ghost_button = Button(400, 80, 200, 85, "Ghost", self.set_ghost_form)

		self.grass_button = Button(100, 245, 200, 85, "Grass", self.set_grass_form)
		self.grass2_button = Button(400, 245, 200, 85, "Ground", self.set_grass2_form)

		self.stars_button = Button(100, 410, 200, 85, "Stars", self.set_stars_form)
		self.forest_button = Button(400, 410, 200, 85, "Forest", self.set_forest_form)

		self.menu_button = Button(240, 530, 200, 85, "Menu", menu)

		while True:
			bg_image = pygame.image.load(self.background_form).convert()
			background_height = bg_image.get_height()
			scale_factor = WINDOW_HEIGHT / background_height
			full_height = bg_image.get_height() * scale_factor
			full_width = bg_image.get_width() * scale_factor
			full_sized_image = pygame.transform.scale(bg_image, (full_width, full_height))
			screen.blit(full_sized_image, (0, 0))

			screen.blit(pygame.image.load(self.grass_form).convert_alpha(), [0, height - 69])

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			self.display_text()

			self.menu_button.process()
			self.picachu_button.process()
			self.ghost_button.process()
			self.grass_button.process()
			self.grass2_button.process()
			self.stars_button.process()
			self.forest_button.process()

			pygame.display.flip()
			pygame.display.update()

	def set_pikachu_form(self):
		self.player_form = {"frames_count": 6, "frames_name": "pica", "sound": "../sounds/jump_pikachu.mp3"}

	def set_ghost_form(self):
		self.player_form = {"frames_count": 2, "frames_name": "ghost", "sound": "../sounds/jump2.mp3"}

	def set_grass_form(self):
		self.grass_form = '../graphics/environment/ground0.png'

	def set_grass2_form(self):
		self.grass_form = '../graphics/environment/ground.png'

	def set_stars_form(self):
		self.background_form = '../graphics/environment/background.png'

	def set_forest_form(self):
		self.background_form = '../graphics/environment/background3.jpg'

	def get_player_form(self):
		return self.player_form

	def get_grass_form(self):
		return self.grass_form

	def get_background_form(self):
		return self.background_form


class Game:
	def __init__(self, player_form, ground_form, background_form):
		# setup

		self.player_form = player_form
		self.ground_form = ground_form
		self.background_form = background_form

		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		pygame.display.set_caption('Fly-jump-die')
		self.clock = pygame.time.Clock()
		self.active = True
		self.max_scores = 0
		self.save_data = Save()

		# sprite
		self.all_sprites = pygame.sprite.Group()
		self.collision_sprites = pygame.sprite.Group()

		# scale_factor
		background_height = pygame.image.load(self.background_form).get_height()
		self.scale_factor = WINDOW_HEIGHT / background_height

		# sprite setup
		Background(self.all_sprites, self.scale_factor, self.background_form)
		Ground([self.all_sprites, self.collision_sprites], self.scale_factor, self.ground_form)
		self.player = Player(self.all_sprites,
							self.scale_factor / 2,
							self.player_form["frames_count"],
							self.player_form["frames_name"],
							self.player_form["sound"])

		# about timer
		self.obstacle_timer = pygame.USEREVENT + 1
		pygame.time.set_timer(self.obstacle_timer, 1000)

		# about text
		self.font = pygame.font.Font('../graphics/font/VerberaC.ttf', 60)
		self.score = 0
		self.start_offset = pygame.time.get_ticks()

		# about menu
		self.play_val = True
		self.menu_button = Button(200, 250, 300, 85, "menu", self.show_menu)
		self.restart_button = Button(200, 380, 300, 85, "restart", self.restart)

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
			x = WINDOW_WIDTH - 150
		else:
			y = 130
			x = WINDOW_WIDTH / 2
			y1 = 65

			score_surf1 = self.font.render(f'Your max score: ' + str(self.max_score), True, 'red')
			score_rect1 = score_surf1.get_rect(midtop=(x, y1))
			self.display_surface.blit(score_surf1, score_rect1)

		score_surf = self.font.render(f'Score: ' + str(self.score), True, 'red')
		score_rect = score_surf.get_rect(midtop=(x, y))
		self.display_surface.blit(score_surf, score_rect)

	def run(self):
		last_time = time.time()

		## изменение максимального счётчика
		#self.save_data.save('max', 0)

		while self.play_val:

			# delta time
			dt = time.time() - last_time
			last_time = time.time()

			# max score
			self.max_score = self.save_data.get('max')

			if self.score > self.max_score:
				self.max_score = self.score
				self.save_data.save('max', self.max_score)

			# event loop
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

					self.save_data.save()
					self.save_data.add('max', self.max_scores)

				if event.type == pygame.KEYDOWN:
					if self.active:
						self.player.jump()

					if not self.active:
						self.player = Player(self.all_sprites, self.scale_factor / 1.7,
											 self.player_form["frames_count"],
											 self.player_form["frames_name"],
											 self.player_form["sound"])
						self.active = True
						self.start_offset = pygame.time.get_ticks()

				if event.type == self.obstacle_timer and self.active:
					Obstacle([self.all_sprites, self.collision_sprites], self.scale_factor)

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
		print("res")
		game = Game(optional.get_player_form(), optional.get_grass_form(), optional.get_background_form())
		game.run()

	def show_menu(self):
		print("menu")
		time.sleep(0.2)
		self.play_val = False


optional = Optional()


def start():
	print("start")
	game = Game(optional.get_player_form(), optional.get_grass_form(), optional.get_background_form())
	game.run()


def exit_func():
	exit()


def optional_func():
	print("optional")
	optional.draw_optional()


def menu():
	menu = Menu(optional.get_grass_form(), optional.get_background_form())
	menu.draw_menu()


if __name__ == '__main__':
	optional = Optional()
	menu()
