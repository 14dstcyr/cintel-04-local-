import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly
import palmerpenguins  # This package provides the Palmer Penguins dataset
import pandas as pd
import seaborn as sns
from shiny import App, reactive, render, req
from shiny.ui import output_code, output_plot
import matplotlib.pyplot as plt
from palmerpenguins import load_penguins

# Use the built-in function to load the Palmer Penguins dataset.
penguins_df = palmerpenguins.load_penguins()

# Name of Project Page
ui.page_opts(title="St_Cyr Penguin Data", fillable=False)

# Add a sidebar
with ui.sidebar(open="open"):  
    
    ui.h2("Sidebar")

    # Use ui.input_selectize() to create a dropdown input to choose a column
    ui.input_selectize(
        "Selected_Attribute",
        "Bill Length in Millimeters",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
    )
    
    # Use ui.input_numeric() to create a numeric input for the number of Plotly histogram bins
    ui.input_numeric("plotly_bin_count", "Number of Plotly Bins", 20)

    # Use ui.input_slider() to create a slider input for the number of Seaborn bins
    ui.input_slider("seaborn_bin_count", "Bin Count", 1, 100, 20)

    # Use ui.input_checkbox_group() to create a checkbox group input to filter the species
    ui.input_checkbox_group("selected_species_list", "Penguin Species",  ["Adelie", "Gentoo", "Chinstrap"], selected=["Chinstrap"],
        inline=True,
    )

    # Use ui.hr() to add a horizontal rule to the sidebar
    ui.hr()
    
    # Use ui.a() to add a hyperlink to the sidebar
    ui.a("Github", href="https://github.com/14dstcyr/cintel-02-data", target="blank")
    
    
# Create tables and plots displaying all data
## Data Table and Grid
with ui.layout_columns():  
    with ui.card(full_screen=False):  
        ui.h2("Penguins Table")        
        @render.data_frame
        def Penguins_Table():
                return render.DataTable(filtered_data())
                    
    with ui.card(full_screen=False):
        ui.h2("Penguins Grid")
        
        @render.data_frame
        def render_Penguin_Grid():
            return render.DataGrid(filtered_data())

app_ui = ui.page_fluid(
    ui.output_plot(
    "plot",
    click=True,  
    dblclick=True,  
    hover=True,  
    brush=True,  
),

"Click:"
output_code("clk", placeholder=True)
"Double Click:"
output_code("dblclk", placeholder=True)
"Hover:"
output_code("hvr", placeholder=True)
"Brush"
output_code("brsh", placeholder=True)
)
with ui.hold():
    @render.plot(alt="A histogram")
    def plot():
        df = penguins_df() 
        # df = load_penguins()
        mass = df["body_mass_g"]
        bill = df["bill_length_mm"]

        plt.scatter(mass, bill)
        plt.xlabel("Mass (g)")
        plt.ylabel("Bill Length (mm)")
        plt.title("Penguin Mass vs Bill Length")

    @render.text
    def clk():
        return input.plot_click()

    @render.text
    def dblclk():
        return input.plot_dblclick()

    @render.text
    def hvr():
        return input.plot_hover()

    @render.text
    def brsh():
        return input.plot_brush()
