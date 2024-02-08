from manim import *

class Intro(Scene):
    def construct(self):
        # Erstelle das Textobjekt für "Bootstrap aggregating" und füge es animiert hinzu
        text_bootstrap = Text("Bootstrap aggregating", font_size=72)
        text_bootstrap.move_to(ORIGIN)
        self.play(Write(text_bootstrap))

        # Warte einen Moment, bevor das Wort "Bootstrap aggregating" in "Bagging" transformiert wird
        self.wait(1)

        # Erstelle das Textobjekt für "Bagging"
        text_bagging = Text("Bagging", font_size=72)
        text_bagging.move_to(text_bootstrap.get_center())

        # Führe eine sanfte Animation durch, um von "Bootstrap aggregating" zu "Bagging" zu wechseln
        self.play(Transform(text_bootstrap, text_bagging))

        # Lass das Wort "Bagging" langsam nach oben fahren und das Wort "Bootstrap aggregating" verschwinden
        self.play(ApplyMethod(text_bootstrap.move_to, UP * 3), FadeOut(text_bagging))

        # Erstelle die Bullet Points
        bullet_points = VGroup(
            Text("• Grundlage für Random Forest", font_size=36),  # Erstes Bullet Point
            Text("• Mehrere Bäume aus den Daten", font_size=36),  # Zweites Bullet Point
            Text("• Mehrheitsentscheidung", font_size=36)  # Drittes Bullet Point
        ).arrange(DOWN, aligned_edge=LEFT)  # Anordnen der Bullet Points vertikal
        bullet_points.next_to(text_bootstrap, DOWN)  # Positionieren der Bullet Points unterhalb des Textes
        bullet_points.shift(DOWN)  # Die Bullet Points etwas nach unten verschieben

        # Animiere die Bullet Points
        for bullet_point in bullet_points:
            self.play(Write(bullet_point))
            self.wait(0.5)  # Eine kleine Pause zwischen den Bullet Points

        # Warte einige Sekunden, um das endgültige Ergebnis zu betrachten
        self.wait(2)

