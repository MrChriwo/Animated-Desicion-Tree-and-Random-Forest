from manim import *
import networkx as nx
import numpy as np

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


class c(Scene):
    
    def create_tree(self): 
        G = nx.Graph()

        G.add_node("ROOT")

        for i in range(5):
            G.add_node("Child_%i" % i)
            G.add_node("Grandchild_%i" % i)

            G.add_edge("ROOT", "Child_%i" % i)
            G.add_edge("Child_%i" % i, "Grandchild_%i" % i)

            # all nodes black
            G.nodes["Child_%i" % i]["color"] = "black"


        return (Graph(list(G.nodes), list(G.edges), layout="tree", root_vertex="ROOT").set_color_by_gradient(BLUE, GREEN, RED))
    
    def construct(self):
        title = (Text("Decision Trees", font="Montserrat", color=WHITE).scale(1.5))
        title.to_edge(UP)
        title.set_color_by_gradient(BLUE, GREEN, RED)
        self.play(Write(title))
        tree_classifier = self.create_tree()
        tree_regressor = self.create_tree()
        tree_classifier.scale(0.3)
        tree_regressor.scale(0.3)
        tree_classifier.next_to(LEFT*4.5, buff=0.5)
        tree_regressor.next_to(RIGHT*2, buff=0.5)

        title_classifier = Text("Classification Tree", font="Montserrat", color=WHITE).scale(0.7)
        title_regressor = Text("Regression Tree", font="Montserrat", color=WHITE).scale(0.7)
        title_classifier.next_to(tree_classifier, DOWN, buff=0.3)
        title_regressor.next_to(tree_regressor, DOWN, buff=0.3)

        self.play(Create(tree_classifier))
        self.wait(1)
        self.play(Write(title_classifier))
        self.wait(1)

        self.play(Create(tree_regressor))
        self.wait
        self.play(Write(title_regressor))
        self.wait(1)

        # self.play(title_classifier.scale, 1.5, title_classifier.shift, UP*0.8)
        title_classifier.animate.shift( RIGHT*0.8)

        explain_classifier = Text("Used for classification tasks", font="Montserrat", color=WHITE).scale(0.4)
        explain_classifier.next_to(title_classifier, DOWN, buff=0.3)
        self.play(Write(explain_classifier))

        explain_classifier_2 = Text("Predicts a class", font="Montserrat", color=WHITE).scale(0.4)
        self.wait(1)
        explain_classifier_2.next_to(explain_classifier, DOWN, buff=0.3)
        self.wait(1)
        self.play(Write(explain_classifier_2))

        explain_regressor = Text("Used for regression tasks", font="Montserrat", color=WHITE).scale(0.4)
        explain_regressor.next_to(title_regressor, DOWN, buff=0.3)
        explain_regressor_2 = Text("Predicts a numeric value", font="Montserrat", color=WHITE).scale(0.4)
        explain_regressor_2.next_to(explain_regressor, DOWN, buff=0.3)
        self.wait(1)
        self.play(Write(explain_regressor))
        self.wait(1)
        self.play(Write(explain_regressor_2))
        self.wait(2)

        self.play(FadeOut(*self.mobjects))
        self.wait(0.3)



