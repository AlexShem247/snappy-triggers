import pygame
import os
import sys
from random import randrange, random
from enemies import enemyValues
from menus import createText, startingScreen, countdown, endRoundScreen, \
    startingBossScreen, endBossScreen, playerHealthbar, bossHealthbar

def startGame(fps, volume, crosshairColor, pauseGame):
    """ Starts the single player gamemode """
        
    pygame.init()  # Initialises the pygame module
    pygame.font.init()
    
    # Define values
    DISPLAY_WIDTH, DISPLAY_HEIGHT = 1280, 720
    CROSSHAIR_WIDTH, CROSSHAIR_HEIGHT = 50, 50
    BLACK, DARK_GRAY, LIGHT_GRAY, WHITE = (0, 0, 0), (100, 100, 100), (204, 204, 204), (255, 255, 255)
    COLORS = {"blue": (0, 134, 217), "red": (255, 34, 0), "green": (10, 194, 62), "yellow": (242, 222, 0)}
    DARK_GREEN = (2, 122, 18)
    CENTER_TOLERANCE = 10
    EXCLAM_SPACING = 10
    SCROLL_EVENT = 1027
    MAX_AMMO = 10
    NO_LEVELS = 3
    GUN_POWER = 0.5
    
    score = 0
    x, y = pygame.mouse.get_pos()
    x1, y1 = x, y
    
    
    class Cursor(pygame.sprite.Sprite):
        """ Shows crosshair on screen """
        def __init__(self, sprite_image, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(sprite_image).convert_alpha()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect(center=(x, y))
    
        def moveBy(self, dx, dy):
            """ Moves cursor """
            self.rect.move_ip(dx, dy)
            
        def resetCursor(self, x, y):
            self.rect = self.image.get_rect(center=(x, y))
            
        def configColor(self, sprite_image):
            """ Changes image used for cursor """
            self.image = pygame.image.load(sprite_image).convert_alpha()
            self.mask = pygame.mask.from_surface(self.image)
              
            
    def createEnemy(enemyGrid, levelValues, levelEnemies, sprite_group, enemy_group, enemy_spawning, volume):
        """Creates an enemy"""
        enemyCoords = enemyGrid.pop(randrange(len(enemyGrid))) # Randomly takes out a pair of coordinates
        
        e = levelEnemies.pop(randrange(len(levelEnemies))) # Randomly takes out an enemy
        
        if levelValues["reverse"] and enemyCoords[0] == levelValues["loc"]["xEnd"]:
            reverse = True
        else:
            reverse = False
            
        enemy = levelValues["enemyClass"](e["name"], enemyCoords[0], enemyCoords[1], e["pAwarded"], e["bpAwarded"],
                                         e["spFrames"], e["shFrames"], volume, reverse, e["idFrames"], e["moveVal"])
            
        sprite_group.add(enemy)
        enemy_group.add(enemy)
        if enemy.SPAWNFRAMES > 0:
            enemy_spawning.append(enemy)
        return enemyGrid, levelEnemies, sprite_group, enemy_group, enemy_spawning
    
    
    def startRound(levelValues, round_no, score, fps, volume, crosshairColor, pauseGame):
        """ Creates sprites and starts level """
        # Define variables    
        enemyGrid = []
        enemy_spawning = []
        enemy_despawning = []
        ammo = 10
        x, y = pygame.mouse.get_pos()
        x1, y1 = x, y
        
        # Change Round Number
        pygame.display.set_caption(f"Snappy Triggers - Round {round_no+1}")
        
        # Create images
        bg = pygame.image.load(f"Images/{levelValues['bg']}.png")
        crosshair = pygame.image.load(f"Images/Crosshair_{crosshairColor}.png")
        
        if levelValues["extraBg"]:
            extraBg = pygame.image.load(f"Images/{levelValues['bg'] + '_Extra'}.png")
        else:
            extraBg = None
        
        # Create Sprite groups
        sprite_group = pygame.sprite.Group()
        sprite_group.add(cursor)
        
        cursor_group = pygame.sprite.GroupSingle()
        cursor_group.add(cursor)
        
        enemy_group = pygame.sprite.Group()
        shot_group = pygame.sprite.Group()
        
        enemiesHit = {levelValues["nEnemy"]["name"]: 0,
                  levelValues["bEnemy"]["name"]: 0,
                  levelValues["pEnemy"]["name"]: 0}
    
        # Create a list of enemies
        levelEnemies = [levelValues["nEnemy"] for _ in range(levelValues["nEnemy"]["quantity"])] + \
            [levelValues["bEnemy"] for _ in range(levelValues["bEnemy"]["quantity"])] + \
                [levelValues["pEnemy"] for _ in range(levelValues["pEnemy"]["quantity"])]
        
        # Spaces for enemies to spawn on
        for xPos in range(levelValues["loc"]["xStart"], levelValues["loc"]["xEnd"] + 1, levelValues["loc"]["xSpacing"]):
            for yPos in range(levelValues["loc"]["yStart"], levelValues["loc"]["yEnd"] + 1,
                              levelValues["loc"]["ySpacing"]):
                enemyGrid.append((xPos, yPos))
                 
        # Show starting screen
        startingScreen(levelValues["enemyType"],
    (levelValues["nEnemy"]["name"], levelValues["nEnemy"]["description"], levelValues["nEnemy"]["bonus_description"]),
    (levelValues["bEnemy"]["name"], levelValues["bEnemy"]["description"], levelValues["bEnemy"]["bonus_description"]),
    (levelValues["pEnemy"]["name"], levelValues["pEnemy"]["description"], levelValues["pEnemy"]["bonus_description"]),
    gameDisplay, round_no, clock, fps)
        
        countdown(bg, three, two, one, go, countSound1, countSound2, countSound3, gameDisplay, fps, clock)
    
        # Create enemies
        for x in range(levelValues["maxEnemies"]):
            enemyGrid, levelEnemies, sprite_group, enemy_group, enemy_spawning\
                = createEnemy(enemyGrid, levelValues, levelEnemies, sprite_group, enemy_group, enemy_spawning, volume)
            
        gameLoop = True
        endGame = False
        pausingGame = False
        gamePaused = False
        
        cursor.resetCursor(x, y)
        
        # Check for background music
        if levelValues["bgMusic"]:
            bgMusic = pygame.mixer.Sound(f"Audio\{levelValues['bgMusic']}.mp3")
            pygame.mixer.Sound.play(bgMusic)
            sounds.append(bgMusic)
        
        while gameLoop:
            pygame.mouse.set_visible(False) # Hide mouse cursor
            
            for event in pygame.event.get():
        
                if levelEnemies == [] and len(enemy_group) == 0 and len(shot_group) == 0:
                    # Close Game
                    gameLoop = False
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and ammo >= 1:
                    # Left mouse click
                    isEnemyShot = False
                    
                    # Ammo goes down by 1
                    ammo -= 1
                        
                    for enemy in enemy_group:
                        
                        if pygame.sprite.spritecollide(enemy, cursor_group, False,
                                                       collided=pygame.sprite.collide_mask):
                            # Enemy has been shot
                            isEnemyShot = True
                            score += enemy.pointsAwarded
                            enemiesHit[enemy.name] += enemy.pointsAwarded
                            
                            accuracy = (abs(enemy.rect[0] + enemy.rect[2]//2 - x1) + # On average, how many pixels
                                        abs(enemy.rect[1] + enemy.rect[3]//2 - y1))/2 # away from the center
                            
                            if accuracy <= CENTER_TOLERANCE:
                                # Award accuracy points
                                score += enemy.bonusPointsAwarded
                                enemiesHit[enemy.name] += enemy.bonusPointsAwarded
                            
                            enemy.shotSound()
                            enemy_group.remove(enemy)
                            
                            # Stop showning despawning animation if despawning
                            if enemy in enemy_despawning:
                                enemy_despawning.remove(enemy)
                                
                            shot_group.add(enemy)
                            enemyGrid.append((enemy.sX, enemy.sY))
                            
                            
                    if not isEnemyShot:
                        pygame.mixer.Sound.play(shot)
                
                if event.type == SCROLL_EVENT:
                    # Mouse scroll wheel
                    if event.y != 0 and ammo < MAX_AMMO:
                            ammo += 1 # Ammo increases
                            
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        # Pause Game
                        pausingGame = True
                        
                if gamePaused:
                    fps, volume, crosshairColor, endGame = pauseGame(fps, volume, crosshairColor)
                    pausingGame = False
                    gamePaused = False
                    cursor.configColor(f"Images/Cursor_{crosshairColor}.png")
                    crosshair = pygame.image.load(f"Images/Crosshair_{crosshairColor}.png")
                    
                    # Config volume
                    for sound in sounds:
                        sound.set_volume(volume)
                        
                    for enemy in enemy_group:
                        enemy.updatevolume(volume)
                            
                        
            # Main Code Here
            x1, y1 = pygame.mouse.get_pos()
            gameDisplay.blit(bg, (-x1, -y1//2))
                
            # Redraw sprites
            sprite_group.update()
            enemy_group.draw(gameDisplay)
            shot_group.draw(gameDisplay)
        
            cursor.moveBy(x1 - x, y1 - y)
            
            if extraBg:
                gameDisplay.blit(extraBg, (-x1, -y1//2))
            
            # Draw score
            scoreText = createText(f"Score: {score}", 70, COLORS[crosshairColor])
            gameDisplay.blit(scoreText, (10, DISPLAY_HEIGHT - scoreText.get_rect().height-20))
            
            # Move enemies
            eLeft, eRight, eUp, eDown = False, False, False, False
            for enemy in enemy_group:
                
                # If enemy off the screen, display !
                if enemy.rect[0] > DISPLAY_WIDTH and not eRight:
                    
                    # Enemy is to the right
                    eX, eY = DISPLAY_WIDTH - rightExclam.get_rect().size[0] - EXCLAM_SPACING, enemy.rect[1]
                    if eY > DISPLAY_HEIGHT - rightExclam.get_rect().size[1] - EXCLAM_SPACING:
                        eY = DISPLAY_HEIGHT - rightExclam.get_rect().size[1] - EXCLAM_SPACING
                    elif eY < EXCLAM_SPACING:
                        eY = EXCLAM_SPACING
                        
                    eRight = True
                    gameDisplay.blit(rightExclam, (eX, eY))
                    
                if (enemy.rect[0] + enemy.rect[2]) < 0 and not eLeft:
                    
                    # Enemy is to the left
                    eX, eY = EXCLAM_SPACING, enemy.rect[1]
                    if eY > DISPLAY_HEIGHT - leftExclam.get_rect().size[1] - EXCLAM_SPACING:
                        eY = DISPLAY_HEIGHT - leftExclam.get_rect().size[1] - EXCLAM_SPACING
                    elif eY < EXCLAM_SPACING:
                        eY = EXCLAM_SPACING
                        
                    eLeft = True
                    gameDisplay.blit(leftExclam, (eX, eY))
                    
                if enemy.rect[1] > DISPLAY_HEIGHT and not eDown:
                    # Enemy is below
                    eDown = True
                    gameDisplay.blit(downExclam, (enemy.rect[0],
                                                   DISPLAY_HEIGHT - rightExclam.get_rect().size[1]- EXCLAM_SPACING))
                if (enemy.rect[1] + enemy.rect[3]) < 0 and not eUp:
                    # Enemy is above
                    eUp = True
                    gameDisplay.blit(upExclam, (enemy.rect[0],
                                                   EXCLAM_SPACING))
                    
                enemy.moveBy(-x1, -y1//2)
                
                if enemy.IDFRAMES > 1:
                    enemy.idAnimation()
                    
                if enemy.moveVal:
                    if enemy.reverse:
                        enemy.move(-enemy.moveVal[0], enemy.moveVal[1])
                    else:
                        enemy.move(enemy.moveVal[0], enemy.moveVal[1])
                        
                # If enemy moved offscreen
                if enemy.x < levelValues["loc"]["xStart"] or enemy.x > levelValues["loc"]["xEnd"]:
                    enemy_group.remove(enemy)
                    enemyGrid.append((enemy.sX, enemy.sY))
                
                # Checks how long its been on the screen
                enemy.timer += 1
                if levelValues["enemyDuration"]:
                    if enemy.timer/fps >= levelValues["enemyDuration"] and enemy not in enemy_despawning and\
                        levelValues["despawn"]:
                        enemy_despawning.append(enemy)
                        enemy.frameNo = enemy.SPAWNFRAMES
                else:
                    if enemy not in enemy_despawning and levelValues["despawn"]:
                        enemy_despawning.append(enemy)
                        enemy.frameNo = enemy.SPAWNFRAMES
            
            # Show spawning animation
            for enemy in enemy_spawning:
                if enemy.frameNo < enemy.SPAWNFRAMES + 1:
                    enemy.spawnAnimation()
                else:
                    enemy.resetImage()
                    enemy_spawning.remove(enemy)
             
            # Showing shot animation
            for enemy in shot_group:
                if enemy.frameNo < enemy.SHOTFRAMES + 1:
                    enemy.shotAnimation()
                else:
                    shot_group.remove(enemy)
                    
            # Show despawn animation
            for enemy in enemy_despawning:
                if enemy.frameNo > 1:
                    enemy.despawnAnimation()
                else:
                    enemy_despawning.remove(enemy)
                    enemy_group.remove(enemy)
            
            # Display crosshair
            gameDisplay.blit(crosshair, (x - CROSSHAIR_WIDTH, y - CROSSHAIR_HEIGHT))
            ammoText = createText(str(int(ammo)), 50, COLORS[crosshairColor])
            gameDisplay.blit(ammoText, (x - ammoText.get_rect().width//2, y + CROSSHAIR_HEIGHT))
            
            # Check if more enemies need to be generated
            if len(enemy_group) < levelValues["maxEnemies"] and levelEnemies != []:
                
                # Average rate of spawn (s)= 1/levelValues["spRate"]/fps
                if random() < levelValues["spRate"]:
                    enemyGrid, levelEnemies, sprite_group, enemy_group, enemy_spawning\
                        = createEnemy(enemyGrid, levelValues, levelEnemies, sprite_group, \
                                      enemy_group, enemy_spawning, volume)
            
            # Check if window is paused
            if pausingGame:
                
                # Grey out screen
                transLayer = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
                transLayer.set_alpha(150)
                transLayer.fill(DARK_GRAY)
                gameDisplay.blit(transLayer, (0,0))
                
                # Add 'paused' text
                text = createText("Paused", 80, COLORS["red"])
                gameDisplay.blit(text, (DISPLAY_WIDTH//2 - text.get_width()//2, 10))
                
                pygame.mouse.set_visible(True) # Show mouse cursor
                gamePaused = True
            
            # Update window
            x, y = x1, y1
            pygame.display.update()
            clock.tick(fps)
            
            if endGame:
                # If user quit game
                pygame.quit()
        
        # Disable level music
        if levelValues["bgMusic"]:
            bgMusic.stop()
        
        endRoundScreen(enemiesHit, score, fps, gameDisplay, round_no, clock)
        
        return score, fps, volume, crosshairColor
    
    
    def startBossRound(levelValues, round_no, score, fps, volume, crosshairColor, pauseGame):
        """ Creates sprites and starts level """
        # Define variables    
        enemyGrid = []
        minionGrid = []
        ammo = 10
        health = 100
        bossDefeated = False
        timer = 1
        x, y = pygame.mouse.get_pos()
        x1, y1 = x, y
        
        # Change Round Number
        pygame.display.set_caption("Snappy Triggers - Final Round")
        
        # Create images
        bg = pygame.image.load(f"Images/{levelValues['bg']}.png")
        crosshair = pygame.image.load(f"Images/Crosshair_{crosshairColor}.png")
        
        # Create Sprite groups
        sprite_group = pygame.sprite.Group()
        sprite_group.add(cursor)
        
        cursor_group = pygame.sprite.GroupSingle()
        cursor_group.add(cursor)
        
        boss_group = pygame.sprite.GroupSingle()
        enemy_group = pygame.sprite.Group()
        shot_group = pygame.sprite.Group()
        shoot_group = pygame.sprite.Group()
        
        enemiesHit = {levelValues["bossship"]["name"]: 0,
                  levelValues["minion"]["name"]: 0}
                 
        # Show starting screen
        startingBossScreen(
    (levelValues["bossship"]["name"], levelValues["bossship"]["description"],
     levelValues["bossship"]["bonus_description"]),
    (levelValues["minion"]["name"], levelValues["minion"]["description"],
     levelValues["minion"]["bonus_description"]),
    gameDisplay, clock, fps)
        
        countdown(bg, three, two, one, go, countSound1, countSound2, countSound3, gameDisplay, fps, clock)
    
        gameLoop = True
        endGame = False
        pausingGame = False
        gamePaused = False
        
        # Create boss
        e = levelValues["bossship"]
        bossEnemy = e["enemyClass"](e["name"], e["spX"], e["spY"], e["pAwarded"], e["shFrames"], e["shootFrames"],
                                    e["moveVal"], e["health"], volume)
            
        sprite_group.add(bossEnemy)
        boss_group.add(bossEnemy)
        
        cursor.resetCursor(x, y)
        
        # Check for background music
        if levelValues["bgMusic"]:
            bgMusic = pygame.mixer.Sound(f"Audio\{levelValues['bgMusic']}.mp3")
            pygame.mixer.Sound.play(bgMusic)
            sounds.append(bgMusic)
            
        while gameLoop:
            pygame.mouse.set_visible(False) # Hide mouse cursor
            
            for event in pygame.event.get():
        
                if (len(boss_group) == 0 and len(enemy_group) == 0 and len(shot_group) == 0)\
                    or health <= 0:
                    # Close Game
                    gameLoop = False
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and ammo >= 1:
                    # Left mouse click
                    isEnemyShot = False
                    
                    # Ammo goes down by 1
                    ammo -= 1
                        
                    for enemy in enemy_group:
                        
                        if pygame.sprite.spritecollide(enemy, cursor_group, False,
                                                       collided=pygame.sprite.collide_mask):
                            # Enemy has been shot
                            isEnemyShot = True
                            score += enemy.pointsAwarded
                            enemiesHit[enemy.name] += enemy.pointsAwarded                      
                            
                            enemy.shotSound()
                            enemy_group.remove(enemy)
                                
                            shot_group.add(enemy)
                            
                            
                    if pygame.sprite.spritecollide(bossEnemy, cursor_group, False, 
                                                   collided=pygame.sprite.collide_mask):
                        # Boss has been shot
                        bossEnemy.health -= GUN_POWER
                        
                        if bossEnemy.health < 0:
                            # Boss has been killed
                            bossDefeated = True
                            boss_group.remove(bossEnemy)
                            shot_group.add(bossEnemy)
                            
                        else:
                            score += bossEnemy.pointsAwarded
                            enemiesHit[bossEnemy.name] += bossEnemy.pointsAwarded    
                            
                    if not isEnemyShot:
                        pygame.mixer.Sound.play(shot)
                
                if event.type == SCROLL_EVENT:
                    # Mouse scroll wheel
                    if event.y != 0 and ammo < MAX_AMMO:
                            ammo += 1 # Ammo increases
                            
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        # Pause Game
                        pausingGame = True
                        
                if gamePaused:
                    fps, volume, crosshairColor, endGame = pauseGame(fps, volume, crosshairColor)
                    pausingGame = False
                    gamePaused = False
                    cursor.configColor(f"Images/Cursor_{crosshairColor}.png")
                    crosshair = pygame.image.load(f"Images/Crosshair_{crosshairColor}.png")
                    
                    # Config volume
                    for sound in sounds:
                        sound.set_volume(volume)
                        
                    for enemy in enemy_group:
                        enemy.updatevolume(volume)
                                    
            # Main Code Here
            x1, y1 = pygame.mouse.get_pos()
            gameDisplay.blit(bg, (-x1, -y1//2))
                
            # Redraw sprites
            sprite_group.update()
            boss_group.draw(gameDisplay)
            enemy_group.draw(gameDisplay)
            shot_group.draw(gameDisplay)
        
            cursor.moveBy(x1 - x, y1 - y)
            
            # Draw score
            scoreText = createText(f"Score: {score}", 70, COLORS[crosshairColor])
            gameDisplay.blit(scoreText, (10, DISPLAY_HEIGHT - scoreText.get_rect().height-20))
            
            # Draw healthbar
            healthText = createText("Health:", 60, COLORS[crosshairColor])
            gameDisplay.blit(healthText, (10, DISPLAY_HEIGHT - scoreText.get_rect().height-75))
            playerHealthbar(gameDisplay, health, COLORS[crosshairColor])
            
            # Draw boss healthbar
            healthText = createText("Boss Health:", 35, DARK_GREEN)
            gameDisplay.blit(healthText, (10, 30))
            bossHealthbar(gameDisplay, bossEnemy.health)
            
            
            # Move boss depending on health
            if bossEnemy.y < levelValues["bossship"]["endY"]:
                bossEnemy.move(0, bossEnemy.moveVal*2)
                for enemy in enemy_group:
                    enemy.move(0, bossEnemy.moveVal*2)
            
            if 50 < bossEnemy.health <= 75:
                # Medium health
                if bossEnemy.x > levelValues["bossship"]["spX"] - levelValues["bossship"]["endX"]:
                    moveVal = -bossEnemy.moveVal
                else:
                    moveVal = 0
                    
                minionNo = 3
    
            elif 25 < bossEnemy.health <= 50:
                # Low Health
                if bossEnemy.x < levelValues["bossship"]["spX"] + levelValues["bossship"]["endX"]:
                    moveVal = bossEnemy.moveVal
                else:
                    moveVal = 0
                    
                minionNo = 4
                
            elif bossEnemy.health <= 25:
                # Very low health
                if bossEnemy.x > levelValues["bossship"]["spX"]:
                    moveVal = -bossEnemy.moveVal
                else:
                    moveVal = 0
                    
                minionNo = 5
            else:
                # High health
                moveVal = 0
                minionNo = 2
                
            bossEnemy.move(moveVal, 0)
            bossEnemy.moveBy(-x1, -y1//2)
            
            # Move enemies
            for enemy in enemy_group:
                enemy.move(moveVal, 0)
                enemy.moveBy(-x1, -y1//2)
            
            # Events
            if timer == fps*levelValues["spRate"] and bossEnemy.health > 5:
                # Boss spawn minions
                spCoords = [(bossEnemy.x - levelValues["bossship"]["w"], bossEnemy.y - levelValues["bossship"]["h"]),
                            (bossEnemy.x + levelValues["bossship"]["w"], bossEnemy.y - levelValues["bossship"]["h"]),
                            (bossEnemy.x - levelValues["bossship"]["w"], bossEnemy.y + levelValues["bossship"]["h"]),
                            (bossEnemy.x + levelValues["bossship"]["w"], bossEnemy.y + levelValues["bossship"]["h"]),
                            (bossEnemy.x, bossEnemy.y + 3*levelValues["bossship"]["h"])]
                
                for i in range(minionNo):
                
                    if i not in minionGrid:
                        e = levelValues["minion"]
                        enemy = e["enemyClass"](e["name"], spCoords[i][0], spCoords[i][1], e["pAwarded"],
                                                e["shFrames"], e["shootFrames"], e["moveVal"], volume, i)
                    
                        enemy_group.add(enemy)
                        minionGrid.append(i)
                        
            if timer % fps*levelValues["minion"]["shRate"] == 0:
                # Minions shoot laser
                for enemy in enemy_group:
                    shoot_group.add(enemy)
                
            if timer == fps*levelValues["bossship"]["shRate"]:
                # Boss shoot laser
                shoot_group.add(bossEnemy)
                timer = 1
                
            # Show shoot animation
            if bossEnemy in shoot_group:
                if bossEnemy.health > 5:
                    if bossEnemy.frameNo < bossEnemy.SHOOTFRAMES + 1:
                        bossEnemy.shoot()
                        
                        if bossEnemy.frameNo >= bossEnemy.shootStart:
                            health -= levelValues["bossship"]["strength"]
                        
                    else:
                        bossEnemy.image = pygame.image.load(bossEnemy.sprite_image)
                        bossEnemy.frameNo = 1
                        shoot_group.remove(bossEnemy)
                else:
                        bossEnemy.image = pygame.image.load(bossEnemy.sprite_image)
                        bossEnemy.frameNo = 1
                        shoot_group.remove(bossEnemy)
                    
            # Show shoot animation for minionship
            for enemy in shoot_group:
                if enemy.enemyType != "Boss":
                    health -= levelValues["minion"]["strength"]
                    
                    if enemy.frameNo < enemy.SHOOTFRAMES + 1:
                        enemy.shoot()
                    
                    else:
                        enemy.image = pygame.image.load(enemy.sprite_image)
                        enemy.frameNo = 1
                        shoot_group.remove(enemy)
                    
            
            # Showing shot animation
            for enemy in shot_group:
                enemy.moveBy(-x1, -y1//2)
                
                if enemy.frameNo < enemy.SHOTFRAMES + 1:
                    enemy.shotAnimation()
                else:
                    shot_group.remove(enemy)
                    if enemy.enemyType == "Minion":
                        minionGrid.remove(enemy.i)
                    
            # Display crosshair
            gameDisplay.blit(crosshair, (x - CROSSHAIR_WIDTH, y - CROSSHAIR_HEIGHT))
            ammoText = createText(str(int(ammo)), 50, COLORS[crosshairColor])
            gameDisplay.blit(ammoText, (x - ammoText.get_rect().width//2, y + CROSSHAIR_HEIGHT))
            
            # Check if window is paused
            if pausingGame:
                
                # Grey out screen
                transLayer = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
                transLayer.set_alpha(150)
                transLayer.fill(DARK_GRAY)
                gameDisplay.blit(transLayer, (0,0))
                
                # Add 'paused' text
                text = createText("Paused", 80, COLORS["red"])
                gameDisplay.blit(text, (DISPLAY_WIDTH//2 - text.get_width()//2, 10))
                
                pygame.mouse.set_visible(True) # Show mouse cursor
                gamePaused = True
            
            # Update window
            x, y = x1, y1
            timer += 1
            pygame.display.update()
            clock.tick(fps)
            
            if endGame:
                # If user quit game
                pygame.quit()
        
        # Disable level music
        if levelValues["bgMusic"]:
            bgMusic.stop()
            
        # Calculate bonus score
        
        healthPoints = int(health)*5
        if healthPoints < 0:
            healthPoints = 0
        score += healthPoints # Bonus points from health
        
        if bossDefeated:
            bossPoints = levelValues["bossship"]["bp"]
        else:
            bossPoints = 0
        
        score += bossPoints # Bonus points from killing the boss
        
        endBossScreen(enemiesHit, healthPoints, bossPoints, score, fps, gameDisplay, clock)
        
        return score, bossDefeated, fps, volume, crosshairColor
                
                
    # Create pygame window
    surface = pygame.HWSURFACE | pygame.DOUBLEBUF
    gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), surface)  # Creates a pygame surface object
    pygame.display.set_caption("Snappy Triggers - Round 1")  # Set a window title
    programIcon = pygame.image.load("images/logo.ico")
    pygame.display.set_icon(programIcon)
    
    clock = pygame.time.Clock()
    
    # Define images
    cursor = Cursor(f"Images/Cursor_{crosshairColor}.png", x, y)
    leftExclam = pygame.image.load("Images/Left_Exclam.png")
    rightExclam = pygame.image.load("Images/Right_Exclam.png")
    upExclam = pygame.image.load("Images/Up_Exclam.png")
    downExclam = pygame.image.load("Images/Down_Exclam.png")
    three = pygame.image.load("Images/3.png")
    two = pygame.image.load("Images/2.png")
    one = pygame.image.load("Images/1.png")
    go = pygame.image.load("Images/go.png")
    
    # Define sounds
    shot = pygame.mixer.Sound("Audio\Shot.mp3")
    countSound1 = pygame.mixer.Sound("Audio\Start_Round1.mp3")
    countSound2 = pygame.mixer.Sound("Audio\Start_Round2.mp3")
    countSound3 = pygame.mixer.Sound("Audio\Start_Round3.mp3")
    sounds = [shot, countSound1, countSound2, countSound3]
    
    ENEMY_VALUES = enemyValues()
    
    # =============================================================================
    # Game Starts
    # =============================================================================
    
    
    for round_no in range(NO_LEVELS):
        # Get values for the current level
        levelValues = ENEMY_VALUES[round_no]
    
        score, fps, volume, crosshairColor =\
            startRound(levelValues, round_no, score, fps, volume, crosshairColor, pauseGame)
    
    round_no = 3
    
    levelValues = ENEMY_VALUES[round_no]
    
    score, bossDefeated, fps, volume, crosshairColor =\
             startBossRound(levelValues, round_no, score, fps, volume, crosshairColor, pauseGame)
            
    pygame.quit()
    
    return score, bossDefeated, fps, volume, crosshairColor
