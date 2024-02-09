from manim import * 
import networkx as nx


class Outro(Scene):
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

        title = Text("Zusammenfassung", font="Arial", color=WHITE).scale(1.5)
        title.to_edge(UP)
        self.play(Write(title))

        # decision tree
        decision_tree = self.create_tree()

        decision_tree.scale(0.5)

        decision_tree.shift(LEFT * 4)

        tree_title = Text("Decision Trees", font="Arial", color=WHITE).scale(.5)

        tree_title.next_to(decision_tree, DOWN, buff=0.5)

        tree_sub_1 = Text("Fragen und Antwort basiert", font="Arial", color=WHITE).scale(.3)

        tree_sub_1.next_to(tree_title, DOWN, buff=0.3)

        tree_sub2 = Text("Baumstruktur", font="Arial", color=WHITE).scale(.3)

        tree_sub2.next_to(tree_sub_1, DOWN, buff=0.3)



        self.play(Write(decision_tree))

        self.play(Write(tree_title), Create(decision_tree))

        self.wait(2)

        self.play(Write(tree_sub_1))

        self.wait(2)

        self.play(Write(tree_sub2))

        self.wait(2)





        # boosting
        boosting_title = Text("Boosting", font="Arial", color=WHITE).scale(.5)
        boosting_title.shift(UP)
        bst_sub_1 = Text("Kombination von schwachen Lernalgorithmen", font="Arial", color=WHITE).scale(.3)
        bst_sub_1.next_to(boosting_title, DOWN, buff=0.3)
        bst_sub_2 = Text("zu einem starken Lernalgorithmus", font="Arial", color=WHITE).scale(.3)
        bst_sub_2.next_to(bst_sub_1, DOWN, buff=0.3)
        self.play(Write(boosting_title))
        self.wait(2)
        self.play(Write(bst_sub_1))
        self.wait(1.3)
        self.play(Write(bst_sub_2))
        self.wait(2)

        self.wait(2)


        # random forest
        random_forest = Text("Random Forests", font="Arial", color=WHITE).scale(.5)
        random_forest.shift(RIGHT * 4.3)
        random_forest.shift(UP * 1.5)

        rfsubs0 = Text("Bagging", font="Arial", color=WHITE).scale(.5)
        rfsubs0.next_to(random_forest, DOWN, buff=0.3)

        rf_sub_1 = Text("Ensemble von Entscheidungsbäumen", font="Arial", color=WHITE).scale(.3)
        rf_sub_1.next_to(rfsubs0, DOWN, buff=0.3)
        rf_sub_2 = Text("Viele Bäume entscheiden", font="Arial", color=WHITE).scale(.3)
        rf_sub_3 = Text("Mehrheitsabstimmung", font="Arial", color=WHITE).scale(.3)
        rf_sub_2.next_to(rf_sub_1, DOWN, buff=0.3)
        rf_sub_3.next_to(rf_sub_2, DOWN, buff=0.3)
        
        self.play(Write(random_forest))

        self.wait(2)
        self.play(Write(rfsubs0))
        self.wait(2)
        self.play(Write(rf_sub_1))      
        self.wait(1.3)
        self.play(Write(rf_sub_2))
        self.wait(1.3)
        self.play(Write(rf_sub_3))  
        self.wait(4)
        self.play(FadeOut(*self.mobjects)) # fade out all mobjects