class d(Scene):

    def __init__(self): 
        super().__init__()
        self.treeDepth = 1
        self.treeChildren = 2
        self.treeLayoutConfig = {"vertex_spacing": (1.8, 2.1)}
        self.treeVertexConfig = {"radius": 0.85, "color": GREY, "fill_opacity": 1, "stroke_width": 3}
        
    def expand_vertex(self, g, vertex_id: str, depth: int):
        new_vertices = [f"{vertex_id}/{i}" for i in range(self.treeChildren)]
        new_edges = [(vertex_id, child_id) for child_id in new_vertices]
        
        g.add_edges(
            *new_edges,
            vertex_config=self.treeVertexConfig,
            positions={
                k: g.vertices[vertex_id].get_center() + 0.1 * DOWN for k in new_vertices
            },
        )
        if depth < self.treeDepth:
            for child_id in new_vertices:
                self.expand_vertex(g, child_id, depth + 1)

        return g


    def create_random_row(self):
        num = 0
        while True:
            # random values for the columns
            random_row = [
                np.random.choice(["rot", "orange"]),
                np.random.choice(["leicht", "schwer"]),
                np.random.choice(["klein", "groß"]),
                np.random.choice(["apfel", "orange"]),
            ]

            if "apfel" in random_row and "orange" in random_row and ["orange", "rot"] in random_row or num > 10:
                return [str(x) for x in random_row]
            else: 
                num += 1

    def calculate_gini(self, p0, p1):
        return 1 - (p0 ** 2 + p1 ** 2)


    def construct(self):
        title = (Text("Classification Trees", font="Montserrat", color=WHITE).scale(1.5))
        title.to_edge(UP)
        title.set_color_by_gradient(BLUE, GREEN, RED)
        self.play(Write(title))
        self.wait(1)


        rect = Rectangle(height=2, width=7, color=WHITE)
        rect.set_color_by_gradient(BLUE, GREEN, RED)
        rect.next_to(title, DOWN, buff=1.2)
        self.play(Create(rect))
        self.wait(1)

        # wirte gini formula in the rectangle
        gini_formula = MathTex("Gini", "(", "t", ")", "=", "1", "-", "(", "p", "_", "0", "^2", "+", "p", "_", "1", "^2", ")")
        gini_formula.scale(1.3)
        gini_formula.next_to(title, DOWN, buff=1.9)

        gini_grp = VGroup(rect, gini_formula)
        # display the gini formula grp 
        self.play(Write(gini_grp))
    
        self.wait(2)

        # scale grp down and  move the grp to left bottom corner 
        self.play(gini_grp.animate.scale(0.4))
        self.play(gini_grp.animate.shift(DOWN*3.2))
        self.play(gini_grp.animate.shift(RIGHT*3.4))
        self.wait(1)

        num_rows = 5

        table = Table(
            [["Farbe", "Gewicht", "Größe", "Obst"]] +
            [["rot", "leicht", "klein", "apfel"],
            ["orange", "schwer", "groß", "orange"],
            ["rot", "leicht", "groß", "apfel"],
            ["orange", "leicht", "klein", "apfel"],
            ["rot", "schwer", "klein", "orange"]],
            h_buff=1,
            v_buff=0.5,
            line_config={"color": WHITE},
            fill_color=BLUE,
            fill_opacity=1,
        )
        tree = Graph(["ROOT"], [], vertex_config=self.treeVertexConfig)

        rows = ["Farbe", "Gewicht", "Groesse", "Obst"]

        table.scale(0.7)
        table.next_to(title, DOWN, buff=0.5)
        self.play(Create(table))
        self.wait(1.5)

        # scale the table down and move it to the left
        self.play(table.animate.scale(0.7))
        self.play(table.animate.shift(LEFT*3))
        self.wait(1)

        self.wait(2)

        # column_texts = [Text(f"score {i+1}", font_size=24).next_to(table.get_columns()[i], DOWN) for i in range(4)]
        scores = {any: any}

        for i in range(3):
            # Highlight column
            self.play(table.get_columns()[i].animate.set_color(YELLOW))

            # tree root node is the current column
            tree = Graph([rows[i]], [], vertex_config=self.treeVertexConfig, labels=True)

            tree = self.expand_vertex(tree, rows[i], 1)
            tree = self.expand_vertex(tree, f"{rows[i]}/0", 2)
            tree = self.expand_vertex(tree, f"{rows[i]}/1", 2)

            tree.scale(0.6) 

            self.add(tree)
        
            self.play(
                tree.animate.change_layout(
                    "tree",
                    root_vertex=f"{rows[i]}",
                    layout_config=self.treeLayoutConfig,
                    
                )
            )


            self.play(tree.animate.scale(0.7))
            self.play(tree.animate.shift(RIGHT*3.7))
            # animate a arrow pointing on the table fro right 
            arrow = Arrow(RIGHT, LEFT*2, color=WHITE).scale(0.8)
            arrow.next_to(table, RIGHT, buff=0.5)
            arrow.shift(UP*0.9)
            self.play(Create(arrow))

        
            apfel = 0
            orange = 0
            
            for i in range(4):
                if i % 2 == 0: 
                    apfel += 1

                    self.play(arrow.animate.set_color(RED), arrow.animate.shift(DOWN*0.6) )
                else: 
                    orange += 1
                    self.play(arrow.animate.set_color(ORANGE), arrow.animate.shift(DOWN*0.6), arrow.animate.shift(DOWN*0.6) )
                self.wait(1)


            self.play(FadeOut(arrow))
            self.wait(1)
            self.play(table.get_columns()[i].animate.set_color(WHITE))

            entities = table.get_rows()[1:]
            num_apples = sum([1 for entity in entities if entity[i] == "apfel"])
            num_oranges = sum([1 for entity in entities if entity[i] == "orange"])
            gini = self.calculate_gini(num_apples / num_rows, num_oranges / num_rows)
            scores[i] = gini
            self.play(FadeOut(tree))

        self.wait(1)
        self.play(FadeOut(*self.mobjects))

        