class Bagging(Scene):

    def construct(self):
        # Erstelle die Überschrift "Bagging" und lasse sie erscheinen
        title = Text("Bagging", font_size=72)
        title.move_to(UP * 2.5)  # Positionieren der Überschrift oben auf dem Bildschirm

        # Führe eine Animation durch, um die Überschrift langsam aufzubauen
        self.play(Write(title))

        # Warte einen Moment, bevor das Bild erscheint
        self.wait(1)

        # Erstelle das Bildobjekt für "data.png" und lasse es erscheinen
        data_image = ImageMobject("../assets/Intro/data.png")
        data_image.scale(0.5)  # Skalieren des Bildes auf die Hälfte der Größe
        data_image.next_to(title, DOWN)  # Positionieren des Bildes unterhalb der Überschrift

        # Führe eine Animation durch, um das Bild langsam aufzubauen
        self.play(FadeIn(data_image))

        # Erstelle die Pfeile
        arrow1 = Arrow(data_image.get_bottom(), LEFT * 5 + DOWN, color=WHITE)
        arrow2 = Arrow(data_image.get_bottom(), DOWN, color=WHITE)
        arrow3 = Arrow(data_image.get_bottom(), RIGHT * 5 + DOWN, color=WHITE)

        # Erstelle den ersten Entscheidungsbaum
        self.play(GrowArrow(arrow1))
        first_tree = self.create_decision_tree(LEFT * 5 + DOWN)

        # Erstelle den zweiten Entscheidungsbaum
        self.play(GrowArrow(arrow2))
        second_tree = self.create_decision_tree(DOWN)

        # Erstelle den dritten Entscheidungsbaum
        self.play(GrowArrow(arrow3))
        third_tree = self.create_decision_tree(RIGHT * 5 + DOWN)

        # Warte einen Moment, bevor die Unterschriften erscheinen
        self.wait(1)

        # Füge die Unterschrift "BAD" unter den ersten Baum hinzu
        bad_text = Text("BAD", color=RED).next_to(first_tree[0], DOWN).shift(1 * DOWN + 1 * LEFT)
        self.play(Write(bad_text))

        # Füge die Unterschrift "MID" unter den zweiten Baum hinzu
        mid_text = Text("MID", color=YELLOW).next_to(second_tree[0], DOWN).shift(1 * DOWN + 1 * LEFT)
        self.play(Write(mid_text))

        # Füge die Unterschrift "BEST" unter den dritten Baum hinzu
        best_text = Text("BEST", color=GREEN).next_to(third_tree[0], DOWN).shift(1 * DOWN + 1 * LEFT)
        self.play(Write(best_text))

        # Warte einen Moment, bevor der grüne Kreis erscheint
        self.wait(1)

        # Ziehe einen Kreis um den gesamten Baum mit der Beschriftung "BEST"
        best_circle = Circle(radius=2.25, color=GREEN, stroke_width=4).move_to(third_tree[0], DOWN).shift(2 * DOWN + 1 * LEFT)
        self.play(Create(best_circle))

        self.wait(3)

        # Rückgängig machen der Animationen
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def create_decision_tree(self, start_pos):
        # Initialize variables for node radius, base angle, and length reduction factor
        node_radius = 0.15
        base_angle = 70 * DEGREES
        length_reduction_factor = 0.5

        center_node = Circle(radius=node_radius, color=WHITE).move_to(start_pos)

        # First level of nodes and arrows with a wider angle
        first_nodes, first_arrows = self.add_branches(center_node, start_pos, angle=base_angle,
                                                      length=2 * length_reduction_factor)

        second_nodes = []
        second_arrows = []
        for node in first_nodes:
            # Second level of nodes and arrows with the standard angle
            new_nodes, new_arrows = self.add_branches(node, node.get_center(), angle=45 * DEGREES,
                                                      length=1.5 * length_reduction_factor)
            second_nodes.extend(new_nodes)
            second_arrows.extend(new_arrows)

        third_nodes = []
        third_arrows = []
        for node in second_nodes:
            # Third level of nodes and arrows, additional level compared to AdaBoost
            new_nodes, new_arrows = self.add_branches(node, node.get_center(), angle=30 * DEGREES,
                                                      length=1 * length_reduction_factor)
            third_nodes.extend(new_nodes)
            third_arrows.extend(new_arrows)

        return first_nodes

    def add_branches(self, parent_node, start_pos, angle, length):
        nodes = []
        arrows = []

        right_dir = np.array([np.sin(angle), -np.cos(angle), 0])
        left_dir = np.array([-np.sin(angle), -np.cos(angle), 0])

        right_pos = start_pos + length * right_dir
        left_pos = start_pos + length * left_dir

        right_node = Circle(radius=0.15, color=WHITE).move_to(right_pos)
        left_node = Circle(radius=0.15, color=WHITE).move_to(left_pos)
        nodes.extend([right_node, left_node])

        arrow_to_right = Arrow(start_pos, right_pos, buff=0.1, color=WHITE)
        arrow_to_left = Arrow(start_pos, left_pos, buff=0.1, color=WHITE)
        arrows.extend([arrow_to_right, arrow_to_left])

        self.play(FadeIn(parent_node), GrowArrow(arrow_to_right), FadeIn(right_node), GrowArrow(arrow_to_left),
                  FadeIn(left_node), run_time=1)

        return nodes, arrows
    
