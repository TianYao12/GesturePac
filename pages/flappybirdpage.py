from taipy.gui import Gui, Markdown

text="Open and close your hand to make Faby jump!"
content1="../flappybirdimage.jpg"
content2="../states.jpg"


# Definition of the page
flappybird_page = Markdown("""
<|{text}|id=pacmantitle|>
<container|container|
<|{content1}|image|id=column|width=26vw|height=32vw|>
<|{content2}|image|id=column|width=38vw|height=32vw|>

""")


