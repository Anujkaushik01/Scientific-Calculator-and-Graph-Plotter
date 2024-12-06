import tkinter as tk
from tkinter import messagebox
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sympy as sp
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ScientificCalculatorConfig:

    """Configuration class for calculator settings."""
    DEFAULT_STYLE = {'font': ('sans-serif', 20, 'bold'), 
                     'bg_primary': '#293C4A',
                     'bg_secondary': '#3C3636',
                     'fg_primary': '#BBB',
                     'fg_secondary': '#000',
                     'highlight': '#db701f'}

    """Initialize calculator configuration.
    Args: precision (int): Number of decimal places for calculations,
          angle_mode (str): Angle calculation mode ('degrees' or 'radians')"""
    def __init__(self, precision: int = 8, angle_mode: str = 'degrees'):
        self.precision = precision
        self.angle_mode = angle_mode
        self.style = self.DEFAULT_STYLE

class MathExpressionEvaluator:

    """Safely evaluate mathematical expressions.
        Args: expression (str): Mathematical expression to evaluate
              precision (int): Number of decimal places to round
        Returns:str: Evaluated result"""
    @staticmethod
    def safe_evaluate(expression: str, precision: int = 8) -> str:
        try:
            x = sp.Symbol('x')
            safe_functions = {
                'abs': sp.Abs, 'sin': sp.sin, 'cos': sp.cos, 
                'tan': sp.tan, 'log': sp.log, 'ln': sp.log, 
                'exp': sp.exp, 'sqrt': sp.sqrt, 
                'factorial': sp.factorial}
            
            # Replace ln to log 
            expression = expression.replace('ln(', 'log(')
            
            expr = sp.sympify(expression, locals=safe_functions)
            result = float(expr.evalf())
            return f"{result:.{precision}f}"
        except Exception as e:
            logger.error(f"Expression evaluation error: {e}")
            return "ERROR"

class GraphPlotter:
    
    """Initialize graph plotter.
        Args: master: Parent tkinter widget
              figsize (tuple): Figure size
              dpi (int): Dots per inch for resolution"""
    def __init__(self, master, figsize: tuple = (5, 4), dpi: int = 100):
        self.fig, self.ax = plt.subplots(figsize=figsize, dpi=dpi)
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas_widget = self.canvas.get_tk_widget()
    
    """Plot a mathematical function.
        Args: expression (str): Function to plot"""
    def plot_function(self, expression: str) -> None:
        try:
            x_sym = sp.Symbol('x')
            
            safe_functions = {
                'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan,
                'log': sp.log, 'exp': sp.exp, 'sqrt': sp.sqrt}
            
            # Parse and convert to numpy-compatible function
            expr = sp.sympify(expression, locals=safe_functions)
            f = sp.lambdify(x_sym, expr, modules='numpy')
            
            # Generate plot data
            x = np.linspace(-10, 10, 400)
            y = f(x)
            
            # Clear previous plot and draw new one
            self.ax.clear()
            self.ax.plot(x, y, label=f"y = {expression}")
            self.ax.axhline(0, color='black', linewidth=0.5)
            self.ax.axvline(0, color='black', linewidth=0.5)
            self.ax.grid(True, linestyle='--', alpha=0.7)
            self.ax.legend()
            self.canvas.draw()
        
        except Exception as e:
            logger.error(f"Graph plotting error: {e}")
            self.ax.clear()
            self.ax.text(0.5, 0.5, f"Error: {str(e)}", 
                         fontsize=12, color='red', 
                         ha='center', va='center', 
                         transform=self.ax.transAxes)
            self.canvas.draw()

