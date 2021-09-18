import pygame

# Define constants
DISPLAY_WIDTH, DISPLAY_HEIGHT = 1280, 720

class Enemy(pygame.sprite.Sprite):
    """ An enemy that the Player can shoot to Earn Points """
    def __init__(self, enemyType, x, y, pointsAwarded, bonusPointsAwarded,
                 spawnframes, shotframes, volume, reverse, idframes, moveVal):
        
        pygame.sprite.Sprite.__init__(self)
        self.sprite_image = "Images/" + enemyType + ".png"
        self.image = pygame.image.load(self.sprite_image).convert_alpha()
        
        if reverse:
            self.image = pygame.transform.flip(self.image, True, False)
            
        self.mask = pygame.mask.from_surface(self.image)
        self.x, self.y = x, y
        self.sX, self.sY = x, y
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.frameNo = 1
        self.SPAWNFRAMES, self.SHOTFRAMES, self.IDFRAMES = \
            spawnframes, shotframes, idframes # No. of frames per animations
        self.pointsAwarded = pointsAwarded
        self.bonusPointsAwarded = bonusPointsAwarded
        self.shotAudio = pygame.mixer.Sound(f"Audio\{enemyType}_Shot.mp3")
        self.shotAudio.set_volume(volume)
        self.enemyType = enemyType
        self.timer = 0
        self.name = enemyType
        self.moveVal = moveVal
        self.reverse = reverse
        
    def moveBy(self, dx, dy):
        self.rect = self.image.get_rect(center=(dx + self.x, dy + self.y))
        
    def updatevolume(self, volume):
        self.shotAudio.set_volume(volume)
        
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.rect = self.image.get_rect(center=(self.x, self.y))
        
        
class Target(Enemy):
    """ Target Enemies """
    def shotAnimation(self):
        self.image = pygame.image.load(f"Images\{self.enemyType}_Break{int(self.frameNo//1)}.png")
        self.frameNo += 0.5
        
    def spawnAnimation(self):
        self.image = pygame.image.load(f"Images\{self.enemyType}_{int(self.frameNo//1)}.png")
        self.mask = pygame.mask.from_surface(self.image)
        self.frameNo += 0.5
    
    def resetImage(self):
        self.image = pygame.image.load(self.sprite_image)
        self.frameNo = 1
        
    def shotSound(self):
        pygame.mixer.Sound.play(self.shotAudio)
        
    def despawnAnimation(self):
        self.image = pygame.image.load(f"Images\{self.enemyType}_{int(self.frameNo//1)}.png")
        self.image = pygame.transform.flip(self.image, True, False)
        self.mask = pygame.mask.from_surface(self.image)
        self.frameNo -= 0.5
        

