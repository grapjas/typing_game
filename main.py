import pygame
import random

##### not sure where to put this 
wordList = []

with open("assets/gemeentes.txt") as f_obj:
	for line in f_obj:
		line = line.lower().strip()
		wordList.append(line)
######


# --- constants --- (UPPER_CASE names)

WIDTH = 960
HEIGHT = 720

BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

FPS = 30

# --- classes ---

class Word(object):

	def __init__(self, screen):
		self.screen = screen
		self.screen_rect = screen.get_rect()

		self.w_font = pygame.font.SysFont("arial", 25)
		self.word_text = get_random_word()
		self.text = self.w_font.render(self.word_text, True, BLACK)

		self.rect = self.text.get_rect()
		self.rect.x = 0
		self.rect.y = random.randint(50, HEIGHT-20)

		self.dist_x = 3 # speed
		self.dist_y = 0

	def update(self):
		if self.rect.left <= self.screen_rect.right:
			self.rect.x += self.dist_x
			self.rect.y += self.dist_y
		else:
			self.delete()	# also in main loop?

	def draw(self, screen):
		screen.blit(self.text, self.rect)
	
	def delete(self):
		pass

# --- functions --- (lower_case names)
# WIDTH = 960
# HEIGHT = 720

def check_word(words, typed):
	for wordx in words:
		if wordx.word_text == typed:
			words.remove(wordx)
			return True 
		else:
			return False

def life_text(screen, life, font):
	text = font.render(f"Lifes: {life}", True, WHITE, BLACK)

	text_rect = text.get_rect()
	text_rect.topleft = (15, 5)

	screen.blit(text, text_rect)

def word_text(screen, typed, font):
	text = font.render(typed, True, GREEN, BLACK)

	text_rect = text.get_rect()
	text_rect.topleft = (int(WIDTH/2), 5)

	screen.blit(text, text_rect)

def get_random_word():
	return random.choice(wordList)

def draw_bottom_bar(screen):
	pygame.draw.rect(screen,WHITE,(0,670,WIDTH,50))


# --- main --- (lower_case names)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen_rect = screen.get_rect()

# - objects -

# background

map_img = pygame.image.load("assets/background.jpg")

# - other -
lifes = 50

font = pygame.font.SysFont("arial", 20)
clock = pygame.time.Clock()
words = []
timeRunning_ms = 0
wordSpawn_ms = 0
word_cnt = 0
correct_cnt = 0
typed = ''

# - mainloop -

running = True

while running:
	
	if (wordSpawn_ms >= 1500):
		words.append(Word(screen))
		wordSpawn_ms = 0
		word_cnt += 1

	# - events -

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			#print(f"words list length: {len(words)}")
			print(f"cnt: {word_cnt}")
			print(f"correct_cnt: {correct_cnt}")

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN:
				for wordx in words:
					if wordx.word_text == typed:
						words.remove(wordx)
						correct_cnt += 1
				typed = ''
			elif event.key == pygame.K_BACKSPACE:
				typed = typed[:-1]
			else:
				typed += chr(event.key) 
	# - updates -

	for wordx in words:
		wordx.update()
		if wordx.rect.left >= screen_rect.right:
			lifes -= 1
			words.remove(wordx)

	# - draws -
	# background
	screen.blit(map_img, (0,0))

	# other
	for wordx in words:
		wordx.draw(screen)
	
	life_text(screen, lifes, font)
	word_text(screen, typed, font)


	pygame.display.update()
	# - FPS -

	tmp = clock.tick(FPS)
	wordSpawn_ms += tmp 
	timeRunning_ms += tmp
	tmp = 0

pygame.quit()