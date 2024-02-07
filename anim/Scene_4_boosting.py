from manim import *

class Intro(Scene):
    def construct(self):
        # Hintergrundbild laden und einblenden
        background_image = ImageMobject("../assets/Boosting/background.jpg")
        background_image.scale_to_fit_height(config.frame_height)
        background_image.scale_to_fit_width(config.frame_width)
        self.play(FadeIn(background_image))
        self.wait(2)  

        # Haupttitel erstellen, etwas kleiner und unterstrichen
        title = Text("Boosting in Entscheidungsbäumen", font_size=68, color=BLUE, weight=BOLD).set_stroke(BLACK, width=0.5)
        title.underline = True  # Unterstreichung hinzufügen
        self.play(FadeIn(title))
        self.wait(1)  # Kurze Pause vor der nächsten Animation

        # Haupttitel nach oben verschieben, um Platz zu machen
        self.play(title.animate.to_edge(UP, buff=0.75))

        # Unterüberschrift erstellen
        sub_text = Text("Leistungsverbesserung", font_size=60, color=GREEN, weight=BOLD).set_stroke(BLACK, width=0.5)
        sub_text.next_to(title, DOWN, buff=1)

        # Pfeil korrekt positionieren und dicker machen
        arrow = Arrow(LEFT*0.5 + sub_text.get_left(), sub_text.get_left(), buff=5, color=RED, stroke_width=10)
        arrow.next_to(sub_text, LEFT, buff=0.2)

        # Unterüberschrift und Pfeil einblenden
        self.play(GrowArrow(arrow), FadeIn(sub_text))
        self.wait(2)  # Verlängerte Wartezeit für die Gesamtlänge

        # Ausrichtung überprüfen, um sicherzustellen, dass Haupttitel und Untertitel zusammen mittig sind
        group = VGroup(title, sub_text, arrow)
        group.move_to(ORIGIN)

        # Ausblendung aller Elemente am Ende
        self.play(FadeOut(group), FadeOut(background_image))
        self.wait(2)  # Abschlusswartezeit

