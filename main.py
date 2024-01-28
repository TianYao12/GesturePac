from taipy.gui import Gui
from pages.landing import landing_page
from pages.pacmanpage import pacman_page
from pages.flappybirdpage import flappybird_page
from pages.pmleaderboard import pmleaderboard_page
from pages.fbleaderboard import fbleaderboard_page

pages = {
 "/": "<center><|navbar|></center>",
"landing": landing_page,
"pacman": pacman_page,
"flappybird": flappybird_page,
"Pac-Man-Leaderboard": pmleaderboard_page,
"Flappy-Bird-Leaderboard": fbleaderboard_page
}


Gui(pages=pages).run()