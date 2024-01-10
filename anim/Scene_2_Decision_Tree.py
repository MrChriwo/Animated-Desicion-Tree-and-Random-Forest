from manim import *
import networkx as nx

class a_decision_tree_intro(Scene):

    def create_tree(self): 
        G = nx.Graph()

        G.add_node("ROOT")

        for i in range(5):
            G.add_node("Child_%i" % i)
            G.add_node("Grandchild_%i" % i)
            G.add_node("Greatgrandchild_%i" % i)

            G.add_edge("ROOT", "Child_%i" % i)
            G.add_edge("Child_%i" % i, "Grandchild_%i" % i)
            G.add_edge("Grandchild_%i" % i, "Greatgrandchild_%i" % i)

            # make all nodes black
            G.nodes["Child_%i" % i]["color"] = "black"


        return (Graph(list(G.nodes), list(G.edges), layout="tree", root_vertex="ROOT").set_color_by_gradient(BLUE, GREEN, RED))


    def construct(self):
        self.wait(0.5)
        title = Text("Decision Trees", font="Montserrat", color=WHITE).scale(1.5)
        title.to_edge(UP)
        title.set_color_by_gradient(BLUE, GREEN, RED)
        separator = Line(LEFT, RIGHT, color=WHITE).scale(2)
        separator.next_to(title, DOWN)

        # circle 
        circle = Circle(color=WHITE).scale(0.8)
        circle.set_color_by_gradient(BLUE, GREEN, RED)
        circle.next_to(separator, DOWN, buff=0.3)

        # tree
        tree = self.create_tree()
        tree.scale(0.3)
        tree.next_to(separator, DOWN, buff=0.5)


        group = Group(title, separator, circle, tree)
        group.center()

        self.play(Write(title))
        self.wait(0.3)
        self.play(Write(separator))
        self.wait(0.3)
        self.play(Create(group[2]))
        self.play(Create(group[3]))
        self.wait(2)
        self.play(FadeOut(*self.mobjects))



