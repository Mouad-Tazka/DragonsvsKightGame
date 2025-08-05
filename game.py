#Game Description:
#There will be one player against multiple enemies. The objective of the game will be to collect all
#the coins for that level to move to the next round. In doing so, there will be enemies moving
#towards the player. If the player happpens to touch the enemy, the player will lose a bar of health
#ach time (total bar health:4). If the player is able to collect all the coins, the player will move
#to the next round and the rounds will get increasingly difficult with more enemies/enemies moving
#faster.

#Basic Features:
#-User input: Keys will be used to move the player
#-Game over: When the player loses all their bars of health, the game will be over and the player
#position will reset [REVISED: When player loses all health, Game Over in red text will be presented.
#-The player will have an image of a knight, while the enemies will be images of dragons [MODIFIED: background of game is a castle path]

#Additional Features:
#-Restart from game over: When the player loses all bars of health, the game will present a screen
#with Game Over! The player will have the option to restart the game and start from round 1 [DELETED]
#Sprite Animation: The health bar will animate to a different index  each time the player hits the enemy
#-Enemies: There will be multiple and faster enemies each round [CHANGE]
#-Health bar: The player will have a total health bar of 4 and this will deplete every time it collides
#with an enemy
#Collectibles: gold coins have to be picked uo by the character to move to the next level [CHANGES]
#-Multiple levels: There will be multiple levels in the game. If the player obtains all the coins
#each round, the player will move up to the next level where it will be increasingly difficult


import uvage
import random

camera = uvage.Camera(800, 600)
background = uvage.from_image(400, 400, 'castle.jpeg') #added background of a medieval castle
background.scale_by(0.3)



player = uvage.from_image(0, 0, 'knight.png') #kept player character as a knight, also made it start at (0, 0)
player.size = [40, 40]

health_bar_image = uvage.load_sprite_sheet('health_bar.png', 4, 1) #added our health bar sprite sheet image, goes down after each enemy hit
healthbar = uvage.from_image(175, 565, health_bar_image[0])
healthbar.scale_by(0.085)



global count
count = 0

coins = [] # These are lists that store instances of coins and enemies. The reset_level function clears these lists and repopulates them when the player advances to a new level.
enemies = []
enemy_start_speed = 2 # These variables determine the initial speed of enemies and the increment in speed for each new level. The speed of enemies increases as the player progresses through levels.
enemy_speed_increment = 0.5
enemy_gap = 20 #These variables define the gap between enemies and the width and height of enemies
enemy_width = 40
enemy_height = 40
player_health = 4
collected_coins = 0 #These variables keep track of the player's health, the number of coins collected, and the current level
level = 1
game_on = True # This is used to control the game state. It is initially set to True, indicating that the game is active. When the player collides with an enemy, game_on is set to False, pausing the game until it is reset.

def create_enemy():
    enemy_gap_multiplier = 2
    enemy = uvage.from_image(
        random.randint(0, camera.width - enemy_width),
        -enemy_gap_multiplier * enemy_gap * len(enemies),
        "dragon.png", #made the enemies dragons
    )
    enemy.speedy = enemy_start_speed + (level - 1) * enemy_speed_increment #changed enemy speed to something more controlled and specific after each level
    enemies.append(enemy)
    enemy.size = [50, 50]

def lose_health(a):
    global count, game_on
    if game_on:
        if player.touches(a):
            enemies.remove(a)
            count += 1
            update_healthbar()

def update_healthbar(): #added to change health bar appearance after each hit with enemy
    global count
    if count == 1:
        healthbar.image = health_bar_image[1]
    elif count == 2:
        healthbar.image = health_bar_image[2]
    elif count == 3:
        healthbar.image = health_bar_image[3]

def reset_level():
    global collected_coins, level, player_health, game_on

    collected_coins = 0
    player_health = 4
    game_on = True

    player.center = [400, 300]

    coins.clear()
    enemies.clear()

    for c in range(3 + (level - 1) * 2):
        coin = uvage.from_image(random.randint(0, camera.width - 10), random.randint(0, camera.height - 10), "coin.png") #We made coins using an image of a coin in this code
        coins.append(coin) #adds coins after each level
        coin.size = [20, 20]

    for e in range(6 + (level - 1)):
        create_enemy() #creates new enemies after each level

    level += 1

def game_over():
    global collected_coins, level, player_health, game_on

    print("Game Over! You collided with an enemy.")


    game_on = False #Set game_on to False to stop the game

    game_over_text = uvage.from_text(400, 250, 'GAME OVER!', 75, 'red', bold=False) #added to present 'GAME OVER' text when the user loses

    camera.clear('black')
    camera.draw(game_over_text)
    camera.display()

    uvage.timer_loop(30, reset_level) #decreased frames per second

def tick():
    global collected_coins, player_health

    if uvage.is_pressing("up arrow"):
        player.move(0, -5)
    if uvage.is_pressing("down arrow"):
        player.move(0, 5)
    if uvage.is_pressing("left arrow"):
        player.move(-5, 0)
    if uvage.is_pressing("right arrow"):
        player.move(5, 0)

    if player.left < 0:
        player.left = 0
    if player.right > camera.width:
        player.right = camera.width
    if player.top < 0:
        player.top = 0
    if player.bottom > camera.height:
        player.bottom = camera.height

    for enemy in enemies:
        enemy.move(0, enemy.speedy)
        if enemy.top > camera.height:
            enemy.top = -enemy_height - enemy_gap
            enemy.left = random.randint(0, camera.width - enemy_width)

        if player.touches(enemy, -5, 0):
            player_health -= 1

            if player_health == 0:
                game_over()

            lose_health(enemy)

    for coin in coins:
        if player.touches(coin):
            coins.remove(coin)
            collected_coins += 1

    camera.clear("black")
    camera.draw(background)  #Background drawn in this code
    camera.draw(player)
    camera.draw(healthbar)
    for enemy in enemies:
        camera.draw(enemy)
    for coin in coins:
        camera.draw(coin)

    camera.draw("Coins: " + str(collected_coins), 20, "white", 650, 10)
    camera.draw("Level: " + str(level - 1), 20, "white", 650, 30)

    camera.display()

    if not coins and game_on:
        print("Level " + str(level - 1) + " Complete! Moving to the next level.")
        reset_level()

level = 1 #ensures it starts at level 1
reset_level()
uvage.timer_loop(30, tick)

