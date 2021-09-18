import pygame
import tkinter as tk

# Define constants
DISPLAY_WIDTH, DISPLAY_HEIGHT = 1280, 720
BLACK, DARK_GRAY, LIGHT_GRAY, WHITE = (0, 0, 0), (100, 100, 100), (204, 204, 204), (255, 255, 255)
DARK_GREEN = (2, 122, 18)

def createText(text, size, color):
    """ Creates a pygame font object and returns pygame text object """
    font = pygame.font.SysFont(None, size)
    textObject = font.render(text, True, color)
    
    return textObject

def startingScreen(shootTarget, enemy1, enemy2, enemy3, gameDisplay, round_no, clock, fps):
    """ Displays starting screen """
    startLoop = True
    pygame.mouse.set_visible(True)

    while startLoop:
        for event in pygame.event.get():
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    startLoop = False
                    
        gameDisplay.fill(BLACK)
        
        
        # Display images in window
        image = pygame.image.load("Images/" + enemy1[0] + ".png")
        gameDisplay.blit(image, (DISPLAY_WIDTH//4 - image.get_width()//2-100, 250))
        
        image = pygame.image.load("Images/" + enemy2[0] + ".png")
        gameDisplay.blit(image, (DISPLAY_WIDTH//2 - image.get_width()//2, 250))
        
        subTextHeight = 250 + image.get_height() + 50
        
        image = pygame.image.load("Images/" + enemy3[0] + ".png")
        gameDisplay.blit(image, ((DISPLAY_WIDTH//4)*3 - image.get_width()//2+100, 250))
                    
        
        # Draw text in window
        text = createText(f"Round {round_no + 1}", 100, WHITE)
        gameDisplay.blit(text, (DISPLAY_WIDTH//2 - text.get_width()//2, 20))
        
        text = createText(f"Shoot the {shootTarget} to gain Points", 60, LIGHT_GRAY)
        gameDisplay.blit(text, (DISPLAY_WIDTH//2 - text.get_width()//2, 120))
        
        text = createText("Press SPACE to Start", 80, WHITE)
        gameDisplay.blit(text, (DISPLAY_WIDTH//2 - text.get_width()//2, 600))
        
        text = createText(enemy1[1], 30, WHITE)
        gameDisplay.blit(text, (DISPLAY_WIDTH//4 - text.get_width()//2-100, subTextHeight))
        
        if enemy1[2]:
            text = createText(enemy1[2], 30, WHITE)
            gameDisplay.blit(text, (DISPLAY_WIDTH//4 - text.get_width()//2-100, subTextHeight + 50))
        
        text = createText(enemy2[1], 30, WHITE)
        gameDisplay.blit(text, (DISPLAY_WIDTH//2 - text.get_width()//2, subTextHeight))
        
        if enemy2[2]:
            text = createText(enemy2[2], 30, WHITE)
            gameDisplay.blit(text, (DISPLAY_WIDTH//2 - text.get_width()//2, subTextHeight + 50))
        
        text = createText(enemy3[1], 30, WHITE)
        gameDisplay.blit(text, ((DISPLAY_WIDTH//4)*3 - text.get_width()//2+100, subTextHeight))
        
        if enemy3[2]:
            text = createText(enemy3[2], 30, WHITE)
            gameDisplay.blit(text, ((DISPLAY_WIDTH//4)*3 - text.get_width()//2+100, subTextHeight + 50))
                    
        pygame.display.update()
        clock.tick(fps)
        
        
def countdown(bg, three, two, one, go, countSound1, countSound2, countSound3, gameDisplay, fps, clock):
    """ Displays three second countdown on screen"""
    countLoop = True
    timer = 1
    cX, cY = DISPLAY_WIDTH//2 - three.get_width()//2, DISPLAY_HEIGHT//2 - three.get_height()//2
    
    gameDisplay.blit(bg, (-DISPLAY_WIDTH//2, -DISPLAY_HEIGHT//4))
        
    gameDisplay.blit(three, (cX, cY))
    pygame.mixer.Sound.play(countSound1)


    while countLoop:
        pygame.event.get()
                          
        # Draw text in window      
        if timer == fps:
            gameDisplay.blit(bg, (-DISPLAY_WIDTH//2, -DISPLAY_HEIGHT//4))
            gameDisplay.blit(two, (cX, cY))
            pygame.mixer.Sound.play(countSound1)
            
        elif timer == fps*2:
            gameDisplay.blit(bg, (-DISPLAY_WIDTH//2, -DISPLAY_HEIGHT//4))
            gameDisplay.blit(one, (cX, cY))
            pygame.mixer.Sound.play(countSound2)
            
        elif timer == fps*3:
            gameDisplay.blit(bg, (-DISPLAY_WIDTH//2, -DISPLAY_HEIGHT//4))
            gameDisplay.blit(go, (DISPLAY_WIDTH//2 - go.get_width()//2, DISPLAY_HEIGHT//2 - go.get_height()//2))
            pygame.mixer.Sound.play(countSound3)
            
        elif timer == fps*4:
            pygame.mixer.Sound.stop(countSound3)
            countLoop = False
        
        
        timer += 1
                    
        pygame.display.update()
        clock.tick(fps)
        
    
def endRoundScreen(enemiesHit, score, fps, gameDisplay, round_no, clock):
    """ Displays end of round screen """
    startLoop = True
    pygame.mouse.set_visible(True)

    while startLoop:
        for event in pygame.event.get():
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    startLoop = False
        
        gameDisplay.fill(BLACK)
                    
        # Draw text in window
        text = createText(f"End of Round {round_no + 1}", 60, LIGHT_GRAY)
        gameDisplay.blit(text, (DISPLAY_WIDTH//2 - text.get_width()//2, 20))
        
        text = createText("Round Summary", 100, WHITE)
        gameDisplay.blit(text, (DISPLAY_WIDTH//2 - text.get_width()//2, 120))
        
        text = createText("Press SPACE to Continue", 80, WHITE)
        gameDisplay.blit(text, (DISPLAY_WIDTH//2 - text.get_width()//2, 600))
        
        enemyNames = list(enemiesHit.keys())
        
        text = createText(f"{enemyNames[0].replace('_', ' ')+'s'}:        {enemiesHit[enemyNames[0]]}",
                          50, LIGHT_GRAY)
        gameDisplay.blit(text, (DISPLAY_WIDTH//2 - text.get_width() + 100, 250))
                         
        text = createText(f"{enemyNames[1].replace('_', ' ')+'s'}:        {enemiesHit[enemyNames[1]]}",
                          50, LIGHT_GRAY)
        gameDisplay.blit(text, (DISPLAY_WIDTH//2 - text.get_width() + 100, 320))
                         
        text = createText(f"{enemyNames[2].replace('_', ' ')+'s'}:        {enemiesHit[enemyNames[2]]}",
                          50, LIGHT_GRAY)
        gameDisplay.blit(text, (DISPLAY_WIDTH//2 - text.get_width() + 100, 390))
                         
        text = createText(f"Total Score:        {score}", 50, WHITE)
        gameDisplay.blit(text, (DISPLAY_WIDTH//2 - text.get_width() + 100, 480))
                    
        pygame.display.update()
        clock.tick(fps)
        
        
def startingBossScreen(enemy1, enemy2, gameDisplay, clock, fps):
    """ Displays starting screen """
    startLoop = True
    pygame.mouse.set_visible(True)

    while startLoop:
        for event in pygame.event.get():
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    startLoop = False
                    
        gameDisplay.fill(BLACK)
        
        
        # Display images in window
        image1 = pygame.image.load("Images/" + enemy1[0] + ".png")
        image1 = pygame.transform.scale(image1, (412, 300))
        gameDisplay.blit(image1, (DISPLAY_WIDTH//3 - image1.get_width()//2 - 50, 150))
        
        subTextHeight = 180 + image1.get_height()
        
        image2 = pygame.image.load("Images/" + enemy2[0] + ".png")
        gameDisplay.blit(image2, ((DISPLAY_WIDTH//3)*2 - image2.get_width()//2 + 50,
                                  150 + image1.get_height()//2))
                          
        # Draw text in window
        text = createText("Final Round", 100, WHITE)
        gameDisplay.blit(text, (DISPLAY_WIDTH//2 - text.get_width()//2, 20))
        
        text = createText("Defeat the Boss to gain points", 60, LIGHT_GRAY)
        gameDisplay.blit(text, (DISPLAY_WIDTH//2 - text.get_width()//2, 100))
        
        text = createText("If you run out of Health, the level will end", 40, LIGHT_GRAY)
        gameDisplay.blit(text, (DISPLAY_WIDTH//2 - text.get_width()//2, 600))
        
        text = createText("Press SPACE to Start", 80, WHITE)
        gameDisplay.blit(text, (DISPLAY_WIDTH//2 - text.get_width()//2, 650))
        
        text = createText(enemy1[1], 30, WHITE)
        gameDisplay.blit(text, (DISPLAY_WIDTH//3 - text.get_width()//2 - 50, subTextHeight))
        
        text = createText(enemy1[2], 30, WHITE)
        gameDisplay.blit(text, (DISPLAY_WIDTH//3 - text.get_width()//2 - 50, subTextHeight + 50))
        
        text = createText(enemy2[1], 30, WHITE)
        gameDisplay.blit(text, ((DISPLAY_WIDTH//3)*2 - text.get_width()//2 + 50, subTextHeight))
        
        text = createText(enemy2[2], 30, WHITE)
        gameDisplay.blit(text, ((DISPLAY_WIDTH//3)*2 - text.get_width()//2 + 50, subTextHeight + 50))
        
                    
        pygame.display.update()
        clock.tick(fps)
        
        
def endBossScreen(enemiesHit, healthPoints, bossPoints, score, fps, gameDisplay, clock):
    """ Displays end of boss round screen """
    startLoop = True
    pygame.mouse.set_visible(True)

    while startLoop:
        for event in pygame.event.get():
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    startLoop = False
        
        gameDisplay.fill(BLACK)
                    
        # Draw text in window
        text = createText(f"End of Boss Round", 60, LIGHT_GRAY)
        gameDisplay.blit(text, (DISPLAY_WIDTH//2 - text.get_width()//2, 20))
        
        text = createText("Round Summary", 100, WHITE)
        gameDisplay.blit(text, (DISPLAY_WIDTH//2 - text.get_width()//2, 120))
        
        text = createText("Press SPACE to Continue", 80, WHITE)
        gameDisplay.blit(text, (DISPLAY_WIDTH//2 - text.get_width()//2, 610))
        
        enemyNames = list(enemiesHit.keys())
        
        text = createText(f"Points from Bossship:        {enemiesHit[enemyNames[0]]}",
                          50, LIGHT_GRAY)
        gameDisplay.blit(text, (DISPLAY_WIDTH//2 - text.get_width() + 100, 250))
                         
        text = createText(f"Points from Spaceships:        {enemiesHit[enemyNames[1]]}",
                          50, LIGHT_GRAY)
        gameDisplay.blit(text, (DISPLAY_WIDTH//2 - text.get_width() + 100, 310))
                         
        text = createText(f"Health bonus:        {healthPoints}",
                          50, LIGHT_GRAY)
        gameDisplay.blit(text, (DISPLAY_WIDTH//2 - text.get_width() + 100, 400))
        
        text = createText(f"Boss defeated bonus:        {bossPoints}",
                          50, LIGHT_GRAY)
        gameDisplay.blit(text, (DISPLAY_WIDTH//2 - text.get_width() + 100, 460))
                         
        text = createText(f"Total Score:        {score}", 50, WHITE)
        gameDisplay.blit(text, (DISPLAY_WIDTH//2 - text.get_width() + 100, 540))
                    
        pygame.display.update()
        clock.tick(fps)
        
        
def playerHealthbar(gameDisplay, health, color):
    """ Draws a healthbar using the player's current health """
    x, y = 175, 600
    h, w = 35, health*10
    t = 3
    if health > 0:
        pygame.draw.polygon(gameDisplay, LIGHT_GRAY, ((x, y), (x + w, y), (x + w, y + h), (x, y + h)))
        pygame.draw.polygon(gameDisplay, color, ((x, y + t), (x + w, y + t), (x + w, y - t + h), (x, y - t + h)))
        
def bossHealthbar(gameDisplay, health):
    """ Draws a healthbar using the boss's current health """
    x, y = 175, 25
    h, w = 35, health*10
    if health == 0:
        w = 1
    t = 3
    if health >= 0:
        pygame.draw.polygon(gameDisplay, LIGHT_GRAY, ((x, y), (x + w, y), (x + w, y + h), (x, y + h)))
        pygame.draw.polygon(gameDisplay, DARK_GREEN, ((x, y + t), (x + w, y + t),
                                                       (x + w, y - t + h), (x, y - t + h)))
        
    