class ScientificCalculatorApp:
    """Main application class for Scientific Calculator and Graph Plotter."""

    # Initialize the main application. Args: root (tk.Tk): Root tkinter window 
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Scientific Calculator and Graph Plotter")
        self.root.geometry("600x600")
        
        self.config = ScientificCalculatorConfig()
        self.calc_operator = ""
        self.text_input = tk.StringVar()
        
        self._create_ui()
    
    def _create_ui(self):
        # Configure grid weights to make the application resizable
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=1)

        # Create a container for all frames
        container = tk.Frame(self.root)
        container.grid(row=1, column=0, sticky="nsew")
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        # Create navigation bar
        nav_bar = tk.Frame(self.root, bg="lightgray")
        nav_bar.grid(row=0, column=0, sticky="ew")

        # Create frames for calculator and graph plotter
        self.frame_calculator = tk.Frame(container, bg=self.config.style['bg_primary'])
        self.frame_graph = tk.Frame(container, bg=self.config.style['bg_primary'])

        for frame in (self.frame_calculator, self.frame_graph):
            frame.grid(row=0, column=0, sticky="nsew")

        # Navigation buttons
        tk.Button(nav_bar, text="Calculator", 
                  command=lambda: self._show_frame(self.frame_calculator)).grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        tk.Button(nav_bar, text="Graph Plot", 
                  command=lambda: self._show_frame(self.frame_graph)).grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        # Calculator Layout
        self._create_calculator_frame()
        self._create_graph_frame()

        # Show calculator frame by default
        self._show_frame(self.frame_calculator)
    
    def _create_calculator_frame(self):
        # Text display
        text_display = tk.Entry(self.frame_calculator, font=self.config.style['font'], 
                                textvariable=self.text_input, bd=5, insertwidth=5, 
                                bg='#BBB', justify='right')
        text_display.grid(row=0, column=0, columnspan=5, padx=10, pady=15, sticky="ew")

        # Button parameters
        button_params = {'bd':5, 'fg':self.config.style['fg_primary'], 
                         'bg':self.config.style['bg_secondary'], 
                         'font':self.config.style['font']}
        button_params_main = {'bd':5, 'fg':self.config.style['fg_secondary'], 
                              'bg':self.config.style['fg_primary'], 
                              'font':self.config.style['font']}

        # Configure grid weights
        for i in range(10):
            self.frame_calculator.grid_rowconfigure(i, weight=1)
        for i in range(5):
            self.frame_calculator.grid_columnconfigure(i, weight=1)

        # Button definitions 
        self._create_calculator_buttons(button_params, button_params_main)

    def _create_calculator_buttons(self, button_params, button_params_main):
        # Row 1
        tk.Button(self.frame_calculator, button_params, text='abs', 
                  command=lambda: self._button_click('abs(')).grid(row=1, column=0, sticky="nsew")
        tk.Button(self.frame_calculator, button_params, text='mod', 
                  command=lambda: self._button_click('%')).grid(row=1, column=1, sticky="nsew")
        tk.Button(self.frame_calculator, button_params, text='div', 
                  command=lambda: self._button_click('//')).grid(row=1, column=2, sticky="nsew")
        tk.Button(self.frame_calculator, button_params, text='x!', 
                  command=self._fact_func).grid(row=1, column=3, sticky="nsew")
        tk.Button(self.frame_calculator, button_params, text='e', 
                  command=lambda: self._button_click(str(math.e))).grid(row=1, column=4, sticky="nsew")
        # Row 2
        tk.Button(self.frame_calculator, button_params, text='sin', 
                  command=self._trig_sin).grid(row=2, column=0, sticky="nsew")
        tk.Button(self.frame_calculator, button_params, text='cos',
                  command=self._trig_cos).grid(row=2, column=1, sticky="nsew")
        tk.Button(self.frame_calculator, button_params, text='tan',
                  command=self._trig_tan).grid(row=2, column=2, sticky="nsew")
        tk.Button(self.frame_calculator, button_params, text='cot',
                  command=self._trig_cot).grid(row=2, column=3, sticky="nsew")
        tk.Button(self.frame_calculator, button_params, text='π',
                  command=lambda:self._button_click(str(math.pi))).grid(row=2, column=4, sticky="nsew")
        # Row 3
        tk.Button(self.frame_calculator, button_params, text='x\u00B2',
                  command=lambda:self._button_click('**2')).grid(row=3, column=0, sticky="nsew")
        tk.Button(self.frame_calculator, button_params, text='x\u00B3',
                  command=lambda:self._button_click('**3')).grid(row=3, column=1, sticky="nsew")
        tk.Button(self.frame_calculator, button_params, text='x^n',
                  command=lambda:self._button_click('**')).grid(row=3, column=2, sticky="nsew")
        tk.Button(self.frame_calculator, button_params, text='x\u207b\xb9',
                  command=lambda:self._button_click('**(-1)')).grid(row=3, column=3, sticky="nsew")
        tk.Button(self.frame_calculator, button_params, text='10^x', font=('sans-serif', 15, 'bold'),
                  command=lambda:self._button_click('10**')).grid(row=3, column=4, sticky="nsew")     
        # Row 4
        tk.Button(self.frame_calculator, button_params, text='\u00B2\u221A',
                  command=self._square_root).grid(row=4, column=0, sticky="nsew")
        tk.Button(self.frame_calculator, button_params, text='\u00B3\u221A',
                  command=self._third_root).grid(row=4, column=1, sticky="nsew")
        tk.Button(self.frame_calculator, button_params, text='\u221A',
                  command=lambda:self._button_click('**(1/')).grid(row=4, column=2, sticky="nsew")
        tk.Button(self.frame_calculator, button_params, text='log\u2081\u2080', font=('sans-serif', 16, 'bold'),
                  command=self._log_base_10).grid(row=4, column=3, sticky="nsew")
        tk.Button(self.frame_calculator, button_params, text='ln',
                  command=self._ln).grid(row=4, column=4, sticky="nsew")
        # Row 5
        tk.Button(self.frame_calculator, button_params, text='(',
                  command=lambda:self._button_click('(')).grid(row=5, column=0, sticky="nsew")
        tk.Button(self.frame_calculator, button_params, text=')',
                  command=lambda:self._button_click(')')).grid(row=5, column=1, sticky="nsew")  
        tk.Button(self.frame_calculator, button_params, text='\u00B1',
                  command=self._sign_change).grid(row=5, column=2, sticky="nsew")
        tk.Button(self.frame_calculator, button_params, text='%',
                  command=self._percent).grid(row=5, column=3, sticky="nsew")
        tk.Button(self.frame_calculator, button_params, text='e^x',
                  command=self._exp_func).grid(row=5, column=4, sticky="nsew")
        # Row 6
        tk.Button(self.frame_calculator, button_params_main, text='7',
                  command=lambda:self._button_click('7')).grid(row=6, column=0, sticky="nsew")
        tk.Button(self.frame_calculator, button_params_main, text='8',
                  command=lambda:self._button_click('8')).grid(row=6, column=1, sticky="nsew")
        tk.Button(self.frame_calculator, button_params_main, text='9',
                  command=lambda:self._button_click('9')).grid(row=6, column=2, sticky="nsew")
        tk.Button(self.frame_calculator, bd=5, fg='#000', font=('sans-serif', 20, 'bold'), text='DEL', 
                  command=self._button_delete, bg='#db701f').grid(row=6, column=3, sticky="nsew")
        tk.Button(self.frame_calculator, bd=5, fg='#000', font=('sans-serif', 20, 'bold'), text='AC', 
                  command=self._button_clear_all, bg='#db701f').grid(row=6, column=4, sticky="nsew")
        # Row 7
        tk.Button(self.frame_calculator, button_params_main, text='4',
                  command=lambda:self._button_click('4')).grid(row=7, column=0, sticky="nsew")
        tk.Button(self.frame_calculator, button_params_main, text='5',
                  command=lambda:self._button_click('5')).grid(row=7, column=1, sticky="nsew")
        tk.Button(self.frame_calculator, button_params_main, text='6',
                  command=lambda:self._button_click('6')).grid(row=7, column=2, sticky="nsew")
        tk.Button(self.frame_calculator, button_params_main, text='*',
                  command=lambda:self._button_click('*')).grid(row=7, column=3, sticky="nsew")
        tk.Button(self.frame_calculator, button_params_main, text='/',
                  command=lambda:self._button_click('/')).grid(row=7, column=4, sticky="nsew")
        # Row 8
        tk.Button(self.frame_calculator, button_params_main, text='1',
                  command=lambda:self._button_click('1')).grid(row=8, column=0, sticky="nsew")
        tk.Button(self.frame_calculator, button_params_main, text='2',
                  command=lambda:self._button_click('2')).grid(row=8, column=1, sticky="nsew")
        tk.Button(self.frame_calculator, button_params_main, text='3',
                  command=lambda:self._button_click('3')).grid(row=8, column=2, sticky="nsew")
        tk.Button(self.frame_calculator, button_params_main, text='+',
                  command=lambda:self._button_click('+')).grid(row=8, column=3, sticky="nsew")
        tk.Button(self.frame_calculator, button_params_main, text='-',
                  command=lambda:self._button_click('-')).grid(row=8, column=4, sticky="nsew")
        # Row 9 - special handling for equal button
        tk.Button(self.frame_calculator, button_params_main, text='0', 
                  command=lambda:self._button_click('0')).grid(row=9, column=0, sticky="nsew")
        tk.Button(self.frame_calculator, button_params_main, text='.', 
                  command=lambda:self._button_click('.')).grid(row=9, column=1, sticky="nsew")
        tk.Button(self.frame_calculator, button_params_main, text='EXP', font=('sans-serif', 16, 'bold'), 
                  command=lambda:self._button_click('*10**')).grid(row=9, column=2, sticky="nsew")
        tk.Button(self.frame_calculator, button_params_main, text='=', 
                  command=self._button_equal).grid(row=9, columnspan=2, column=3, sticky="nsew")

        # Number and operation buttons
        numbers_operators = [('7', '8', '9', 'DEL', 'AC'),
                             ('4', '5', '6', '*', '/'),
                             ('1', '2', '3', '+', '-'),
                             ('0', '.', 'EXP', '=', None)]
        
        for row_idx, row in enumerate(numbers_operators, start=6):
            for col_idx, btn_text in enumerate(row):
                if btn_text:
                    if btn_text in ('DEL', 'AC'):
                        btn_cmd = self._button_delete if btn_text == 'DEL' else self._button_clear_all
                        tk.Button(self.frame_calculator, button_params_main, text=btn_text, command=btn_cmd, 
                                  bg=self.config.style['highlight']).grid(row=row_idx, column=col_idx, sticky="nsew")
                    elif btn_text == '=':
                        tk.Button(self.frame_calculator, button_params_main, text='=', 
                                  command=self._button_equal).grid(row=row_idx, column=col_idx, columnspan=2, sticky="nsew")
                    elif btn_text == 'EXP':
                        tk.Button(self.frame_calculator, button_params_main, text='EXP', 
                                  command=lambda: self._button_click('*10**')).grid(row=row_idx, column=col_idx, sticky="nsew")
                    else:
                        tk.Button(self.frame_calculator, button_params_main, text=btn_text, 
                                  command=lambda x=btn_text: self._button_click(x)).grid(row=row_idx, column=col_idx, sticky="nsew")

    def _create_graph_frame(self):
        self.frame_graph.grid_columnconfigure(0, weight=1)
        self.frame_graph.grid_rowconfigure(2, weight=1)

        self.graph_input = tk.Entry(self.frame_graph, font=('Arial', 20))
        self.graph_input.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        plot_button = tk.Button(self.frame_graph, text="Plot", command=self._plot_graph)
        plot_button.grid(row=1, column=0, pady=10)

        self.graph_plotter = GraphPlotter(self.frame_graph)
        self.graph_plotter.canvas_widget.grid(row=2, column=0, sticky="nsew")

    def _show_frame(self, frame):
        frame.tkraise()

    '''Defining Buttons in Calculator frame.'''
    def _button_click(self, char):
        # Add a character to the current expression.
        self.calc_operator += str(char)
        self.text_input.set(self.calc_operator)

    def _button_clear_all(self):
        # Clear the entire expression.
        self.calc_operator = ""
        self.text_input.set("")

    def _button_delete(self):
        # Delete the last character.
        self.calc_operator = self.calc_operator[:-1]
        self.text_input.set(self.calc_operator)

    def _button_equal(self):
        result = MathExpressionEvaluator.safe_evaluate(self.calc_operator, precision=self.config.precision)
        self.text_input.set(result)
        self.calc_operator = result

    def _trig_sin(self):
        try:
            angle = float(self.calc_operator)
            result = str(round(math.sin(math.radians(angle)), 8))
            self.calc_operator = result
            self.text_input.set(result)
        except Exception as e:
            self.text_input.set("ERROR")
            logger.error(f"Sine calculation error: {e}")

    def _trig_cos(self):
        try:
            angle = float(self.calc_operator)
            result = str(round(math.cos(math.radians(angle)), 8))
            self.calc_operator = result
            self.text_input.set(result)
        except Exception as e:
            self.text_input.set("ERROR")
            logger.error(f"Cosine calculation error: {e}")

    def _trig_tan(self):
        try:
            angle = float(self.calc_operator)
            # Check for special cases that cause tangent to be undefined
            if abs(angle % 180 - 90) < 1e-10:  # Handling angles close to 90, 270, etc.
                self.text_input.set("UNDEFINED")
                self.calc_operator = ""
                return
            result = str(round(math.tan(math.radians(angle)), 8))
            self.calc_operator = result
            self.text_input.set(result)
        except Exception as e:
            self.text_input.set("ERROR")
            logger.error(f"Tangent calculation error: {e}")

    def _trig_cot(self):
        try:
            angle = float(self.calc_operator)
            # Check for special cases that cause cotangent to be undefined
            if abs(angle % 180) < 1e-10:  # Handling angles close to 0, 180, 360, etc.
                self.text_input.set("UNDEFINED")
                self.calc_operator = ""
                return
            result = str(round(1/math.tan(math.radians(angle)), 8))
            self.calc_operator = result
            self.text_input.set(result)
        except Exception as e:
            self.text_input.set("ERROR")
            logger.error(f"Cotangent calculation error: {e}")

    def _square_root(self):
        try:
            # Check if the number is non-negative
            if float(self.calc_operator) >= 0:
                result = MathExpressionEvaluator.safe_evaluate(f"sqrt({self.calc_operator})")
                self.calc_operator = result
                self.text_input.set(result)
            else:
                self.text_input.set("ERROR")
        except Exception as e:
            self.text_input.set("ERROR")
            logger.error(f"Square root calculation error: {e}")

    def _log_base_10(self):
        try:
            value = float(self.calc_operator)
            result = str(round(math.log10(value), 8))
            self.calc_operator = result
            self.text_input.set(result)
        except Exception as e:
            self.text_input.set("ERROR")
            logger.error(f"Log10 calculation error: {e}")

    def _ln(self):
        try:
            value = float(self.calc_operator)
            result = str(round(math.log(value), 8))
            self.calc_operator = result
            self.text_input.set(result)
        except Exception as e:
            self.text_input.set("ERROR")
            logger.error(f"ln calculation error: {e}")

    def _exp_func(self):
        try:
            value = float(self.calc_operator)
            result = str(round(math.exp(value), 8))
            self.calc_operator = result
            self.text_input.set(result)
        except Exception as e:
            self.text_input.set("ERROR")
            logger.error(f"Exponential calculation error: {e}")

    def _third_root(self):
        try:
            result = MathExpressionEvaluator.safe_evaluate(f"({self.calc_operator})**(1/3)")
            self.calc_operator = result
            self.text_input.set(result)
        except Exception as e:
            self.text_input.set("ERROR")
            logger.error(f"Cube root calculation error: {e}")

    def _sign_change(self):
        try:
            # If the expression starts with a minus, remove it
            if self.calc_operator and self.calc_operator[0] == '-':
                result = self.calc_operator[1:]
            else:
                # Otherwise, add a minus sign
                result = '-' + self.calc_operator
            self.calc_operator = result
            self.text_input.set(result)
        except Exception as e:
            self.text_input.set("ERROR")
            logger.error(f"Sign change error: {e}")

    def _percent(self):
        try:
            result = MathExpressionEvaluator.safe_evaluate(f"{self.calc_operator}/100")
            self.calc_operator = result
            self.text_input.set(result)
        except Exception as e:
            self.text_input.set("ERROR")
            logger.error(f"Percentage calculation error: {e}")
    
    def _fact_func(self):
        try:
            result = MathExpressionEvaluator.safe_evaluate(f"factorial({self.calc_operator})")
            self.calc_operator = result
            self.text_input.set(result)
        except Exception as e:
            self.text_input.set("ERROR")
            logger.error(f"Factorial calculation error: {e}")

    ''' Plot button in Graph Plotter frame.'''
    def _plot_graph(self):
        try:
            expression = self.graph_input.get()
            self.graph_plotter.plot_function(expression)
        except Exception as e:
            messagebox.showerror("Plotting Error", str(e))
    

def main():
    root = tk.Tk()
    ScientificCalculatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