class AdaBoost(Scene):

    def construct(self):
        self.camera.background_color = "#add8e6"
        
        # Initialisiere title_text als Instanzvariable
        self.title_text = Text("Adaptive Boosting", font_size=48).move_to(ORIGIN)
        
        # Schreibe den title_text und transformiere ihn dann in "AdaBoost"
        self.play(Write(self.title_text), run_time=5)
        self.wait(4)  # Verlängerte Wartezeit
        
        # Transformiere "Adaptive Boosting" zu "AdaBoost"
        ada_boost_text = Text("AdaBoost", font_size=48)
        self.play(Transform(self.title_text, ada_boost_text), run_time=3)
        self.wait(4)  # Verlängerte Wartezeit
        
        # Bewege "AdaBoost" an den oberen Bildschirmrand
        self.play(self.title_text.animate.to_edge(UP), run_time=3)
        self.wait(4)
        
        # Erstellung des Entscheidungsbaums
        self.create_decision_tree(self.title_text.get_bottom() + DOWN * 0.5)
        self.wait(4)  
        
        # Zeichnen des inkorrekten Zeichens
        self.draw_incorrect_sign()
        self.wait(4)
        
        # Löschen des Baumes und des X-Zeichens
        self.clear_tree_and_sign()

        # Erstellung mehrerer kleiner Bäume
        self.create_multiple_small_trees()
        self.wait(4)  

        # Zeichnen des korrekten Zeichens
        self.draw_correct_sign()
        self.wait(4)

        # Alles außer der Überschrift und dem Hintergrund ausblenden
        self.remove_all_except_title_and_background()

        # Füge die neue Sequenz hier hinzu
        self.construct_data_flow_sequence()
        
        # Alles außer der Hintergrundfarbe und Überschrift ausblenden
        self.play(*[FadeOut(obj) for obj in self.mobjects if obj != self.title_text], run_time=3)
        self.wait(3)

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

    def clear_tree_and_sign(self):
        # Alle Objekte außer der Überschrift ausblenden
        self.play(
            *[FadeOut(mob) for mob in self.mobjects if mob != self.title_text],
            run_time=2
        )

    def create_multiple_small_trees(self):
        positions = [
            UP * 1.5 + LEFT * 4,
            UP * 1.5 + RIGHT * 4,
            ORIGIN,
            DOWN * 1.5 + LEFT * 4,
            DOWN * 1.5 + RIGHT * 4
        ]
        
        for pos in positions:
            self.create_small_tree(pos)

    def create_small_tree(self, start_pos):
        # Größere Bäume erstellen
        center_node = Circle(radius=0.2, color=WHITE)
        center_node.move_to(start_pos)
        # Anpassungen für größere und diagonal platzierte Bäume
        angle = 45 * DEGREES
        length = 1.5  # Erhöhte Länge für größere Bäume

        right_dir = np.array([np.cos(angle), -np.sin(angle), 0])
        left_dir = np.array([-np.cos(angle), -np.sin(angle), 0])

        right_pos = start_pos + length * right_dir
        left_pos = start_pos + length * left_dir

        right_node = Circle(radius=0.2, color=WHITE).move_to(right_pos)
        left_node = Circle(radius=0.2, color=WHITE).move_to(left_pos)

        arrow_to_right = Arrow(start_pos, right_pos, buff=0.1, color=WHITE)
        arrow_to_left = Arrow(start_pos, left_pos, buff=0.1, color=WHITE)

        self.play(FadeIn(center_node), GrowArrow(arrow_to_right), FadeIn(right_node), GrowArrow(arrow_to_left), FadeIn(left_node), run_time=2)

    def draw_correct_sign(self):
        # Großes grünes Häkchen zeichnen
        start_pos = UP * 2 + LEFT * 2
        mid_pos = ORIGIN + DOWN * 0.5 + RIGHT * 0.5
        end_pos = UP * 3 + RIGHT * 4

        check_line1 = Line(start_pos, mid_pos, color=GREEN, stroke_width=10)
        check_line2 = Line(mid_pos, end_pos, color=GREEN, stroke_width=10)

        self.play(Create(check_line1), Create(check_line2), run_time=2)

    def remove_all_except_title_and_background(self):
        # Alle Objekte außer der Überschrift und dem Hintergrund ausblenden
        self.play(*[FadeOut(obj) for obj in self.mobjects if obj not in [self.camera.background_color, self.title_text]], run_time=3)

    def construct_data_flow_sequence(self):
        # Schriftzug "Training Data" oben links erstellen
        training_data_text = Text("Training Data", font_size=48).to_corner(UP + LEFT)
        self.play(Write(training_data_text), run_time=2)
        
        # Erster Baum und dessen Position
        first_tree_position = UP * 0.5 + LEFT * 5
        arrow_to_first_tree = Arrow(training_data_text.get_bottom(), first_tree_position, buff=0.1, color=BLUE, stroke_width=10)
        self.play(GrowArrow(arrow_to_first_tree), run_time=2)

        # Jetzt den restlichen Teil der Sequenz abspielen
        tree_positions = [first_tree_position, UP * 0.5, UP * 0.5 + RIGHT * 5]
       
        # Erhöhe den Abstand zwischen den Bäumen, um Überschneidungen zu vermeiden
        tree_positions = [UP * 0.5 + LEFT * 5, UP * 0.5, UP * 0.5 + RIGHT * 5]
        
        for i, pos in enumerate(tree_positions):
            # 1. Baum erstellen
            tree = self.create_small_tree(pos)
            self.wait(1)
            
            # Berechnung der Position für den Data-Schriftzug unterhalb des Baumes
            data_pos = pos + DOWN * 3
            data_text = Text("Data", font_size=48).move_to(data_pos)
            
            if i < len(tree_positions) - 1:
                # 2. Pfeil vom Baum zu "Data" Schriftzug unter ihm
                arrow_to_data = Arrow(pos, data_pos, buff=0.1, color=BLUE, stroke_width=10)
                self.play(GrowArrow(arrow_to_data), run_time=2)
                self.play(Write(data_text), run_time=2)
                
                # 3. Pfeil von "Data" zur Anfangsposition des nächsten Baumes
                next_tree_pos = tree_positions[i + 1]
                arrow_to_next_tree = Arrow(data_pos, next_tree_pos, buff=0.1, color=BLUE, stroke_width=10)
                self.play(GrowArrow(arrow_to_next_tree), run_time=2)
                
                # 4. Wartezeit vor Erstellung des nächsten Baums
                self.wait(1)
            else:
                # Letzter Baum: Nur Pfeil zu "Data" ohne weiteren Baum
                arrow_to_data = Arrow(pos, data_pos, buff=0.1, color=BLUE, stroke_width=10)
                self.play(GrowArrow(arrow_to_data), run_time=2)
                self.play(Write(data_text), run_time=2)

