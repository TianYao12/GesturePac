from taipy.gui import Gui
from pages.landing import landing_page
from pages.pacmanpage import pacman_page
from pages.flappybirdpage import flappybird_page

pages = {
 "/": "<center><|navbar|></center>",
"landing": landing_page,
"pacman": pacman_page,
"flappybird": flappybird_page
}


Gui(pages=pages).run()