class Bird(Enemy):
    """ Class for flying vehicles and birds """
    def shotAnimation(self):
        self.image = pygame.image.load(f"Images\{self.enemyType}_Break1.png")
        if self.reverse:
            self.image = pygame.transform.flip(self.image, True, False)
        self.move(0, ((DISPLAY_HEIGHT*2 - self.y - 500)//(self.SHOTFRAMES/self.frameNo)))
        self.frameNo += 0.25
        
    def shotSound(self):
        pygame.mixer.Sound.play(self.shotAudio)
        
    def idAnimation(self):
        self.image = pygame.image.load(f"Images\{self.enemyType}_{int(self.frameNo//1)}.png")
        if self.reverse:
            self.image = pygame.transform.flip(self.image, True, False)
            
        self.frameNo += 0.25
        
        if self.frameNo > self.IDFRAMES:
            self.frameNo = 1
            
            
class Spaceship(Enemy):
    """ Class for space vehicles """
    def shotAnimation(self):
        self.image = pygame.image.load(f"Images\{self.enemyType}_Break1.png")
        if self.reverse:
            self.image = pygame.transform.flip(self.image, True, False)
        self.frameNo += 0.25
        
    def shotSound(self):
        pygame.mixer.Sound.play(self.shotAudio)
        
        
class BossShip(pygame.sprite.Sprite):
    """ Boss Enemy that contains a health bar and can summon enemy ships """
    def __init__(self, enemyType, x, y, pointsAwarded, shFrames, shootFrames, moveVal, health, volume):
        pygame.sprite.Sprite.__init__(self)
        self.sprite_image = "Images/" + enemyType + ".png"
        self.image = pygame.image.load(self.sprite_image).convert_alpha() 
        self.mask = pygame.mask.from_surface(self.image)
        self.x, self.y = x, y
        self.enemyType = enemyType
        self.SHOTFRAMES, self.SHOOTFRAMES = shFrames, shootFrames
        self.moveVal = moveVal
        self.frameNo = 1
        self.shootStart = 20
        self.health = health
        self.pointsAwarded = pointsAwarded
        self.name = enemyType
        self.rect = self.image.get_rect(center=(self.x, self.y))
        
        self.shotAudio = pygame.mixer.Sound(f"Audio\{enemyType}_Shot.mp3")
        self.shotAudio.set_volume(volume)
        self.shootAudio1 = pygame.mixer.Sound(f"Audio\{enemyType}_Shoot1.mp3")
        self.shootAudio1.set_volume(volume)
        self.shootAudio2 = pygame.mixer.Sound(f"Audio\{enemyType}_Shoot2.mp3")
        self.shootAudio2.set_volume(volume)
        
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.rect = self.image.get_rect(center=(self.x, self.y))
        
    def moveBy(self, dx, dy):
        self.rect = self.image.get_rect(center=(dx + self.x, dy + self.y))
        
    def shoot(self):
        if self.frameNo == 1:
            pygame.mixer.Sound.play(self.shootAudio1)
            
        if self.frameNo == self.shootStart:
            pygame.mixer.Sound.play(self.shootAudio2)
        elif self.frameNo > self.shootStart:
            self.image = pygame.image.load(f"Images\{self.enemyType}_Shoot.png")
        self.frameNo += 0.5
            
    def updatevolume(self, volume):
        self.shotAudio.set_volume(volume)
        self.shootAudio1.set_volume(volume)
        self.shootAudio2.set_volume(volume)
        
    def shotAnimation(self):
        if self.frameNo == 1:
            pygame.mixer.Sound.play(self.shotAudio)
        self.image = pygame.image.load(f"Images\{self.enemyType}_Break{int(self.frameNo//1)}.png")
        self.frameNo += 0.2
            
            
class MinionShip(pygame.sprite.Sprite):
    """ Spaceships that can be summoned by BossShip """
    def __init__(self, enemyType, x, y, pointsAwarded, shFrames, shootFrames, moveVal, volume, i):
        pygame.sprite.Sprite.__init__(self)
        self.sprite_image = "Images/" + enemyType + ".png"
        self.image = pygame.image.load(self.sprite_image).convert_alpha() 
        self.mask = pygame.mask.from_surface(self.image)
        self.x, self.y = x, y
        self.i = i
        self.enemyType = enemyType
        self.frameNo = 1
        self.pointsAwarded = pointsAwarded
        self.SHOTFRAMES = shFrames
        self.SHOOTFRAMES = shootFrames
        self.name = enemyType
        self.rect = self.image.get_rect(center=(self.x, self.y))
        
        self.shotAudio = pygame.mixer.Sound(f"Audio\{enemyType}_Shot.mp3")
        self.shotAudio.set_volume(volume)
        self.shootAudio = pygame.mixer.Sound(f"Audio\{enemyType}_Shoot.mp3")
        self.shootAudio.set_volume(volume)
        
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.rect = self.image.get_rect(center=(self.x, self.y))
        
    def moveBy(self, dx, dy):
        self.rect = self.image.get_rect(center=(dx + self.x, dy + self.y))
        
    def shoot(self):
        if self.frameNo == 1:
            pygame.mixer.Sound.play(self.shootAudio)
            
        self.image = pygame.image.load(f"Images\{self.enemyType}_Shoot.png")
        self.frameNo += 1
            
    def updatevolume(self, volume):
        self.shotAudio.set_volume(volume)
        self.shootAudio.set_volume(volume)
        
    def shotSound(self):
        pygame.mixer.Sound.play(self.shotAudio)
        
    def shotAnimation(self):
        self.image = pygame.image.load(f"Images\{self.enemyType}_Break1.png")
        self.frameNo += 0.5
    
    
def enemyValues():
    """ Values for creating enemies in levels """
    return [
    # Round 1
    {"nEnemy": {"name": "Target", "pAwarded": 10, "bpAwarded": 10,
                "spFrames": 5, "shFrames": 3, "quantity": 30,
                "idFrames": 1, "moveVal": None,
                "description": "Normal Targets are worth 10 points",
                "bonus_description": "(20 if hit in the centre)"}, # Normal target
     
     "bEnemy": {"name": "Gold_Target", "pAwarded": 50, "bpAwarded": 10,
                "spFrames": 5, "shFrames": 3, "quantity": 10,
                "idFrames": 1, "moveVal": None,
                "description": "Gold Targets are worth 50 points",
                "bonus_description": "(60 if hit in the centre)"}, # Bonus target
     
     "pEnemy": {"name": "Penalty_Target", "pAwarded": -30, "bpAwarded": 0,
                "spFrames": 5, "shFrames": 3, "quantity": 10,
                "idFrames": 1, "moveVal": None,
                "description": "Purple Targets will take away 30 points",
                "bonus_description": None}, # Penalty target
     
     "loc": {"xStart": 150, "xEnd": 2350, "yStart": 100, "yEnd": 900, "xSpacing": 200, "ySpacing": 200},
     "bg": "Range_BG", "enemyClass": Target, "enemyDuration": 3, "maxEnemies": 5, "spRate": 0.1,
     "enemyType": "targets", "despawn": True, "extraBg": False, "bgMusic": None, "reverse": False},
    
    # Round 2
    {"nEnemy": {"name": "Pigeon", "pAwarded": 20, "bpAwarded": 0,
                "spFrames": 0, "shFrames": 60, "quantity": 30,
                "idFrames": 5, "moveVal": (10, 0),
                "description": "Pigeons are worth 20 points",
                "bonus_description": None}, # Pigeon
     
     "bEnemy": {"name": "Blue_Bird", "pAwarded": 75, "bpAwarded": 0,
                "spFrames": 0, "shFrames": 60, "quantity": 10,
                "idFrames": 4, "moveVal": (15, 0),
                "description": "Blue Birds are worth 75 points",
                "bonus_description": None}, # Blue Bird
     
     "pEnemy": {"name": "Biplane", "pAwarded": -100, "bpAwarded": 0,
                "spFrames": 0, "shFrames": 60, "quantity": 10,
                "idFrames": 1, "moveVal": (10, 0),
                "description": "Shooting planes will take away 100 points",
                "bonus_description": None}, # Biplane
     
     "loc": {"xStart": 0, "xEnd": 1500, "yStart": 50, "yEnd": 450, "xSpacing": 1500, "ySpacing": 80},
     "bg": "Grass_BG", "enemyClass": Bird, "enemyDuration": None, "maxEnemies": 5, "spRate": 0.1,
     "enemyType": "birds", "despawn": False, "extraBg": True, "bgMusic": "Bird_Sounds", "reverse": True},
    
    # Round 3
    {"nEnemy": {"name": "Spaceship", "pAwarded": 30, "bpAwarded": 0,
                "spFrames": 0, "shFrames": 10, "quantity": 20,
                "idFrames": 0, "moveVal": (15, 0),
                "description": "Spaceships are worth 30 points",
                "bonus_description": None}, # Spaceship
     
     "bEnemy": {"name": "Rocket", "pAwarded": 50, "bpAwarded": 0,
                "spFrames": 0, "shFrames": 10, "quantity": 20,
                "idFrames": 0, "moveVal": (15, 0),
                "description": "Rockets are worth 50 points",
                "bonus_description": None}, # Rocket
     
     "pEnemy": {"name": "UFO", "pAwarded": 200, "bpAwarded": 0,
                "spFrames": 0, "shFrames": 10, "quantity": 5,
                "idFrames": 0, "moveVal": (30, 0),
                "description": "UFOs are worth 200 points",
                "bonus_description": None}, # Biplane
     
     "loc": {"xStart": 0, "xEnd": 1500, "yStart": 50, "yEnd": 450, "xSpacing": 1500, "ySpacing": 80},
     "bg": "Space_BG", "enemyClass": Spaceship, "enemyDuration": None, "maxEnemies": 5, "spRate": 0.1,
     "enemyType": "space vehicles", "despawn": False, "extraBg": False, "bgMusic": "Space_Music", "reverse": True},
    
    # Boss battle
    {"bossship": {"name": "Boss", "pAwarded": 2, "bpAwarded": 0,
              "shootFrames": 45, "shFrames": 14, "enemyClass": BossShip,
              "idFrames": 0, "moveVal": 1, "health": 100, "shRate": 8,
              "bp": 300, "spX": 1200, "spY": -300, "endX": 400, "endY": 400,
              "strength": 0.35, "w": 400, "h": 100,
              "description": "The Boss's healthbar will be displayed above",
              "bonus_description": "Attacks are powerful, but are slow to recharge"}, # Boss ship
     
     "minion": {"name": "Minion", "pAwarded": 10, "bpAwarded": 0,
              "shootFrames": 20, "shFrames": 10, "enemyClass": MinionShip,
              "idFrames": 0, "moveVal": 10, "health": 1, "shRate": 4, "strength": 0.05,
              "description": "The Bossship will summon smaller",
              "bonus_description": "spaceships to attack you"}, # Minions
     "bg": "Space_BG", "enemyDuration": None, "maxEnemies": 3, "spRate": 5,
     "despawn": False, "extraBg": False, "bgMusic": "Space_Music"}
    ]