class OrangeAndApple(Scene):
    def construct(self):
        # Erstelle die Überschrift "Merheitsentscheidung" und lasse sie erscheinen
        title = Text("Merheitsentscheidung", font_size=48)
        title.move_to(UP * 3)
        self.play(Write(title))

        # Warte einen Moment, bevor die Überschrift nach oben wandert
        self.wait(1)

        # Erstelle die Bilder für die Knotenpunkte der Bäume
        root_image = ImageMobject("../assets/Bagging/tree.png").scale(0.04)
        orange_image = ImageMobject("../assets/Bagging/orange.png").scale(0.04)
        apple_image = ImageMobject("../assets/Bagging/apple.png").scale(0.10)

        root_image_big = ImageMobject("../assets/Bagging/tree.png").scale(0.1)
        orange_image_big = ImageMobject("../assets/Bagging/orange.png").scale(0.1)
        apple_image_big = ImageMobject("../assets/Bagging/apple.png").scale(0.3)

        # Positioniere die Bilder für die Knotenpunkte des ersten Baums
        root_image1 = root_image.copy().move_to(UP * 1.5 + LEFT * 4)
        orange_image1 = orange_image.copy().move_to(UP * 0 + LEFT * 6)
        apple_image1 = apple_image.copy().move_to(UP * 0 + LEFT * 2)

        # Positioniere die Bilder für die Knotenpunkte des zweiten Baums
        root_image2 = root_image.copy().move_to(DOWN * 0.75)
        orange_image2 = orange_image.copy().move_to(DOWN * 2.25 + LEFT * 2)
        apple_image2 = apple_image.copy().move_to(DOWN * 2.25 + RIGHT * 2)

        # Positioniere die Bilder für die Knotenpunkte des dritten Baums
        root_image3 = root_image.copy().move_to(UP * 1.5 + RIGHT * 4)
        orange_image3 = orange_image.copy().move_to(UP * 0 + RIGHT * 2)
        apple_image3 = apple_image.copy().move_to(UP * 0 + RIGHT * 6)

        # Erstelle die Bilder für die Knotenpunkte des zentralen Baums
        root_image4 = root_image_big.copy().move_to(UP * 1.5)
        orange_image4 = orange_image_big.copy().move_to(DOWN * 2 + LEFT * 4)
        apple_image4 = apple_image_big.copy().move_to(DOWN * 2 + RIGHT * 4)

        # Führe eine Animation durch, um die Bilder langsam aufzubauen
        self.play(
            FadeIn(root_image1),
            FadeIn(orange_image1),
            FadeIn(apple_image1),
        )
        self.wait(2)

        self.play(    
            FadeIn(root_image2),
            FadeIn(orange_image2),
            FadeIn(apple_image2),
        )
        self.wait(2)

        self.play(
            FadeIn(root_image3),
            FadeIn(orange_image3),
            FadeIn(apple_image3),
        )
        self.wait(2)

        # Füge Pfeile vom Baum zur Orange und zum Apfel hinzu
        orange_arrow1 = Arrow(root_image1.get_bottom(), orange_image1.get_center(), buff=0.1, color=ORANGE)
        apple_arrow1 = Arrow(root_image1.get_bottom(), apple_image1.get_center(), buff=0.1, color=RED)

        orange_arrow2 = Arrow(root_image2.get_bottom(), orange_image2.get_center(), buff=0.1, color=ORANGE)
        apple_arrow2 = Arrow(root_image2.get_bottom(), apple_image2.get_center(), buff=0.1, color=RED)

        orange_arrow3 = Arrow(root_image3.get_bottom(), orange_image3.get_center(), buff=0.1, color=ORANGE)
        apple_arrow3 = Arrow(root_image3.get_bottom(), apple_image3.get_center(), buff=0.1, color=RED)

        orange_arrow4 = Arrow(root_image4.get_bottom(), orange_image4.get_center(), buff=0.1, color=ORANGE)
        apple_arrow4 = Arrow(root_image4.get_bottom(), apple_image4.get_center(), buff=0.1, color=RED)

        self.play(
            GrowArrow(orange_arrow1),
            GrowArrow(apple_arrow1),
            GrowArrow(orange_arrow2),
            GrowArrow(apple_arrow2),
            GrowArrow(orange_arrow3),
            GrowArrow(apple_arrow3)
        )

        # Füge grüne Kreise über die Orange 1, Apple 2 und Orange 3 hinzu
        green_circle1 = Circle(radius=0.6, color=GREEN).move_to(orange_image1.get_center())
        green_circle2 = Circle(radius=0.6, color=GREEN).move_to(apple_image2.get_center())
        green_circle3 = Circle(radius=0.6, color=GREEN).move_to(orange_image3.get_center())
        green_circle4 = Circle(radius=2, color=GREEN).move_to(orange_image4.get_center())

        self.play(
            FadeIn(green_circle1),
            run_time=0.5
        )
        self.wait(1.5)

        self.play(
            FadeIn(green_circle2),
            run_time=0.5
        )
        self.wait(1)

        self.play(
            FadeIn(green_circle3),
            run_time=0.5
        )
        self.wait(1)

        self.play(FadeOut(title), FadeOut(root_image1), FadeOut(orange_image1), FadeOut(apple_image1), FadeOut(root_image2), FadeOut(orange_image2), FadeOut(apple_image2), FadeOut(root_image3), FadeOut(orange_image3), FadeOut(apple_image3), FadeOut(orange_arrow1), FadeOut(apple_arrow1), FadeOut(orange_arrow2), FadeOut(apple_arrow2), FadeOut(orange_arrow3), FadeOut(apple_arrow3), FadeOut(green_circle1), FadeOut(green_circle2), FadeOut(green_circle3))

        # Schreibe "Die Mehrheit entscheidet" in der Mitte
        majority_decision = Text("Die Mehrheit entscheidet", font_size=36)
        self.play(
            Write(majority_decision)
        )
        self.wait(1)

        # Rückgängig machen der Animationen
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=1
        )

        self.play(
            FadeIn(root_image4),
            FadeIn(orange_image4),
            FadeIn(apple_image4),
        )

        self.wait(1)

        self.play(
            GrowArrow(orange_arrow4),
            GrowArrow(apple_arrow4),
        )

        self.wait(1)

        self.play(
            FadeIn(green_circle4),
            run_time=0.5
        )        

        red_x = Cross(apple_image4, color=RED)

        self.play(
            Create(red_x),
            run_time=0.5
        )

        self.wait(2)

        # Verblassen aller Elemente
        self.play(*[FadeOut(mob) for mob in self.mobjects])

        # Animiere den Schriftzug "Random Forest" als Überschrift
        random_forest_title = Text("Random Forest > Einzelner Baum", font_size=48)
        random_forest_title.move_to(UP * 3)
        self.play(Write(random_forest_title))

        # Warte einen Moment
        self.wait(1)

        # Animate the bullet points
        bullet_point1 = Text("Bessere Vorhersagen", font_size=24)
        bullet_point2 = Text("Beugt Overfitting vor", font_size=24)

        bullet_points = VGroup(bullet_point1, bullet_point2).arrange(DOWN, aligned_edge=LEFT)
        bullet_points.move_to(ORIGIN)

        for bullet_point in bullet_points:
            self.play(Write(bullet_point))
            self.wait(0.5)

        self.wait(2)

        # Verblassen aller Elemente
        self.play(*[FadeOut(mob) for mob in self.mobjects])

         # Initialisiere title_text als Instanzvariable
        self.title_text = Text("Einzelner großer Baum", font_size=48).move_to(ORIGIN)

        # Bewege "AdaBoost" an den oberen Bildschirmrand
        self.play(self.title_text.animate.to_edge(UP), run_time=3)
        self.wait(4)
        
        # Erstellung des Entscheidungsbaums
        self.create_decision_tree(self.title_text.get_bottom() + DOWN * 0.5)
        self.wait(4)   
        
        # Zeichnen des inkorrekten Zeichens
        self.draw_incorrect_sign()
        self.wait(1)

        # Verblassen aller Elemente
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def create_decision_tree(self, start_pos):
        center_node = Circle(radius=0.3, color=WHITE)
        center_node.move_to(start_pos)

        # Erhöhe den Winkel und die Länge der ersten Pfeile deutlich, um eine breitere Basis zu schaffen
        first_nodes, first_arrows = self.add_branches(center_node, start_pos, angle=80 * DEGREES, length=3)

        second_nodes = []
        second_arrows = []
        for node in first_nodes:
            new_nodes, new_arrows = self.add_branches(node, node.get_center(), angle=45 * DEGREES, length=2)
            second_nodes.extend(new_nodes)
            second_arrows.extend(new_arrows)

        # Verwende für die dritte Ebene einen kleineren Winkel und kürzere Länge
        for node in second_nodes:
            self.add_branches(node, node.get_center(), angle=30 * DEGREES, length=1.5)

        self.wait(2)

    def add_branches(self, parent_node, start_pos, angle, length):
        nodes = []
        arrows = []

        right_dir = np.array([np.sin(angle), -np.cos(angle), 0])
        left_dir = np.array([-np.sin(angle), -np.cos(angle), 0])

        right_pos = start_pos + length * right_dir
        left_pos = start_pos + length * left_dir

        right_node = Circle(radius=0.3, color=WHITE).move_to(right_pos)
        left_node = Circle(radius=0.3, color=WHITE).move_to(left_pos)
        nodes.extend([right_node, left_node])

        arrow_to_right = Arrow(start_pos, right_pos, buff=0.1, color=WHITE)
        arrow_to_left = Arrow(start_pos, left_pos, buff=0.1, color=WHITE)
        arrows.extend([arrow_to_right, arrow_to_left])

        self.play(FadeIn(parent_node), run_time=1)
        self.play(GrowArrow(arrow_to_right), FadeIn(right_node), run_time=1)
        self.play(GrowArrow(arrow_to_left), FadeIn(left_node), run_time=1)

        return nodes, arrows
    
    def draw_incorrect_sign(self):
        # Bestimme die Positionen für die Endpunkte des X
        start_pos_1 = np.array([-config.frame_width / 2 * 0.8, config.frame_height / 2 * 0.8, 0])
        end_pos_1 = np.array([config.frame_width / 2 * 0.8, -config.frame_height / 2 * 0.8, 0])
        
        start_pos_2 = np.array([-config.frame_width / 2 * 0.8, -config.frame_height / 2 * 0.8, 0])
        end_pos_2 = np.array([config.frame_width / 2 * 0.8, config.frame_height / 2 * 0.8, 0])
        
        # Erstelle die Linien für das X
        line_1 = Line(start_pos_1, end_pos_1, color=RED, stroke_width=10)
        line_2 = Line(start_pos_2, end_pos_2, color=RED, stroke_width=10)
        
        # Zeichne das X über den Baum
        self.play(Create(line_1), Create(line_2), run_time=1)
        self.wait(2)