Things to go over:
 1. The current behavior, the issue. ***
 2. The expected behavior (the idea I pitched in the other issue). ***
 3. Maybe mention the findings from the sim, I guess, sort of explain why the issue is the way it is. ***
 4. Link to the notebook (can we just have it a gist?) mentioning the discussion area in particular for, particularly the possible method of implementation of these changes.



THIS IS THE AUTO-STOPPING VERTICES ISSUE DRAFT
# Current Behavior
Currently, when you load a provenance file in a ProVis tab the nodes space out but they don't stop automatically. Rather, you need to manually stop them using the "Stop Vertices" switch. There are a couple issues that stem from this.

If you have detached nodes or detached groups of nodes, and you don't press "Stop Vertices" once they've spaced out, they will drift away from each other (explained later) and out of sight, requiring you to chase after them. Even a single node or a connected graph will drift.
 * This is because of the constants used in the implementation of the force directed graph. Specifically, the ones used in calculating the attractive and repelling forces between nodes. You would expect the net force of a node to gradually approach 0 as things space out, however, with the current set of constants, it doesn't approach 0, thus they drift. With the right set of constants, the net force upon a node should gradually go down to 0.
 * As for the unconnected nodes or groups of nodes, this is because there is only a repelling force calculated between them and the nodes they're not connected to. No attractive force to counter it, resulting in drifting. Still, with the right set of constants, it should gradually go down to 0.

This setup also makes it confusing to open a diff between two nodes, which requires dragging one node to another. If you don't select "Stop Vertices" before dragging, the node you're dragging towards runs away (trying to space itself out). If you select "Stop Vertices" you can drag one on top of another, but once you've closed the diff, they're left sitting on top of each other, and to space them back out, you must unselect "Stop Vertices", selecting it again once they've spaced out.

# Expected Behavior
Upon loading a provenance file, the force directed graph algorithm will run until everything is spaced out. It must determine by itself when the nodes are spaced out and stop.
 * According to [this](https://cs.brown.edu/people/rtamassi/gdhandbook/chapters/force-directed.pdf) paper, (specifically section 12.2 from page 3 to 4, which covers the force directed graph implementation ProVis uses) it mentions that the criteria for an "aesthetically pleasing graph" is that (1) the lengths of the edges ought to be the same, and (2) the layout should display as much symmetry as possible. I discuss this further in the Jupyter Notebook linked towards the end of this issue description.

From then on, whenever the user interacts with the nodes (by dragging them) the algorithm should be stopped so they don't have to chase other nodes, and when they're done (once the node being dragged is released), the algorithm should run again to space everything back out, stopping automatically.

Of course, all of this means the "Stop Vertices" toggle will be removed.

# Jupyter Notebook
I made a Jupyter Notebook [here]() containing a force directed graph implementation just like the one used by ProVis. It sets up a bunch of nodes in random locations, creating edges to form multiple groups of them and links the groups together. It then runs the force directed graph algorithm to space everything out (the simulation portion). Doing this allowed me to
 * Visualize data (e.g., net forces of the nodes throughout the simulation), so I could get a better understanding of how this algorithm works.
 * Understand why the current set of constants used in calculating the attractive and repelling forces don't work as expected and have a way to find a proper set of constants.

At the end of the notebook is a Discussion covering most of the things mentioned here and my discoveries in finding a method to automatically detect when the nodes have been spaced out - that bit in partiuclar you should look at if you are trying to solve this issue. It also goes over how to find the right set of constants.



THIS IS THE VANILLA REDRAWING METHOD ISSUE DRAFT

Currently, the canvas (the off-white portion of the ProVis tab wherein the nodes are displayed) is re-drawn for every single frame. However, as long as the window isn't resized (and I believe if it isn't minimized) the canvas will stay the same. You don't need to redraw it every time.

So, we should only redraw the canvas when the user is interacting with it, *or* when the window is being resized or iconified (minimized). Interaction with the canvas includes:
 * Hovering over a node or edge (which highlights the item being hovered upon, providing it with a label).
 * Clicking on a node or relationship, or dragging a node.
 * Selecting any switches in the right-hand panel of the ProVis tab that affects what's rendered in the Canvas (i.e., "All Vertex IDs", or "All Relationships", etc.)

Additionally, we must keep redrawing frames when the graph in the ProVis tab is being spaced out, otherwise the graph will space out but the display won't be updated to match.