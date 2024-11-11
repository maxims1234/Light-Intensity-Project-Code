"""
Limitations:
    - If you start plot with a polynomial, you cannot use the back button
    - y-axis is limited to 80 because of hardware LED limit
"""


"""
Importing libraries
"""
# Import the tkinter library and numpy. SettingsFile is custom script that contains static and dynamic variables
import tkinter as tk
import numpy as np
import SettingsFile
from tkinter import filedialog

# Implement the default Matplotlib key bindings as well as ttk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.figure import Figure
from tkinter import ttk




"""
Create the root object and instances of the settings object.
Also create the references to the variables in the GUI.
"""
# Create the root object
root = tk.Tk()
settings_object = SettingsFile.Settings()
root.geometry(f"{settings_object.MAIN_WIDTH}x{settings_object.MAIN_HEIGHT}")
root.title(settings_object.MAIN_TITLE)

# Create the default variables (custom tkinter StringVar values)
xlim_button_min = tk.StringVar()
xlim_button_max = tk.StringVar()
ylim_button_min = tk.StringVar()
ylim_button_max = tk.StringVar()
interpolation_type = tk.StringVar()
render_step = tk.StringVar()




"""
Create the functions that are used in the GUI.
"""
# Create the function that updates the plot
def refresh_everything():
    settings_object.FIGURE_STEP_SIZE_DEFAULT = float(render_step.get())
    update_lims()
    canvas.draw()

# Function to update the ylim and xlim
def update_lims():
    # For the xlims
    if int(xlim_button_min.get()) < settings_object.XLIM_DEFAULT_MAX:
        settings_object.XLIM_DEFAULT_MIN = int(xlim_button_min.get())
    else:
        second_input_frame_text1_input.delete(0, 'end')
        second_input_frame_text1_input.insert(0, settings_object.XLIM_DEFAULT_MIN)
    if int(xlim_button_max.get()) > settings_object.XLIM_DEFAULT_MIN:
        settings_object.XLIM_DEFAULT_MAX = int(xlim_button_max.get())
    else:
        second_input_frame_text2_input.delete(0, 'end')
        second_input_frame_text2_input.insert(0, settings_object.XLIM_DEFAULT_MAX)
    ax.set_xlim(settings_object.XLIM_DEFAULT_MIN, settings_object.XLIM_DEFAULT_MAX)

# Function that resets everything
def reset_all_data():
    # Reset the xlims
    settings_object.reset_data()
    ax.set_xlim(settings_object.XLIM_DEFAULT_MIN, settings_object.XLIM_DEFAULT_MAX)
    second_input_frame_text1_input.delete(0, 'end')
    second_input_frame_text1_input.insert(0, settings_object.XLIM_DEFAULT_MIN)
    second_input_frame_text2_input.delete(0, 'end')
    second_input_frame_text2_input.insert(0, settings_object.XLIM_DEFAULT_MAX)

    # Reset the ylims
    ax.set_ylim(settings_object.YLIM_DEFAULT_MIN, settings_object.YLIM_DEFAULT_MAX)
    first_input_frame_text1_input.delete(0, 'end')
    first_input_frame_text1_input.insert(0, settings_object.YLIM_DEFAULT_MIN)
    first_input_frame_text2_input.delete(0, 'end')
    first_input_frame_text2_input.insert(0, settings_object.YLIM_DEFAULT_MAX)

    # Reset step size
    fourth_input_frame_text1_input.delete(0, 'end')
    fourth_input_frame_text1_input.insert(0, settings_object.FIGURE_STEP_SIZE_DEFAULT)

    # Update the graph
    line.set_data(settings_object.FINAL_ARRAY_X, settings_object.FINAL_ARRAY_Y)
    canvas.draw()

# If start button is pressed
def lock_everything():
    # Disable the buttons
    first_input_frame_button1['state'] = 'disabled'
    first_input_frame_button2['state'] = 'normal'
    fourth_input_frame_button1['state'] = 'normal'
    second_input_frame_button1['state'] = 'disabled'
    second_input_frame_button2['state'] = 'disabled'
    fourth_input_frame_button2['state'] = 'disabled'

    # Disable the inputs
    second_input_frame_text1_input['state'] = 'disabled'
    second_input_frame_text2_input['state'] = 'disabled'

    # Highlight the stop button as green
    first_input_frame_button2.configure(bg='green')

    # Enable the click_id
    click_id = canvas.mpl_connect('button_press_event', onclick)

