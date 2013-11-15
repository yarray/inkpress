inkpress
========

Using inkscape to build the big graph of impress.js

## Description

Impress.js is great, even greater than prezi because you can use all the good
stuffs of html/js/css to get fantastic effects and these technologies are
towards future (unlike flash used by prezi). However, I feel upset to fill all
the "data-x, data-y..." in impress.js. It is hard to calculate and until
refreshing browser you cannot see the overall effects, which contradicts to my
taste.

There is Sozi that mimics prezi functionalities as inkscape plugin. But I think
that inkscape merely cannot support presentation well since it is hard to get
uniform text styles or create animations and it is impossible for svg to
combine the whole range of good stuffs as html/css/js do.

In my opinion the most exciting point of presentations on canvas like
impress.js, jmpress.js (which I'm also considering) or prezi is that they can
offer information on a big graph and present in a time line in hierarchical
manner. Presentations on canvas should not merely be something that induces
"wow". It should be used for better expression of non-linear ideas. Thus the
big graphs should be the very center of the processes of making such
presentations, which I believe inkscape is a ideal tool to deal with. On the
other hand, tools based on html5 like impress.js cannot be replaced for its
ability to embed nearly anything to the presentations.

## Tutorial

*For who are impatient: Check the demo, it is quite simple.*

### Suggested workflow:

1. Create an svg in inkscape (other tools are possible but there may be problems
because I haven't test them).
2. Create a layer named "Trace" which will determine the positions and sizes of
each step.
3. Create bounding boxes. All boxes should have the same width-height ratio but
you can rotate or resize it as you like. It is highly recommended that you
use boxes with the same width-height ratio with the resolution of target
display to avoid unexpected clip or leakage of background image. Give the
boxes ids to determine their order (the order is ONLY determined by the number
part of the id, so "1" will be after "rect-0").
4. Build the html. Add reference for jquery and impress, then add reference to
inkpress.js and inkpress.css. Invoke inkpress.init(svgPath, panelSize) after
the page is loaded.
5. Now view the html. **Notice** that the page should be viewed under a
web server since I use ajax to grab svg and insert into html (If you have
better idea please leave a comment). You should be able to move around as you
designed in the svg. Hooray!
6. Modify the html to add some steps containing text, whose styles can be
controlled uniformly by css. The steps named "step-{id}" will be linked to the
rectangle with "{id}" as its id.
7. Now it is time to make the Trace layer in the svg file invisible. Add
additional layers to the svg file containing those you'd like to present on
the screen.

## Further...

This project is created in one night for personal use so its functionalities
are quite limited and there are a lot of flaws. I will take more time to
improve it if time permits. All kinds of discussion and contributions are
highly welcomed. Please feel free to contact me by sending emails to
08to09@gmail.com.


Anran Yang  
2013.11.5