class e(Scene):
    DEPTH = 3
    CHILDREN_PER_VERTEX = 2
    LAYOUT_CONFIG = {"vertex_spacing": (1.2, 1)}
    VERTEX_CONF = {"radius": 0.25, "color": WHITE, "fill_opacity": 1}

    def expand_vertex(self, g, vertex_id: str, depth: int):
        new_vertices = [f"{vertex_id}/{i}" for i in range(self.CHILDREN_PER_VERTEX)]
        new_edges = [(vertex_id, child_id) for child_id in new_vertices]
        g.add_edges(
            *new_edges,
            vertex_config=self.VERTEX_CONF,
            positions={k: g.vertices[vertex_id].get_center() + 0.1 * DOWN for k in new_vertices},
        )
        if depth < self.DEPTH:
            for child_id in new_vertices:
                self.expand_vertex(g, child_id, depth + 1)
        return g

    def construct(self):
        # Create and expand the tree
        tree = Graph(["ROOT"], [], vertex_config=self.VERTEX_CONF)
        tree = self.expand_vertex(tree, "ROOT", 1)
        tree.scale(0.7)
        self.play(
            tree.animate.change_layout(
                "tree",
                root_vertex="ROOT",
                layout_config=self.LAYOUT_CONFIG,
            )
        )


        self.play((tree.vertices["ROOT"].animate.set_color(RED)))
        self.wait(1)
        self.play(tree.vertices["ROOT/0"].animate.set_color(GREEN))
        self.wait(1)
        self.play(tree.vertices["ROOT/0/0"].animate.set_color(GREEN))
        self.wait(1)
        self.play(tree.vertices["ROOT/0/0/1"].animate.set_color(GREEN))
        # reset the colors
        self.play(
            tree.vertices["ROOT"].animate.set_color(WHITE),
            tree.vertices["ROOT/0"].animate.set_color(WHITE),
            tree.vertices["ROOT/0/0"].animate.set_color(WHITE),
            tree.vertices["ROOT/0/0/1"].animate.set_color(WHITE),
        )
        self.wait(1)
        # another way 
        self.play((tree.vertices["ROOT"].animate.set_color(RED)))
        self.wait(1)
        self.play(tree.vertices["ROOT/0"].animate.set_color(GREEN))
        self.wait(1)
        self.play(tree.vertices["ROOT/0/0"].animate.set_color(GREEN))
        self.wait(1)
        self.play(tree.vertices["ROOT/0/0/0"].animate.set_color(GREEN))
        # reset the colors
        self.play(
            tree.vertices["ROOT"].animate.set_color(WHITE),
            tree.vertices["ROOT/0"].animate.set_color(WHITE),
            tree.vertices["ROOT/0/0"].animate.set_color(WHITE),
            tree.vertices["ROOT/0/0/0"].animate.set_color(WHITE),
        )

        # another way 
        self.play(tree.vertices["ROOT/0"].animate.set_color(GREEN))
        self.wait(1)
        self.play(tree.vertices["ROOT/0/1"].animate.set_color(GREEN))
        self.wait(1)
        self.play(tree.vertices["ROOT/0/1/0"].animate.set_color(GREEN))
        # reset the colors
        self.play(
            tree.vertices["ROOT/0"].animate.set_color(WHITE),
            tree.vertices["ROOT/0/0"].animate.set_color(WHITE),
            tree.vertices["ROOT/0/1"].animate.set_color(WHITE),
            tree.vertices["ROOT/0/1/0"].animate.set_color(WHITE),
        )

        self.wait(2)

        self.play( tree.verticies["ROOT"].animate.set_color(RED))
        self.wait(1)
        self.play(tree.verticies["ROOT/1"].animate.set_color(GREEN))
        self.wait(1)
        self.play( tree.verticies["ROOT/1/0"].animate.set_color(GREEN))
        self.wait(1)
        self.play(tree.verticies["ROOT/1/0/1"].animate.set_color(GREEN))

        self.wait(2)

        # clean up
        self.play(
            tree.vertices["ROOT"].animate.set_color(WHITE),
            tree.vertices["ROOT/1"].animate.set_color(WHITE),
            tree.vertices["ROOT/1/0"].animate.set_color(WHITE),
            tree.vertices["ROOT/1/0/1"].animate.set_color(WHITE),

        )

        self.play(FadeOut(*self.mobjects))