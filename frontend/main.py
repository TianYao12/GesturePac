from taipy import Gui
from taipy.gui import Html

html_page = Html("""
<style>
    main {
      display: flex;
      justify-content: center;
      height: 100vh;
      margin: 0;
    }
</style>

<div class="main">
  <h1>Run it back!!!</h1>
  <p>Image goes here</p>
</div>  
""")
Gui(page=html_page).run()