# Function to enable the buttons again
def unlock_everything():
    # Enable the buttons
    first_input_frame_button1['state'] = 'normal'
    first_input_frame_button2['state'] = 'disabled'
    fourth_input_frame_button1['state'] = 'disabled'
    second_input_frame_button1['state'] = 'normal'
    second_input_frame_button2['state'] = 'normal'
    fourth_input_frame_button2['state'] = 'normal'

    # Enable the inputs
    second_input_frame_text1_input['state'] = 'normal'
    second_input_frame_text2_input['state'] = 'normal'

    # Highlight the stop button back to normal
    first_input_frame_button2.configure(bg='SystemButtonFace')

    # Disable the click handler
    click_id = canvas.mpl_connect('button_press_event', onclick)
    canvas.mpl_disconnect(click_id)

# Function to detect clicks
def onclick(event):
    # Handle the data value
    if (event.xdata and event.ydata) != None:
        # Check if the data value is behind the last value
        if len(settings_object.X_VALS_DYNAMIC) != 0 and round(event.xdata, 0) <= settings_object.X_VALS_DYNAMIC[-1]:
            pass
        else:
            current_id = len(settings_object.POINTS_DYNAMIC)
            settings_object.POINTS_DYNAMIC[current_id] = {'x': round(event.xdata, 1), 'y': round(event.ydata, 0), 'T': interpolation_type.get()}

            # Plot the new point
            settings_object.X_VALS_DYNAMIC.append(settings_object.POINTS_DYNAMIC[current_id]['x'])
            settings_object.Y_VALS_DYNAMIC.append(settings_object.POINTS_DYNAMIC[current_id]['y'])

            # Interpolation
            interpolation_of_data(current_id)

            # Add the last data point
            settings_object.FINAL_ARRAY_X.append(settings_object.POINTS_DYNAMIC[current_id]['x'])
            settings_object.FINAL_ARRAY_Y.append(settings_object.POINTS_DYNAMIC[current_id]['y'])
            line.set_data(settings_object.FINAL_ARRAY_X, settings_object.FINAL_ARRAY_Y)
            # Function above automatically creates linear lines hence the angled interpolation
            canvas.draw()

# Function that does interpolation
def interpolation_of_data(data_id):
    # Make sure this is not the first data_id
    if data_id != 0:
        # Check if last data point was linear
        if settings_object.POINTS_DYNAMIC[data_id]['T'] == 'Linear':
            linear_x_vals = [settings_object.POINTS_DYNAMIC[data_id-1]['x'], settings_object.POINTS_DYNAMIC[data_id]['x']]
            linear_y_vals = [settings_object.POINTS_DYNAMIC[data_id-1]['y'], settings_object.POINTS_DYNAMIC[data_id]['y']]
            t = np.round(np.arange(linear_x_vals[0], linear_x_vals[1], settings_object.FIGURE_STEP_SIZE_DEFAULT), decimals=settings_object.ROUND_NUM_X)
            t_list = t.tolist()
            interpolated_values= np.round(np.interp(t, linear_x_vals, linear_y_vals), decimals=settings_object.ROUND_NUM_Y)
            interpolated_values_list = interpolated_values.tolist()
            settings_object.FINAL_ARRAY_X.extend(t_list[1:])
            settings_object.FINAL_ARRAY_Y.extend(interpolated_values_list[1:])

        # If polynomial
        elif settings_object.POINTS_DYNAMIC[data_id]['T'] == 'Polynomial':
            points_seen_x = []
            points_seen_y = []
            for i in range(len(settings_object.POINTS_DYNAMIC.keys())-1, -1, -1):
                if settings_object.POINTS_DYNAMIC[i]['T'] == 'Polynomial':
                    points_seen_x.append(settings_object.POINTS_DYNAMIC[i]['x'])
                    points_seen_y.append(settings_object.POINTS_DYNAMIC[i]['y'])
                else:
                    points_seen_x.append(settings_object.POINTS_DYNAMIC[i]['x'])
                    points_seen_y.append(settings_object.POINTS_DYNAMIC[i]['y'])
                    break
            points_seen_x = points_seen_x[::-1]
            points_seen_y = points_seen_y[::-1]

            # Apply the curve fitting
            z = np.polyfit(points_seen_x, points_seen_y, len(points_seen_x)-1)
            p = np.poly1d(z)
            t = np.round(np.arange(points_seen_x[0], points_seen_x[-1], settings_object.FIGURE_STEP_SIZE_DEFAULT), decimals=settings_object.ROUND_NUM_X)
            t_list = t.tolist()
            interpolated_values= np.round(p(t), decimals=settings_object.ROUND_NUM_Y)
            interpolated_values_list = interpolated_values.tolist()

            # Delete the previous values seen
            start = settings_object.FINAL_ARRAY_X.index(points_seen_x[0])
            settings_object.FINAL_ARRAY_X = settings_object.FINAL_ARRAY_X[:start+1]
            settings_object.FINAL_ARRAY_Y = settings_object.FINAL_ARRAY_Y[:start+1]

            # Add the new values
            settings_object.FINAL_ARRAY_X.extend(t_list[1:])
            settings_object.FINAL_ARRAY_Y.extend(interpolated_values_list[1:])