class b_explain_vocabs(Scene):

    DEPTH = 3
    CHILDREN_PER_VERTEX = 2
    LAYOUT_CONFIG = {"vertex_spacing": (1.2, 1)
                     }
    VERTEX_CONF = {"radius": 0.25, "color": WHITE, "fill_opacity": 1}

    def expand_vertex(self, g, vertex_id: str, depth: int):
        new_vertices = [f"{vertex_id}/{i}" for i in range(self.CHILDREN_PER_VERTEX)]
        new_edges = [(vertex_id, child_id) for child_id in new_vertices]
        g.add_edges(
            *new_edges,
            vertex_config=self.VERTEX_CONF,
            positions={
                k: g.vertices[vertex_id].get_center() + 0.1 * DOWN for k in new_vertices
            },
        )
        if depth < self.DEPTH:
            for child_id in new_vertices:
                self.expand_vertex(g, child_id, depth + 1)

        return g
    


    def get_headers(self):
        # explain texts 
        root_text = Text("Root Node", font="Montserrat", color=RED).scale(0.5)
        parent_text = Text("Parent Nodes", font="Montserrat", color=ORANGE).scale(0.5)
        child_text = Text("Child Nodes", font="Montserrat", color=PURPLE).scale(0.5)
        leaf_text = Text("Leaf Nodes", font="Montserrat", color=GREEN).scale(0.5)

        # group the text
        header_group = Group(root_text, parent_text, child_text, leaf_text)

        return header_group


    def construct(self):
        title = (Text("Decision Trees Vocabs", font="Montserrat", color=WHITE).scale(0.9))
        split_text = Text("Split", font="Montserrat", color=YELLOW).scale(0.5)
        depth_text = Text("Depth = 3", font="Montserrat", color=YELLOW).scale(0.5)


        g = Graph(["ROOT"], [], vertex_config=self.VERTEX_CONF)
        g = self.expand_vertex(g, "ROOT",1)
        title.to_edge(UP)
        self.play(Write(title))

        split_text.next_to(g, UP, buff=0.5)
        split_text.shift(LEFT*1.2)
        self.add(g)
        
        self.play(
            g.animate.change_layout(
                "tree",
                root_vertex="ROOT",
                layout_config=self.LAYOUT_CONFIG,
            )
        )
        self.wait(1)

        # get the root vertex and a explain text
        root = g.vertices["ROOT"]
        header_group = self.get_headers()

        # scale the graph down and move it to the left
        self.play(g.animate.scale(0.5))
        self.play(g.animate.shift(LEFT * 3))

        # arrange the header group and move it to the right of the graph
        header_group.arrange(DOWN, buff=0.5)
        header_group.next_to(g, RIGHT, buff=1.2)
        self.wait(0.2)

        # mark root in red and show the corresponding text
        self.play(Write(header_group[0]), root.animate.set_color(RED))
        self.wait(0.2)

        
        # gllow up the splits for short time with their edges
        self.play(
            g.vertices["ROOT/0"].animate.set_color(YELLOW),
            g.vertices["ROOT/1"].animate.set_color(YELLOW),
            g.edges["ROOT", "ROOT/0"].animate.set_color(YELLOW),
            g.edges["ROOT", "ROOT/1"].animate.set_color(YELLOW),
            Write(split_text)
        )
        self.wait(0.4)

        # return to the colors before highlighting the splits
        self.play(
            g.vertices["ROOT/0"].animate.set_color(WHITE),
            g.vertices["ROOT/1"].animate.set_color(WHITE),
            g.edges["ROOT", "ROOT/0"].animate.set_color(WHITE),
            g.edges["ROOT", "ROOT/1"].animate.set_color(WHITE),
            FadeOut(split_text)
        )

        self.wait(1)


        # mark the parent nodes in orange
        self.play(
            g.vertices["ROOT/0"].animate.set_color(ORANGE),
            g.vertices["ROOT/1"].animate.set_color(ORANGE),
            Write(header_group[1])
        )

        # mark the child nodes in purple
        self.wait(1)
        self.play(
            g.vertices["ROOT/0/0"].animate.set_color(PURPLE),
            g.vertices["ROOT/0/1"].animate.set_color(PURPLE),
            g.vertices["ROOT/1/0"].animate.set_color(PURPLE),
            g.vertices["ROOT/1/1"].animate.set_color(PURPLE),
            Write(header_group[2])
        )

        # mark leaf nodes
        self.wait(1)
        self.play(
            g.vertices["ROOT/0/0/0"].animate.set_color(GREEN),
            g.vertices["ROOT/0/0/1"].animate.set_color(GREEN),
            g.vertices["ROOT/0/1/0"].animate.set_color(GREEN),
            g.vertices["ROOT/0/1/1"].animate.set_color(GREEN),
            g.vertices["ROOT/1/0/0"].animate.set_color(GREEN),
            g.vertices["ROOT/1/0/1"].animate.set_color(GREEN),
            g.vertices["ROOT/1/1/0"].animate.set_color(GREEN),
            g.vertices["ROOT/1/1/1"].animate.set_color(GREEN),
            Write(header_group[3])
        )
        self.wait(1)


        # draw an down arrow left to the graph
        arrow = Arrow(UP, DOWN*2.2, color=WHITE).scale(0.8)
        arrow.next_to(g, LEFT, buff=0.5)

        depth_text.next_to(arrow, UP, buff=0.5)

        # mark the depth of the tree and highlight each node in the depth
        self.play(Create(arrow))

        self.play(
            g.vertices["ROOT/0"].animate.set_color(YELLOW),
            g.vertices["ROOT/0/0"].animate.set_color(YELLOW),
            g.vertices["ROOT/0/0/0"].animate.set_color(YELLOW),
            g.edges["ROOT/0", "ROOT/0/0"].animate.set_color(YELLOW),
            g.edges["ROOT/0/0", "ROOT/0/0/0"].animate.set_color(YELLOW),
            Write(depth_text)
        )
        self.wait(0.4)

        self.play(FadeOut(*self.mobjects))
        self.wait(0.3)

