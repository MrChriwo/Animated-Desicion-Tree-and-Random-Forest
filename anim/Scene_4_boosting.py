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

        # Alles außer der Hintergrundfarbe und Überschrift ausblenden
        self.play(*[FadeOut(obj) for obj in self.mobjects if obj not in [self.camera.background_color, self.title_text]], run_time=3)
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

    