# Function to remove last point
def go_back():
    current_id = len(settings_object.POINTS_DYNAMIC)-1
    if current_id <= 0:
        pass
    else:
        if settings_object.POINTS_DYNAMIC[current_id]['T'] == 'Linear':
            index_last = settings_object.FINAL_ARRAY_X.index(settings_object.X_VALS_DYNAMIC[-2])
            del settings_object.POINTS_DYNAMIC[current_id]
            settings_object.X_VALS_DYNAMIC = settings_object.X_VALS_DYNAMIC[:-1]
            settings_object.Y_VALS_DYNAMIC = settings_object.Y_VALS_DYNAMIC[:-1]
            settings_object.FINAL_ARRAY_X = settings_object.FINAL_ARRAY_X[:index_last+1]
            settings_object.FINAL_ARRAY_Y = settings_object.FINAL_ARRAY_Y[:index_last+1]
        # CANNOT START WITH A POLYNOMIAL. START POINT CANNOT BE EARASED
        elif settings_object.POINTS_DYNAMIC[current_id]['T'] == 'Polynomial':
            start_id = None
            total_index = len(settings_object.POINTS_DYNAMIC)-1
            for i in range(len(settings_object.POINTS_DYNAMIC)-1, -1, -1):
                if settings_object.POINTS_DYNAMIC[i]['T'] != 'Polynomial':
                    start_id = i
                    break
            if start_id != None:
                for i in range(start_id+1, total_index+1):
                    del settings_object.POINTS_DYNAMIC[i]
                corresponding_number = settings_object.POINTS_DYNAMIC[start_id]['x']
                X_VALS_DYNAMIC_index = settings_object.X_VALS_DYNAMIC.index(corresponding_number)
                settings_object.X_VALS_DYNAMIC = settings_object.X_VALS_DYNAMIC[:X_VALS_DYNAMIC_index+1]
                settings_object.Y_VALS_DYNAMIC = settings_object.Y_VALS_DYNAMIC[:X_VALS_DYNAMIC_index+1]
                FINAL_ARRAY_X_index = settings_object.FINAL_ARRAY_X.index(corresponding_number)
                settings_object.FINAL_ARRAY_X = settings_object.FINAL_ARRAY_X[:FINAL_ARRAY_X_index+1]
                settings_object.FINAL_ARRAY_Y = settings_object.FINAL_ARRAY_Y[:FINAL_ARRAY_X_index+1]

        line.set_data(settings_object.FINAL_ARRAY_X, settings_object.FINAL_ARRAY_Y)
        canvas.draw()

# Function to save the graph as a CSV file labeled 'scores.csv' in the same folder as the python script
def save_file():
    new_x = []
    new_y = []
    index_s = None
    index_e = None

    # Remove duplicates (interpolation errors)
    temp_x = []
    temp_y = []
    for index, val in enumerate(settings_object.FINAL_ARRAY_X):
        if val not in temp_x:
            temp_x.append(val)
            temp_y.append(settings_object.FINAL_ARRAY_Y[index])
    settings_object.FINAL_ARRAY_X = temp_x
    settings_object.FINAL_ARRAY_Y = temp_y

    # Start the program on the far left
    offset = settings_object.FINAL_ARRAY_X[0]
    for i in range(len(settings_object.FINAL_ARRAY_X)):
        settings_object.FINAL_ARRAY_X[i] = settings_object.FINAL_ARRAY_X[i]-offset

    # Renders only what is see in the window (xlims, ylims).
    with open('data.txt', 'w') as output:
        output.write(f"{settings_object.FIGURE_STEP_SIZE_DEFAULT}\n")
        output.write(f"{int(settings_object.FIGURE_STEP_SIZE_DEFAULT*len(settings_object.FINAL_ARRAY_X))}\n")
        output.write(f"{len(settings_object.FINAL_ARRAY_X)}\n")
        for value in settings_object.FINAL_ARRAY_Y:
            output.write(f"{int(value)}\n")




