class Settings():
    """Settings used to control the GUI colors, texts, and dimensions."""

    def __init__(self):

        # For the main window
        self.MAIN_TITLE = "Intensity Generator V3.0"
        self.MAIN_WIDTH = 1_000
        self.MAIN_HEIGHT = 600
        self.MAIN_BG = 'Black'
        self.MAIN_TO_BAR = (4, 1)

        # For the interpolation and rounding
        self.ROUND_NUM_X = 1
        self.ROUND_NUM_Y = 0


        # For the figure
        self.X_VALS_DYNAMIC = []    # Saved clicked points
        self.Y_VALS_DYNAMIC = []
        self.POINTS_DYNAMIC = {}    # Saved clicked points and their interpolation type
        self.FINAL_ARRAY_X = []     # Final array of interpolated points
        self.FINAL_ARRAY_Y = []
        self.FIGURE_STEP_SIZE_DEFAULT = 0.1
        self.YLIM_DEFAULT_MIN = 0
        self.YLIM_DEFAULT_MAX = 80
        self.XLIM_DEFAULT_MIN = 0
        self.XLIM_DEFAULT_MAX = 100

        # For the input frames
        self.BUTTON_PADX = 5
        self.BUTTON_PADY = 5


    def reset_data(self):
        # Reset all the values
        self.POINTS_DYNAMIC = {}
        self.FINAL_ARRAY_X = []
        self.FINAL_ARRAY_Y = []
        self.X_VALS_DYNAMIC = []
        self.Y_VALS_DYNAMIC = []
        self.FIGURE_STEP_SIZE_DEFAULT = 0.1
        self.YLIM_DEFAULT_MIN = 0
        self.YLIM_DEFAULT_MAX = 80
        self.XLIM_DEFAULT_MIN = 0
        self.XLIM_DEFAULT_MAX = 100