class GradientBoosting(Scene):
    def construct(self):
        self.camera.background_color = "#add8e6"

        # Initialize title_text as an instance variable
        self.title_text = Text("Gradient Boosting", font_size=48)

        # Write the title_text
        self.play(Write(self.title_text), run_time=1)

        # Move "Gradient Boosting" to the top of the screen
        self.play(self.title_text.animate.to_edge(UP), run_time=1)

        # Create the decision trees
        self.create_decision_trees()

    def create_decision_trees(self):
        # Add "Training Data" text to the top left corner
        training_data_text = Text("Training Data", font_size=36).to_edge(UP + LEFT)
        self.play(Write(training_data_text), run_time=1)

        # Add arrow from "Training Data" pointing downwards
        start_pos = training_data_text.get_bottom() + DOWN * 0.5
        end_pos = start_pos + DOWN * 1
        arrow = Arrow(start_pos, end_pos, buff=0.1, color=WHITE)
        self.play(GrowArrow(arrow), run_time=1)

        # Create the first decision tree
        first_tree = self.create_decision_tree(end_pos)

        # Add arrow from the first tree pointing to the right
        start_pos = first_tree[0].get_right()  # Get the right side of the first tree
        end_pos = start_pos + RIGHT * 3  # Move the end position to the right
        arrow = Arrow(start_pos, end_pos, buff=0.1, color=WHITE)
        self.play(GrowArrow(arrow), run_time=1)

        # Create the second decision tree
        second_tree = self.create_decision_tree(end_pos)

        # Add arrow from the second tree pointing to the right
        start_pos = second_tree[0].get_right()  # Get the right side of the second tree
        end_pos = start_pos + RIGHT * 3  # Move the end position to the right
        arrow = Arrow(start_pos, end_pos, buff=0.1, color=WHITE)
        self.play(GrowArrow(arrow), run_time=1)

        # Create the third decision tree
        third_tree = self.create_decision_tree(end_pos)

        # Draw a green checkmark at the end
        self.draw_green_checkmark()

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

    def draw_green_checkmark(self):
        # Großes grünes Häkchen zeichnen
        start_pos = UP * 2 + LEFT * 2
        mid_pos = ORIGIN + DOWN * 0.5 + RIGHT * 0.5
        end_pos = UP * 3 + RIGHT * 4

        check_line1 = Line(start_pos, mid_pos, color=GREEN, stroke_width=10)
        check_line2 = Line(mid_pos, end_pos, color=GREEN, stroke_width=10)

        self.play(Create(check_line1), Create(check_line2), run_time=2)

