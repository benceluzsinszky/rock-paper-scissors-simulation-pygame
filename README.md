# Rock, Paper, Scissor simulation

A 2D Rock, Paper, Scissor simulation with Pygame.

## Requirements
This game was built using Python 3.11.3 and Pygame 2.3.0. 

You need to install Pygame and Scipy to run the simulation:


`pip install pygame`

`pip install scipy`

## How to Play
Clone the repository or download the code files.
Navigate to the project directory and run the command:

`python main.py`

In the main menu, use the sliders to set the speed and group size of the sprites.

Click on the `PLAY` button to start the simulation.

The simulation runs automatically, the group that stays alive in the end wins the round.

Click the `Restart` button in the game over screen to play again.

Click the `Main menu` button in game over screen to go back to the main menu.

## Code Structure
The code is structured as follows:

`main.py`: The main game script that initializes the game and contains the main menu, game loop, and game over screen.

`sprites.py`: Contains the Sprite class, which is the base class for the different types of sprites (rock, paper, and scissors) and their associated methods.

`sprites/`: Contains the sprite images and logo used in the game.

`font/`: Contains the font used in the game.

`README.md`: This readme file.

## Credits
The logo was taken from flaticon.com.

The sprite images are Microsoft Emojis. For more information, visit [Font redistribution FAQ for Windows](https://learn.microsoft.com/en-us/typography/fonts/font-faq).

The font used in the game is [Press Start by CodeMan38](https://www.fontspace.com/press-start-2p-font-f11591).
