from ursina import *

# Initialization of high score text file
SCORE_FILE = "high_score.txt"


# Reference of our action function for high_score_menu button
def read_high_score():
    with open(SCORE_FILE, "r") as f:
        hs = f.read()
        global high_score_text
        high_score_text = Text(f"High Score: {hs}")
        high_score_text.enabled = True
        high_score_text.position = (0, -.2)
        high_score_text.origin = (0, 0)


# Class of game menu
class MenuMenu(Entity):
    def __init__(self, **kwargs):
        super().__init__(parent=camera.ui, ignore_paused=True)

        # Parents of menus content
        self.main_menu = Entity(parent=self, enabled=True)
        self.high_score_menu = Entity(parent=self, enabled=False)
        self.help_menu = Entity(parent=self, enabled=False)

        # Background of Main Menu
        self.background = Sprite(
            '/assets/main_menu.png/', z=1)
        # Background Music of Main Menu
        a = Audio('/sound_effects/menu_bgm.mp3/',
                  pitch=1, loop=False, autoplay=True)
        print(a)  # Plays menu backgroind music
        # [MAIN MENU] WINDOW START
        # Welcome Message
        Text("Team Arcadia Proudly Presents",
             parent=self.main_menu, y=0.4, x=0, origin=(0, 0))

        # Reference of action function to start game
        def start_game_btn():
            a.stop()  # Stops menu background music
            self.main_menu.disable()
            self.background.disable()
            import app

        # Reference of our action function for quit button
        def quit_game():
            application.quit()

        # Reference of our action function for high_score button
        def high_score_menu_btn():
            read_high_score()
            self.high_score_menu.enable()
            self.main_menu.disable()

        # Reference of our action function for resetting high score button
        def reset_high_score():
            with open(SCORE_FILE, "r+") as f:
                f.truncate(0)
                f.write(str(0))
                high_score_text.enabled = False
                read_high_score()

        # Reference of our action function for help button
        def help_menu_btn():
            self.help_menu.enable()
            self.main_menu.disable()

        # Button list
        ButtonList(button_dict={
            "Start": Func(start_game_btn),
            "High Score": Func(high_score_menu_btn),
            "Help": Func(help_menu_btn),
            "Exit": Func(quit_game)
        }, y=-0.3, parent=self.main_menu)
        # [MAIN MENU] WINDOW END

        # [SCORE MENU] WINDOW START
        # Title of our menu
        Text("High Score", parent=self.high_score_menu,
             y=0.4, x=0, origin=(0, 0))

        Button("Reset High Score", parent=self.high_score_menu, y=-0.3, scale=(0.2, 0.05), color=rgb(50, 50, 50),
               on_click=reset_high_score)

        # Reference of our action function for back button
        def high_score_back_btn_action():
            high_score_text.enabled = False
            self.main_menu.enable()
            self.high_score_menu.disable()

        # Back Button in Score Menu
        Button("Back", parent=self.high_score_menu, y=-0.4, scale=(0.1, 0.05), color=rgb(50, 50, 50),
               on_click=high_score_back_btn_action)

        # [HIGH SCORES MENU] WINDOW END

        # [HELP MENU] WINDOW START
        # Title of our menu
        Text("HELP MENU", parent=self.help_menu, y=0.4, x=0, origin=(0, 0))

        # Reference of our action function for back button
        def help_back_btn_action():
            about.enabled = False
            controls.enabled = False
            self.main_menu.enable()
            self.help_menu.disable()

        # About section content
        about = Text("Virus Fighter is a game developed by Team Arcadia. Inspired by 2D shooting games out there powered by Ursina Engine. \nThis game will bring out the tough and challenging battle of combating the viruses that planned to inhabit and bring chaos\nto the Earth. #GetVaccinated! \n\nDisclaimer: We do not own any of the sounds used in this project as it is used for educational purposes only.\nCredits go to MapleStory's CODASOUND.")
        about.enabled = False
        about.position = (0, -.2)
        about.origin = (0, 0)

        # Reference for enabling [About] content
        def enable_about_info():
            controls.enabled = False
            about.enabled = True

        # Controls section content
        controls = Text(
            "The movement of you, as a syringe can be controlled by pressing 'WASD' keys and spacebar to shoot.\nYou get points by eliminating viruses without touching or having contact with them!")
        controls.enabled = False
        controls.position = (0, -.2)
        controls.origin = (0, 0)

        # Reference for enabling [Controls] content
        def enable_controls_info():
            about.enabled = False
            controls.enabled = True

        # Button list
        ButtonList(button_dict={
            "About": Func(enable_about_info),
            "Controls": Func(enable_controls_info),
            "Back": Func(help_back_btn_action)
        }, y=-0.3, parent=self.help_menu)
        # [HELP MENU] WINDOW END

        # Change attributes of this class when called
        for key, value in kwargs.items():
            setattr(self, key, value)

    # Input function that check if key pressed on keyboard
    def input(self, key):

        # If our main menu enabled and we press [Escape]
        if self.main_menu.enabled:
            if key == "escape":
                # Close app
                application.quit()

        # If our high_score menu enabled and we press [Escape]
        if self.high_score_menu.enabled:
            if key == "escape":
                # Close high_score window and show main menu
                self.main_menu.enable()
                self.high_score_menu.disable()

        # If our help menu enabled and we press [Escape]
        if self.help_menu.enabled:
            if key == "escape":
                # Close help window and show main menu
                self.main_menu.enable()
                self.help_menu.disable()

    # Update function that check something every frame
    def update(self):
        pass


# Setup window title
window.title = "Virus Fighter"

# Init application
app = Ursina()

# Call our menu
main_menu = MenuMenu()

# Run application
app.run()
