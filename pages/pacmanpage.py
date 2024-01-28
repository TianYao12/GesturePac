from taipy.gui import Gui, Markdown


title="Pac-man"
content1="../pacmanimage.jpg"
content2="../directions.jpg"
text="Use hand gestures to control Pac-Man!"

# Definition of the page
pacman_page = Markdown("""
<|{text}|id=pacmantitle|>
<container|container|
<|{content1}|image|id=column|width=35vw|height=25vw|>
<|{content2}|image|id=column|width=50vw|height=25vw|>
                       
""")


