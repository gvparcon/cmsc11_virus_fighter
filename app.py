import os
from ursina import *

# Uncomment to test game without main menu
# app = Ursina()
# Initializations of Entities to be Used
window.fullscreen = True
a = Audio('/sound_effects/game_bgm.mp3/', pitch=1,
          loop=True, autoplay=True, volume=0.3)
print(a)
player = Entity(model='quad', texture='assets\player',
                collider='box', y=5, scale=3)
bg = Entity(model='quad', texture='assets\BG', scale=36, z=1)
target = Entity(model='cube', texture='assets\\target1',
                collider='box', scale=3, x=20, y=-10)


# Update and input set to an empty entity for it to be called automatically and continuously
e = Entity()

# Initialization of reading text file
HIGH_SCORE_FILE = "high_score.txt"
if not os.path.isfile(HIGH_SCORE_FILE):
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(0))


# Reads the current high score in text file
def read_high_score():
    with open(HIGH_SCORE_FILE, "r") as f:
        hs = f.read()
    return int(hs)


# Overwrites current previous score if new is higher
def write_high_score(new_high_score):
    hs = read_high_score()
    with open(HIGH_SCORE_FILE, "r+") as f:
        if new_high_score > hs:
            f.write(str(new_high_score-1))


# To store current targets appearing on the screen
targets = []


# Calling this will spawn new targets
def newTarget():
    new = duplicate(target, y=-5+(5124*time.dt) % 15)
    targets.append(new)
    invoke(newTarget, delay=1)


# Spawns new targets
newTarget()
camera.orthographic = True
camera.fov = 20


# Continuously run
def update():
    global score, text
    player.y += held_keys['w'] * 6 * time.dt
    player.y -= held_keys['s'] * 6 * time.dt
    player.x += held_keys['d'] * 6 * time.dt
    player.x -= held_keys['a'] * 6 * time.dt
    a = held_keys['w'] * -20
    b = held_keys['s'] * 20
    if a != 0:
        player.rotation_z = a
    else:
        player.rotation_z = b
    for target in targets:
        target.x -= 4*time.dt
        touch = target.intersects()
        if touch.hit:
            a = Audio('/sound_effects/hit_effect.mp3/',
                      pitch=1, loop=False, autoplay=True)
            print(a)
            targets.remove(target)
            destroy(target)
            destroy(touch.entity)
            score += 1
            text.y = 10
            text = Text(text=f"Score: {score}", position=(-.65, .4),
                        origin=(0, 0), scale=2, color=color.yellow, background=True)
            write_high_score(score)
    t = player.intersects()
    if t.hit and t.entity.scale == 3:
        quit()


# Reference for input by user
def input(key):
    if key == 'space':
        a = Audio('/sound_effects/shoot_effect.mp3/',
                  pitch=1, loop=False, autoplay=True, volume=0.2)
        print(a)
        e = Entity(y=player.y, x=player.x+1, model='cube', scale=1,
                   texture='assets\Bullet', collider='cube')
        e.animate_x(30, duration=2, curve=curve.linear)
        invoke(destroy, e, delay=2)


# Initializations for Score
score = 0
text = Text(text='')
text = Text(text=f"Score: {score}", position=(-.65, .4),
            origin=(0, 0), scale=2, color=color.yellow, background=True)

# Continuously called for user inputs and updates
e.update = update
e.input = input

# Uncomment to test game without main menu
# app.run()