"""
Create the actual interface
"""
############################################# (A) Creating the main frame ################################
# Create the grid (top-level)
frame1 = tk.Frame(master=root)
frame1.rowconfigure([0], weight=settings_object.MAIN_TO_BAR[0], uniform='Frame1Rows')
frame1.rowconfigure([1], weight=settings_object.MAIN_TO_BAR[1], uniform='Frame1Rows')
frame1.columnconfigure([0], weight=1, uniform='Frame1Columns')
frame1.pack(side="top", fill="both", expand=True)


############################################# (B) Creating the figure frame ################################
# Create the figure used in the plot. Set the default values so that it will show up
plotframe = tk.Frame(master=frame1)
plotframe.grid(row=0, column=0, sticky='nsew')
fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot()
line, = ax.plot(0)
ax.set_xlim(settings_object.XLIM_DEFAULT_MIN, settings_object.XLIM_DEFAULT_MAX)
ax.set_ylim(settings_object.YLIM_DEFAULT_MIN, settings_object.YLIM_DEFAULT_MAX)
ax.set_xlabel("time [s]")
ax.set_ylabel("f(t)")
ax.grid(True)
canvas = FigureCanvasTkAgg(fig, master=plotframe)  # A tk.DrawingArea.
canvas.draw()

# Pack the toolbar and the figure (packs into top level frame (1,1))
toolbar = NavigationToolbar2Tk(canvas, plotframe, pack_toolbar=False)
toolbar.update()
toolbar.pack(side=tk.BOTTOM, fill=tk.X)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


############################################# (C) Creating the bottom frame ################################
# Create the bottom bar frame (packs into top level frame (2,1))
frame_bottom = tk.Frame(master=frame1)
frame_bottom.rowconfigure([0], weight=1, uniform='FrameBottomRows')
frame_bottom.columnconfigure([0, 1], weight=1, uniform='FrameBottomColumns')
frame_bottom.grid(row=1, column=0, sticky='nsew')


############################################# (D-1) Creating the bottom left frame ################################
# Create the bottom bar frame left side
left_input_frame = tk.Frame(master=frame_bottom)
left_input_frame.rowconfigure([0, 1], weight=1, uniform='LeftInputFrameRows')
left_input_frame.columnconfigure([0], weight=1, uniform='LeftInputFrameColumns')
left_input_frame.grid(row=0, column=0, sticky='nsew')


############################################# (D-2) Creating the bottom left frame ylim, start, stop ################################
# Create the custom function input frame for buttons
first_input_frame = tk.Frame(master=left_input_frame)
first_input_frame.rowconfigure([0], weight=1, uniform='FirstInputFrameRows')
first_input_frame.columnconfigure([0, 1, 2, 3, 4, 5], weight=1, uniform='FirstInputFrameColumns')
first_input_frame_text1 = tk.Label(master=first_input_frame, text="Ylim (lower):")
first_input_frame_text1.grid(row=0, column=0, sticky='nsew')
first_input_frame_text1_input = tk.Entry(master=first_input_frame, textvariable=ylim_button_min)
first_input_frame_text1_input.insert(0, settings_object.YLIM_DEFAULT_MIN)
first_input_frame_text1_input['state'] = 'disabled'
first_input_frame_text1_input.grid(row=0, column=1, sticky='we')
first_input_frame_text2 = tk.Label(master=first_input_frame, text="Ylim (upper):")
first_input_frame_text2.grid(row=0, column=2, sticky='nsew')
first_input_frame_text2_input = tk.Entry(master=first_input_frame, textvariable=ylim_button_max)
first_input_frame_text2_input.insert(0, settings_object.YLIM_DEFAULT_MAX)
first_input_frame_text2_input['state'] = 'disabled'
first_input_frame_text2_input.grid(row=0, column=3, sticky='we')
first_input_frame_button1 = tk.Button(master=first_input_frame, text="START", command=lock_everything)
first_input_frame_button1.grid(row=0, column=4, sticky='nsew', padx=settings_object.BUTTON_PADX, pady=settings_object.BUTTON_PADY)
first_input_frame_button2 = tk.Button(master=first_input_frame, text="STOP", command=unlock_everything)
first_input_frame_button2['state'] = 'disabled'
first_input_frame_button2.grid(row=0, column=5, sticky='nsew', padx=settings_object.BUTTON_PADX, pady=settings_object.BUTTON_PADY)
first_input_frame.grid(row=0, column=0, sticky='nsew')


