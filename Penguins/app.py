import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly
import palmerpenguins  # This package provides the Palmer Penguins dataset
import pandas as pd
import seaborn as sns
from shiny import reactive, render, req
import matplotlib.pyplot as plt


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

    # Add a horizontal line to sidebar
    ui.hr()

    # Use ui.input_checkbox_group() to create a checkbox group input to filter the species
    ui.input_checkbox_group(
        "selected_species_list",
        "Penguin Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Chinstrap"],
        inline=True,
    )
                            
    # Use ui.input_checkbox_group() to create a checkbox group input to filter the islands
    ui.input_checkbox_group(
        "selected_islands_list",
        "Penguin Islands",
        ["Torgersen", "Biscoe", "Dream"],
        selected=["Torgersen"],
        inline=True,
    )

    # Add a horizontal line to sidebar
    ui.hr()
    
    # Use ui.a() to add a hyperlink to the sidebar
    ui.a("Github", href="https://github.com/14dstcyr/cintel-02-data", target="blank")
    
    
# Create tables and plots displaying all data
## Data Table and Grid
with ui.layout_columns():  
    with ui.card():  
        ui.h2("Penguins Table")        
        @render.data_frame
        def Penguins_Table():
                return render.DataTable(penguins_df)
                    
    with ui.card():
        ui.h2("Penguins Grid")
        
        @render.data_frame
        def render_Penguin_Grid():
            return render.DataGrid(penguins_df)

# Create Histograms and Scatterplot

with ui.layout_columns():
    with ui.card():
        ui.h4("Penguin Histogram")

        @render_plotly
        def plotly_histogram():
            return px.histogram(penguins_df, x="species", color="species")
            
    with ui.card(full_screen=True):
        ui.card_header("Seaborn Histogram")

        palette = sns.color_palette("Set3")  # Choose a palette with 3 colors

        @render.plot(alt="Seaborn Histogram")
        def seaborn_histogram():
            histplot = sns.histplot(
                filtered_data(),
                x="body_mass_g",
                bins=input.seaborn_bin_count(),
                hue="species",
                palette=palette,
            )
            histplot.set_title("Penguins")
            histplot.set_xlabel("Body Mass (g)")  # Set x-axis label
            histplot.set_ylabel("Count")  # Set y-axis label
            return histplot
        
 
## Plotly Scatterplot
    with ui.card():
        ui.card_header()
        @render_plotly
        def plotly_scatterplot():
            return px.scatter(filtered_data(),
                          x="bill_length_mm",
                          y="body_mass_g",
                          color="species",
                          title="Penguin Scatterplot",
                          labels={"bill_length_mm": "Bill Length mm",
                                  "body_mass_g": "Body Mass g"},
                          size_max=20,
            )
            


# --------------------------------------------------------
# Reactive calculations and effects
# --------------------------------------------------------

# Add a reactive calculation to filter the data
# By decorating the function with @reactive, we can use the function to filter the data
# The function will be called whenever an input function used to generate that output changes.
# Any output that depends on the reactive function (e.g., filtered_data()) will be updated when the data changes.

@reactive.calc
def filtered_data():
    return penguins_df[penguins_df["species"].isin(input.selected_species_list())]
