from tkinter import *
from plot_trajectory import *


class MainWindow:
    def __init__(self, root):
        """
        Initializes the main window
        @param root: Toplevel widget object
        """
        self.root = root
        main_lbl = Label(root, text="Tank Ballistics", font=("Helvetica", 20), pady=5, padx=10)
        main_lbl.pack()

        select_lbl = Label(root, text="Select a tank to model its round's projectile motion", font=("Helvetica", 15),
                           pady=10, padx=1)
        select_lbl.pack()

        # Create drop down menu with the tanks that can be modelled
        drop_down_options = ['M1A1 Abrams', "Challenger 1", "M4A1 Sherman", "Churchill Mark IV"]
        self.variable = StringVar(root)
        self.variable.set(drop_down_options[0])  # sets default value
        options = OptionMenu(self.root, self.variable, *drop_down_options)
        options.pack()

        next_btn = Button(root, text="Next", command=self.enter_range_window, pady=1, padx=10)
        next_btn.pack()

        quit_btn = Button(root, text="Quit", font=("Helvetica", 16), command=root.destroy, pady=1, padx=10)
        quit_btn.pack(side=BOTTOM, anchor=SE)

    def enter_range_window(self):
        """
        Asks user for a range to a target
        """
        if self.variable.get() == "M1A1 Abrams":
            chosen_tank = M1A1
        elif self.variable.get() == "Challenger 1":
            chosen_tank = Challenger1
        elif self.variable.get() == "M4A1 Sherman":
            chosen_tank = M4A1
        else:
            chosen_tank = Churchill4

        # The max and min range are displayed so user knows what range can be entered
        chosen_tank_max_range = max_range(chosen_tank)
        chosen_tank_min_range = min_range(chosen_tank)

        enter_range_wd = Toplevel(self.root)
        enter_range_wd.geometry("400x220")
        chosen_lbl = Label(enter_range_wd, text="Tank Chosen: " + self.variable.get(), font=("Helvetica", 15), pady=10,
                           padx=10)
        chosen_lbl.pack()

        # Display entry box to enter range
        enter_key_lbl = Label(enter_range_wd, text="Enter range(m) to target:", font=("Helvetica", 14), pady=1, padx=1)
        enter_key_lbl.pack()

        entry_bar = Entry(enter_range_wd)
        entry_bar.pack()

        empty_lbl = Label(enter_range_wd, text="", font=("Helvetica", 14), pady=1, padx=30)
        empty_lbl.pack()

        # Display max and min range
        max_range_lbl = Label(enter_range_wd,
                              text="Max range for " + self.variable.get() + ": " + str(chosen_tank_max_range)
                                   + " m", font=("Helvetica", 14), pady=1, padx=1)
        max_range_lbl.pack()
        min_range_lbl = Label(enter_range_wd,
                              text="Min range for " + self.variable.get() + ": " + str(chosen_tank_min_range)
                                   + " m", font=("Helvetica", 14), pady=1, padx=1)
        min_range_lbl.pack()

        next_btn = Button(enter_range_wd, text="Next", command=
                          lambda: self.trajectory_stats_window(chosen_tank, entry_bar, enter_range_wd), pady=1, padx=10)
        next_btn.pack()

    def trajectory_stats_window(self, tank, entry_bar, enter_range_wd):
        """
        Displays info about the projectiles trajectory and displays the plotted trajectory
        @param tank: tank object that holds tank info
        @param entry_bar: entry bar widget so the entered range can be extracted
        @param enter_range_wd: enter_range window object, so it can be destroyed AFTER the range is extracted
                               from the entry bar widget
        """
        # Extract distance
        distance = str(entry_bar.get()).strip()
        enter_range_wd.destroy()
        if distance == "":
            distance = max_range(tank)

        # Display error window if an invalid range is entered
        try:
            distance = float(distance)
        except Exception:
            error_wd = Toplevel(self.root)
            error_wd.geometry("240x80")
            error_lbl = Label(error_wd, text="ERROR, please enter a number", font=("Helvetica", 16), pady=10,
                              padx=1)
            error_lbl.pack()
            quit_btn = Button(error_wd, text="Close", font=("Helvetica", 14), command=error_wd.destroy, pady=1,
                              padx=10)
            quit_btn.pack()
            return
        if distance > max_range(tank):
            error_wd = Toplevel(self.root)
            error_wd.geometry("240x80")
            error_lbl = Label(error_wd, text="ERROR target out of range", font=("Helvetica", 16), pady=10,
                                  padx=1)
            error_lbl.pack()
            quit_btn = Button(error_wd, text="Close", font=("Helvetica", 14), command=error_wd.destroy, pady=1,
                              padx=10)
            quit_btn.pack()
            return
        elif distance < min_range(tank):
            error_wd = Toplevel(self.root)
            error_wd.geometry("240x80")
            error_lbl = Label(error_wd, text="ERROR target too close", font=("Helvetica", 16), pady=10,
                                  padx=1)
            error_lbl.pack()
            quit_btn = Button(error_wd, text="Close", font=("Helvetica", 14), command=error_wd.destroy, pady=1,
                              padx=10)
            quit_btn.pack()
            return

        trajectory_stats_wd = Toplevel(self.root)

        # Display whether the gun has to be depressed or elevated to hit the target
        required_angle = get_angle(distance, tank)
        if required_angle > 0:
            stat_lbl_str = "Gun elevation required: " + str(required_angle) + " degrees"
        elif required_angle < 0:
            stat_lbl_str = "Gun depression required: " + str(required_angle) + " degrees"
        else:
            stat_lbl_str = "Gun angle required: 0 degrees"

        stat_lbl = Label(trajectory_stats_wd, text=stat_lbl_str, font=("Helvetica", 14), pady=10, padx=30)
        stat_lbl.pack()

        # Display the time the projectile stays in the air
        time_in_air = get_time(distance, tank)
        stat_lbl2 = Label(trajectory_stats_wd, text="Time in air: " + str(time_in_air) + " seconds",
                          font=("Helvetica", 14), pady=1, padx=30)
        stat_lbl2.pack()

        empty_lbl = Label(trajectory_stats_wd, text="", font=("Helvetica", 12), pady=1, padx=30)
        empty_lbl.pack()

        # Plot the trajectory when the user clicks this button
        next_btn = Button(trajectory_stats_wd, text="View shell trajectory", command=
                          lambda: [plot_trajectory(distance, tank), trajectory_stats_wd.destroy()],
                          pady=1, padx=10)
        next_btn.pack()
        empty_lbl = Label(trajectory_stats_wd, text="", font=("Helvetica", 5), pady=1, padx=30)
        empty_lbl.pack()


if __name__ == '__main__':
    root = Tk()
    root.title('Tank Ballistics Modelling')
    root.geometry("400x200")
    app = MainWindow(root)
    root.mainloop()