############################################# (D-3) Creating the bottom left frame xlim, reset, and refresh buttons ################################
# Create the custom xlim input frame and refresh button and reset button
second_input_frame = tk.Frame(master=left_input_frame)
second_input_frame.rowconfigure([0], weight=1, uniform='SecondInputFrameRows')
second_input_frame.columnconfigure([0, 1, 2, 3, 4, 5], weight=1, uniform='SecondInputFrameColumns')
second_input_frame_text1 = tk.Label(master=second_input_frame, text="Xlim (lower):")
second_input_frame_text1.grid(row=0, column=0, sticky='nsew')
second_input_frame_text1_input = tk.Entry(master=second_input_frame, textvariable=xlim_button_min)
second_input_frame_text1_input.insert(0, settings_object.XLIM_DEFAULT_MIN)
second_input_frame_text1_input.grid(row=0, column=1, sticky='we')
second_input_frame_text2 = tk.Label(master=second_input_frame, text="Xlim (upper):")
second_input_frame_text2.grid(row=0, column=2, sticky='nsew')
second_input_frame_text2_input = tk.Entry(master=second_input_frame, textvariable=xlim_button_max)
second_input_frame_text2_input.insert(0, settings_object.XLIM_DEFAULT_MAX)
second_input_frame_text2_input.grid(row=0, column=3, sticky='we')
second_input_frame_button1 = tk.Button(master=second_input_frame, text='REFRESH', command=refresh_everything)
second_input_frame_button1.grid(row=0, column=4, sticky='nsew', padx=settings_object.BUTTON_PADX, pady=settings_object.BUTTON_PADY)
second_input_frame_button2 = tk.Button(master=second_input_frame, text='RESET', command=reset_all_data)
second_input_frame_button2.grid(row=0, column=5, sticky='nsew', padx=settings_object.BUTTON_PADX, pady=settings_object.BUTTON_PADY)
second_input_frame.grid(row=1, column=0, sticky='nsew')


############################################# (E-1) Creating the bottom right frame ################################
# Create the bottom bar frame right side
right_input_frame = tk.Frame(master=frame_bottom)
right_input_frame.rowconfigure([0, 1], weight=1, uniform='RightInputFrameRows')
right_input_frame.columnconfigure([0], weight=1, uniform='RightInputFrameColumns')
right_input_frame.grid(row=0, column=1, sticky='nsew')


############################################# (E-2) Creating the bottom right frame interpolation and render ################################
# Create the custom function input frame
third_input_frame = tk.Frame(master=right_input_frame)
third_input_frame.rowconfigure([0], weight=1, uniform='ThirdInputFrameRows')
third_input_frame.columnconfigure([0, 1, 2], weight=1, uniform='ThirdInputFrameColumns')
third_input_frame_text1 = tk.Label(master=third_input_frame, text="Interpolation Type: ")
third_input_frame_text1.grid(row=0, column=0, sticky='e')
third_input_frame_interpolation_options = ttk.Combobox(third_input_frame, textvariable=interpolation_type, state='readonly')
third_input_frame_interpolation_options.set('Linear')
third_input_frame_interpolation_options['values'] = ('Linear', 'Polynomial')
third_input_frame_interpolation_options.bind("<<ComboboxSelected>>",lambda e: root.focus())
third_input_frame_interpolation_options.grid(row=0, column=1, sticky='we')
third_input_frame.grid(row=0,column=0,sticky='nsew')


############################################# (E-3) Creating the bottom right frame step size ################################
# Create the custom function input frame
fourth_input_frame = tk.Frame(master=right_input_frame)
fourth_input_frame.rowconfigure([0], weight=1, uniform='FourthInputFrameRows')
fourth_input_frame.columnconfigure([0, 1, 2], weight=1, uniform='FourthInputFrameColumns')
fourth_input_frame_button1 = tk.Button(master=fourth_input_frame, text='BACK', command=go_back)
fourth_input_frame_button1['state'] = 'disabled'
fourth_input_frame_button1.grid(row=0, column=0, sticky='nsw', padx=settings_object.BUTTON_PADX, pady=settings_object.BUTTON_PADY)
fourth_input_frame_text1 = tk.Label(master=fourth_input_frame, text="Step Size: ")
fourth_input_frame_text1.grid(row=0, column=0, sticky='e')
fourth_input_frame_text1_input = tk.Entry(master=fourth_input_frame, textvariable=render_step)
fourth_input_frame_text1_input.insert(0, settings_object.FIGURE_STEP_SIZE_DEFAULT)
fourth_input_frame_text1_input['state'] = 'disabled'
fourth_input_frame_text1_input.grid(row=0, column=1, sticky='we')
fourth_input_frame_button2 = tk.Button(master=fourth_input_frame, text='Save Data', command=save_file)
fourth_input_frame_button2.grid(row=0, column=2)
fourth_input_frame.grid(row=1, column=0, sticky='nsew')




"""
Main Loop Call
"""
tk.mainloop()
