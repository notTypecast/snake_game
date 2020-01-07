# snake_game
This is the good old "snake" game, where you control a snake trying to grab apples and grow, and try to avoid hitting walls or eating your own tail.

The only actual assets currently in use for the game are a UI box and a tick. These are two .png images stored in an "assets" folder, which needs to be in the same directory as the snake.py file. Everything else is made using basic shapes from the pygame.draw class. This might change in the future.

I have basically made the original game, with (so far) a few additions of my own. These will be listed below:

-3 types of apples instead of just 1. From the moment the game starts, instead of simply having one apple spawn, you have 3 of them. A red one, a blue one and a green one.

-Different way of calculating points received per apple. In the original "snake" game, an apple would usually reward the player with 1 point. The player would also increase their snake's length whenever one was eaten. If someone were to play my version for a while, they would think the points rewarded per apple are about 1-10 each, randomly. This isn't exactly the case (there is going to be some math below).
-----------------------
For red apples, the sin of the player's score is calculated. This is multiplied by 10 and then rounded (so the score is always a round value). For blue apples, the same is done, but instead of the sin, the cos of the score is calculated. Finally, for green apples, the sin of the score is multiplied by the cos of the score, which as a product of the two, is then multiplied by 10 and, just like before, rounded.
One can realize that the functions f(x) = sinx and g(x) = cosx have a Af = Ag = R. Yet, from the graphical representation of those two functions we can see that f(R) = g(R) = [-1, 1].
What this practically means is that, no matter which number we apply to f or g, we are not going to get any results besides numbers between -1 and 1, including those two. Therefore, no matter how high the score of the user gets, apples can never give more than 10 points (since the number is multiplied by 10 and rounded). 
However, g ≠ f. Therefore, there will be points where, for the same number, f will give a higher result than g, or the opposite. This means that you can never know which apple, red or blue, will give you more points if picked up.
Green apples are a different story. By multiplying f * g, we get h(x) = sin(x) * cos(x). This function, just like f and g, has an Ah = R. However, its h(R), as one could notice from the function's graph, is [-0.5, 0.5].
For the game, this means that a green apple cannot give more than 5 points. This doesn't mean that it isn't worth going for the green apple, though. Due to how numbers are rounded, there could be points where the green apple would reward one more than any of the other two apples.
-----------------------
The snake's tail obviously grows much faster than in the regular snake game, since 1 block is added to it per point.

-Powerups. The way powerups work, is as follows. Whenever a game starts, a random set of 3 apple colors (red, green or blue) is displayed on top of the screen. If the player eats 3 apples in the same order shown above, they enter the powerup state (note that picking up the wrong apple will reset the set and give the player a new random set of 3 colors). This state lasts for 10 seconds. Upon entering it for the first time, the player gets three changes (and also party snake!). The players' speed is increased. This could be considered a hindrance, since it makes the snake harder to control and it is also easier to die. Nevertheless, this is sort of balanced out by the fact that self-death is disabled. This means that, while in powerup state, the player can go through their own tail without losing. Finally, the player gets increased points while in this state (since it is also harder to eat apples).
One would notice that, whenever this state is entered, a text saying "Powerup x 1" appears on the top left side of the screen. This is essentially a combo-type system. While in powerup state, if the player manages to eat the apples in the order shown above successfully, before the state ends, the timer is reset and they enter the "Powerup x 2" state.
-----------------------
The change that each new powerup stage brings has to do with the combo multiplier. This multiplier represents the stage that one is in (and thus the number shown on screen, next to "Powerup x"). In essence, whenever in powerup state, the player's speed is increased by 2 * combo_multiplier.  The points received are also increased by 1.2 * combo_multiplier (and, of course, rounded).
-----------------------
(Note: The snake, during and after powerup stage 2, starts splitting into boxes more and more due to the speed increase. I believed that that was a cool effect, so I left it in.)
