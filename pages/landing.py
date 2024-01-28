from taipy.gui import Gui, Markdown


title="Telekinesis"
content1="../landingimg2.png"
text="A new way to play old games!"

# Definition of the page
landing_page = Markdown("""
<container|container|
<|{title}|id=maintitle|>

<|{text}|text|id=slogan|>
<container|container|
<|{content1}|image|id=ic|width=50vw|height=25vw|>
""")


