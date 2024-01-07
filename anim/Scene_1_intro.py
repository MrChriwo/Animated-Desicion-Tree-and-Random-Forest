from manim import * 
import os

class a_introduce_bob(Scene):
    
        def __init__(self, **kwargs):
            self.asset_path = os.path.join(os.getcwd(), "assets", "intro")
            super().__init__(**kwargs)
    
            
        def construct(self):
            # make scene background blue (same color as bank bg to make it look like it's the same scene)
            self.camera.background_color = "#BEEBF1"

            bank_asset = os.path.join(self.asset_path, "bank.jpg")
            bob_asset = os.path.join(self.asset_path, "bob.png")
            bank_employee = ImageMobject(bank_asset)
            bob = ImageMobject(bob_asset)
            header = Text("Bob", font="Montserrat", color=BLACK).scale(1.5)
            header.to_edge(UP)
            bob.next_to(header, DOWN)

            group = Group(bob, header)
            # move bob a bit upper to make a fluent animation with the bank
            group[0].shift(UP*1.2)
            group.center()

            # fade in bob
            self.play(FadeIn(group[0]))
            self.wait(0.8)
            # write the header text (bob)
            self.play(Write(group[1]))
            self.wait(1)
            # fade in the bank "background"
            self.play(FadeIn(bank_employee))
            self.wait(3)


class b_bob_and_customers(Scene):
        
        def __init__(self, **kwargs):
            self.asset_path = os.path.join(os.getcwd(), "assets", "intro")
            super().__init__(**kwargs)

        def construct(self):
            self.camera.background_color = "#BEEBF1"

            bank_asset = os.path.join(self.asset_path, "bank.jpg")
            customer_asset = os.path.join(self.asset_path, "customer.png")
            check = os.path.join(self.asset_path, "check.png")
            denied = os.path.join(self.asset_path, "denied.png")
            credit = os.path.join(self.asset_path, "credit.png")
            bank_employee = ImageMobject(bank_asset)
            customer = ImageMobject(customer_asset)

            # position the customer to the right of the bank employee
            customer.shift(RIGHT*3)
            customer.shift(UP*2.1)

            #scale and position checked 
            check = ImageMobject(check)
            check.scale(0.2)
            check.shift(DOWN*0.5)
            check.shift(RIGHT*1.3)

            #scale and position denied
            denied = ImageMobject(denied)
            denied.scale(0.8)
            denied.shift(DOWN*0.5)
            denied.shift(RIGHT*1.3)
            credit_1 = ImageMobject(credit)
            credit_2 = ImageMobject(credit)
            credit_1.scale(0.8)

            # grouping checked and denied credit
            checked_credit = Group(credit_1, check)
            denied_credit = Group(credit_2, denied)
            
            self.play(bank_employee.animate.scale(0.7).shift(LEFT*3))
            self.wait(1.2)


            self.play(FadeIn(customer))
            self.wait(1.2)
            # scale the credit check group down and move it down to the customer
            checked_credit.scale(0.5)
            checked_credit.shift(DOWN*1.2)
            checked_credit.shift(RIGHT*1.4)

            # place the denied credit check group to the right of the checked credit check group
            denied_credit.scale(0.4)
            denied_credit.next_to(checked_credit, RIGHT, buff=0.5)

            # animation time :) 
            self.play(FadeIn(checked_credit[0]))
            self.wait(0.8)
            self.play(FadeIn(checked_credit[1]))
            self.wait(1.1)
            self.play(FadeIn(*denied_credit))
            self.wait(1.1)
            self.play(FadeOut(*self.mobjects))
            self.wait(0.3)
            




