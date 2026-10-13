import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

kivy.require('2.3.0')

# KV Language string for the UI layout
KV_STRING = """
<TipCalculatorLayout>:
    orientation: 'vertical'
    padding: '20dp'
    spacing: '20dp'

    BoxLayout:
        size_hint_y: None
        height: '48dp'
        Label:
            text: 'Bill Amount:'
            font_size: '18sp'
            halign: 'left'
            valign: 'middle'
            text_size: self.size
        TextInput:
            id: bill_input
            text: '0.00'
            multiline: False
            halign: 'right'
            font_size: '18sp'
            input_filter: 'float'
            on_text: root.calculate()

    BoxLayout:
        size_hint_y: None
        height: '48dp'
        Label:
            text: 'Tip Percentage:'
            font_size: '18sp'
            halign: 'left'
            valign: 'middle'
            text_size: self.size
        Label:
            id: tip_percent_label
            text: '15%'
            size_hint_x: 0.4
            font_size: '18sp'
            halign: 'right'
            valign: 'middle'
            text_size: self.size

    Slider:
        id: tip_slider
        min: 0
        max: 50
        value: 15
        step: 1
        size_hint_y: None
        height: '48dp'
        on_value: root.calculate()

    # A separator line
    BoxLayout:
        size_hint_y: None
        height: '2dp'
        canvas:
            Color:
                rgba: 0.5, 0.5, 0.5, 1
            Rectangle:
                pos: self.pos
                size: self.size
    
    # Results section
    BoxLayout:
        orientation: 'vertical'
        padding: '10dp'
        spacing: '10dp'
        
        BoxLayout:
            size_hint_y: None
            height: '30dp'
            Label:
                text: 'Tip Amount:'
                font_size: '20sp'
                halign: 'left'
                text_size: self.size
            Label:
                id: tip_amount_display
                text: '$0.00'
                font_size: '20sp'
                halign: 'right'
                text_size: self.size
        
        BoxLayout:
            size_hint_y: None
            height: '40dp'
            Label:
                text: 'Total Amount:'
                font_size: '24sp'
                bold: True
                halign: 'left'
                text_size: self.size
            Label:
                id: total_amount_display
                text: '$0.00'
                font_size: '24sp'
                bold: True
                halign: 'right'
                text_size: self.size

"""

class TipCalculatorLayout(BoxLayout):
    """Root widget for the tip calculator."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Schedule the first calculation for the next frame to ensure all widgets are ready.
        Clock.schedule_once(lambda dt: self.calculate())

    def calculate(self):
        """Calculates the tip and total amount and updates the UI.
        This method is called whenever an input value changes.
        """
        try:
            bill_amount_str = self.ids.bill_input.text
            bill_amount = float(bill_amount_str) if bill_amount_str else 0.0
        except (ValueError, KeyError):
            # Handle cases where input is not a valid float or ids are not ready
            bill_amount = 0.0

        try:
            tip_percentage = self.ids.tip_slider.value
            self.ids.tip_percent_label.text = f"{int(tip_percentage)}%"
        except KeyError:
            # Handle case where slider is not ready
            tip_percentage = 15

        tip_amount = bill_amount * (tip_percentage / 100.0)
        total_amount = bill_amount + tip_amount

        try:
            # Use a generic currency symbol or none at all.
            # Here we use '$' for convention.
            self.ids.tip_amount_display.text = f"${tip_amount:.2f}"
            self.ids.total_amount_display.text = f"${total_amount:.2f}"
        except KeyError:
            # Widgets might not be ready yet on initial load, so we pass.
            pass

class TipCalculatorApp(App):
    """The main application class."""

    def build(self):
        """Builds the app's UI from the KV string."""
        Builder.load_string(KV_STRING)
        return TipCalculatorLayout()

if __name__ == '__main__':
    TipCalculatorApp().run()