class CompareBoostingMethods(Scene):
    def construct(self):
        # Schriftzug "Ada Boost vs. Gradient Boost" in der Mitte platzieren
        title_text = Text("Ada Boost vs. Gradient Boost", font_size=48).move_to(ORIGIN)
        self.play(Write(title_text), run_time=2)
        self.play(title_text.animate.to_edge(UP), run_time=2)

        # Dünnen Streifen in der Mitte erstellen
        divider = Line(UP * 3, DOWN * 3, color=WHITE, stroke_width=2)
        self.play(Create(divider), run_time=2)

        # Erstelle fünf verschiedene Bäume für AdaBoost auf der linken Seite und gruppiere sie
        trees_group_left = self.create_varied_trees()
        self.wait(2)

        # Gruppierung der Bäume und Verschiebung in die untere linke Ecke
        trees_group_left.move_to(DOWN * 3 + LEFT * 6)
        self.wait(1)

        # Animation der Bäume auf der linken Seite mit sanftem Rutschen nach unten
        self.play(trees_group_left.animate.scale(0.5).move_to(DOWN * 2 + LEFT * 6), run_time=2)
        self.wait(1)  # Kurze Pause am Ende der Animation

        # Pause nach dem Erstellen der AdaBoost-Bäume
        self.wait(1)

        # Punkte für AdaBoost-Seite oben links erstellen und animieren
        points_left = [
            "Bäume mit mehr Gewichtung \n  (Aussagekraft und Wichtigkeit)",
            "Lernen aus den Daten der Vorgänger"
        ]
        self.animate_bullet_points_left(points_left, position=UP * 2 + LEFT * 4)  # Änderung der Position
        self.wait(5)

        # Erstelle drei Entscheidungsbäume für Gradient Boost auf der rechten Seite
        trees_group_right = self.create_decision_trees_right()
        self.wait(1)

        # Gruppierung der Bäume und Verschiebung in die untere rechte Ecke
        trees_group_right.move_to(DOWN * 3 + RIGHT * 6)

        # Animation der Bäume auf der rechten Seite mit sanftem Rutschen nach unten
        self.play(trees_group_right.animate.scale(0.5).move_to(DOWN * 2 + RIGHT * 6), run_time=2)
        self.wait(1)  # Kurze Pause am Ende der Animation

        # Punkte für Gradient Boost-Seite oben rechts erstellen und animieren
        points_right = [
            "Arbeitet an Fehlern des Modells",
            "Verbessert Vorhersagen durch \n Reduktion von Residuen."
        ]
        self.animate_bullet_points_right(points_right, position=UP * 2 + RIGHT * 4)  # Änderung der Position
        self.wait(4)  # Kurze Pause am Ende der Animation

    def create_decision_trees_right(self):
        # Positionen für die Entscheidungsbäume festlegen
        positions = [
            UP * 1.5 + RIGHT * 4,
            ORIGIN + RIGHT * 4,
            DOWN * 1.5 + RIGHT * 4
        ]

        # Bäume erstellen und zur Gruppierung hinzufügen
        trees_group = VGroup()
        size_factors = [0.3, 0.4, 0.5]  # Größenfaktoren für die Bäume
        for pos, size_factor in zip(positions, size_factors):
            tree = self.create_decision_tree_right(pos, size_factor)
            trees_group.add(tree)

        # Bäume nach Größe sortieren
        trees_group.submobjects.sort(key=lambda obj: obj.height, reverse=True)

        # Animation zum Aufbau der Bäume
        for tree in trees_group:
            self.play(GrowFromCenter(tree), run_time=1)

        return trees_group

    def create_decision_tree_right(self, start_pos, size_factor):
        # Baumgröße anhand des Faktors anpassen
        node_radius = 0.15 * size_factor
        base_angle = 70 * DEGREES
        length_reduction_factor = 0.5

        center_node = Circle(radius=node_radius, color=WHITE).move_to(start_pos)

        # Erste Ebene von Knoten und Pfeilen mit einem breiteren Winkel
        first_nodes, first_arrows = self.add_branches(center_node, start_pos, angle=base_angle,
                                                      length=2 * length_reduction_factor)

        second_nodes = []
        second_arrows = []
        for node in first_nodes:
            # Zweite Ebene von Knoten und Pfeilen mit dem Standardwinkel
            new_nodes, new_arrows = self.add_branches(node, node.get_center(), angle=45 * DEGREES,
                                                      length=1.5 * length_reduction_factor)
            second_nodes.extend(new_nodes)
            second_arrows.extend(new_arrows)

        third_nodes = []
        third_arrows = []
        for node in second_nodes:
            # Dritte Ebene von Knoten und Pfeilen
            new_nodes, new_arrows = self.add_branches(node, node.get_center(), angle=30 * DEGREES,
                                                      length=1 * length_reduction_factor)
            third_nodes.extend(new_nodes)
            third_arrows.extend(new_arrows)

        return VGroup(center_node, *first_nodes, *second_nodes, *third_nodes, *first_arrows, *second_arrows, *third_arrows)
    
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

    def create_varied_trees(self):
        # Positionen für die unterschiedlichen Bäume festlegen
        positions = [
            UP * 1.5 + LEFT * 4,
            UP * 0.5 + LEFT * 3,
            ORIGIN + LEFT * 2,
            DOWN * 0.5 + LEFT * 3,
            DOWN * 1.5 + LEFT * 4
        ]

        # Bäume erstellen und zur Gruppierung hinzufügen
        trees_group = VGroup()
        size_factors = [0.3, 0.4, 0.5, 0.6, 0.7]  # Größenfaktoren für die Bäume
        for pos, size_factor in zip(positions, size_factors):
            tree = self.create_tree(pos, size_factor)
            trees_group.add(tree)

        # Bäume nach Größe sortieren
        trees_group.submobjects.sort(key=lambda obj: obj.height, reverse=True)

        # Animation zum Aufbau der Bäume
        for tree in trees_group:
            self.play(GrowFromCenter(tree), run_time=1)

        return trees_group

    def create_tree(self, start_pos, size_factor):
        # Baumgröße anhand des Faktors anpassen
        node_radius = 0.15 * size_factor
        arrow_length = 0.5 * size_factor

        # Zentrale Knoten des Baumes erstellen
        center_node = Circle(radius=node_radius, color=WHITE)
        center_node.move_to(start_pos)

        # Zweige des Baumes hinzufügen
        right_dir = np.array([1, -1, 0])
        left_dir = np.array([-1, -1, 0])

        right_pos = start_pos + arrow_length * right_dir
        left_pos = start_pos + arrow_length * left_dir

        right_node = Circle(radius=0.15 * size_factor, color=WHITE).move_to(right_pos)
        left_node = Circle(radius=0.15 * size_factor, color=WHITE).move_to(left_pos)

        arrow_to_right = Arrow(start_pos, right_pos, buff=0.05, color=WHITE)
        arrow_to_left = Arrow(start_pos, left_pos, buff=0.05, color=WHITE)

        # Bäume gruppieren
        tree_group = VGroup(center_node, right_node, left_node, arrow_to_right, arrow_to_left)

        return tree_group

    def animate_bullet_points_left(self, points, position):
        bullet = "• "
        bullet_points = VGroup()
        prev_point = None
        for point in points:
            bullet_point = Text(f"{bullet}{point}", font_size=30, color=WHITE)
            if prev_point is not None:
                bullet_point.next_to(prev_point, DOWN, aligned_edge=LEFT)
            else:
                bullet_point.move_to(position)  # Neue Position
            bullet_points.add(bullet_point)
            self.play(Write(bullet_point), run_time=2)
            prev_point = bullet_point

        # Textgröße anpassen
        bullet_points.scale(0.8)

    def animate_bullet_points_right(self, points, position):
        bullet = "• "
        bullet_points = VGroup()
        prev_point = None
        for point in points:
            bullet_point = Text(f"{bullet}{point}", font_size=30, color=WHITE)
            if prev_point is not None:
                bullet_point.next_to(prev_point, DOWN, aligned_edge=LEFT)
            else:
                bullet_point.move_to(position)  # Neue Position
            bullet_points.add(bullet_point)
            self.play(Write(bullet_point), run_time=2)
            prev_point = bullet_point

        # Textgröße anpassen
        bullet_points.scale(0.8)