import threading

import customtkinter
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog
from Models.parameter import Parameter
from utils.red_neu_util import RedNeuUtil

import os


class FrameScrollBar(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.label = customtkinter.CTkLabel(self)
        self.label.grid(row=0, column=0, padx=20)

    def set_content_frame(self, frame):
        frame.grid(row=0, column=0, sticky="nsew")


class MainWindow(customtkinter.CTk):
    eta_default = 0.5
    epochs_default = 100
    title_font = ('Roboto', 24)
    normal_font = ('Roboto', 10)

    def __init__(self) -> None:
        super().__init__()
        self.title("Red Neuronal - Perceptron")
        self._set_appearance_mode("dark")

        self.parameter = Parameter(self.eta_default, self.epochs_default)
        self.test = pd.read_csv('test/test.csv', header=None)
        self.red_neu_util = RedNeuUtil(self.parameter, self.test)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.pages_root = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.pages_root.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")

        ##PAGE INITIAL
        self.pages_buttons = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.pages_buttons.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.initial_frame = customtkinter.CTkFrame(self.pages_root)
        self.page_initial = customtkinter.CTkButton(self.pages_buttons, text="Parameters",
                                                    command=lambda: self.show_page(self.initial_frame))

        self.report_frame = customtkinter.CTkFrame(self.pages_root, corner_radius=0, fg_color="transparent")
        self.page_report = customtkinter.CTkButton(self.pages_buttons, text="Report",
                                                   command=lambda: self.show_page(self.report_frame))

        self.charts_frame = customtkinter.CTkFrame(self.pages_root, corner_radius=0, fg_color="transparent")
        self.page_charts = customtkinter.CTkButton(self.pages_buttons, text="Chars",
                                                   command=lambda: self.show_page(self.charts_frame))

        self.page_initial.grid(row=1, column=0, padx=10, pady=0, sticky="wn")
        self.page_report.grid(row=1, column=1, padx=10, pady=0, sticky="wn")
        self.page_charts.grid(row=1, column=2, padx=10, pady=0, sticky="wn")

        self.initial_frame.grid(row=1, column=0, padx=10, pady=50, sticky="nsew")
        self.report_frame.grid(row=1, column=0, padx=10, pady=50, sticky="ew")
        self.charts_frame.grid(row=1, column=0, padx=10, pady=50, sticky="nsew")

        # Param
        self.eta_frame = customtkinter.CTkFrame(self.initial_frame)
        self.eta_frame.grid(row=1, column=0, padx=10, pady=10, sticky="we")

        self.label_title_eta = customtkinter.CTkLabel(self.eta_frame, text="PARAMS",
                                                      font=self.title_font)
        self.label_title_eta.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.label_eta = customtkinter.CTkLabel(self.eta_frame, text="Eta: ")
        self.label_eta.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_eta = customtkinter.CTkEntry(self.eta_frame,
                                                textvariable=customtkinter.StringVar(
                                                    value=str(self.eta_default)))
        self.entry_eta.grid(row=1, column=1, padx=10, pady=(10, 0), sticky="ew")

        self.label_epoch = customtkinter.CTkLabel(self.eta_frame, text="Epochs: ")
        self.label_epoch.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entry_epoch = customtkinter.CTkEntry(self.eta_frame,
                                                  textvariable=customtkinter.StringVar(
                                                      value=str(self.epochs_default)))
        self.entry_epoch.grid(row=2, column=1, padx=10, pady=(10, 0), sticky="ew")

        # Progress
        self.bar_frame = customtkinter.CTkFrame(self.initial_frame)
        self.bar_frame.grid(row=1, column=1, padx=10, pady=10, sticky="news")
        self.label_title_progress = customtkinter.CTkLabel(self.bar_frame, text="Progress",
                                                           font=self.title_font)
        self.label_title_progress.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        self.progressbar = customtkinter.CTkProgressBar(self.bar_frame, orientation="horizontal", mode="determinate")
        self.progressbar.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")
        self.progressbar.set(0)
        self.label_progressbar = customtkinter.CTkLabel(self.bar_frame,
                                                        text="[INFO] Dale al boton 'start' para iniciar.")
        self.label_progressbar.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")

        # Button
        self.button = customtkinter.CTkButton(self.initial_frame, text="Start", command=self.button_callback)
        self.button.grid(row=4, column=0, padx=10, pady=10, sticky="news")
        self.show_page(self.initial_frame)

        self.load_button = customtkinter.CTkButton(self.initial_frame, text="Load CSV", command=self.load_csv)
        self.load_button.grid(row=5, column=0, padx=10, pady=10, sticky="news")

        pass

    def button_callback(self):
        self.load_button.configure(state="disabled")
        self.page_report.configure(state="disabled")
        self.page_charts.configure(state="disabled")
        self.parameter.eta = float(self.entry_eta.get())
        self.parameter.epochs = int(self.entry_epoch.get())
        self.red_neu_util = RedNeuUtil(self.parameter, self.test)
        threading.Thread(target=self.start_optimization).start()

    def load_csv(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filename:
            self.test = pd.read_csv(filename, header=None, delimiter=';')
            file_name_only = os.path.basename(filename)
            self.label_progressbar.configure(text=f"[INFO] CSV CARGADO: {file_name_only}")

    def start_optimization(self):
        self.label_progressbar.configure(text="[INFO] entrenando la red neuronal")
        self.progressbar.set(0.1)
        self.red_neu_util.init_optimization()
        self.progressbar.set(0.5)

        self.label_progressbar.configure(text="[INFO] graficando")
        self.put_the_chars(self.charts_frame)
        self.page_charts.configure(state="normal")
        self.progressbar.set(0.7)

        self.label_progressbar.configure(text="[INFO] reportando")
        self.show_report_simple(self.report_frame)
        self.page_report.configure(state="normal")
        self.progressbar.set(0.9)
        self.button.configure(state="normal")
        self.load_button.configure(state="normal")
        self.progressbar.stop()
        self.progressbar.set(1)
        self.label_progressbar.configure(text="[INFO] Listo, checa el resto de pestañas")

    def show_page(self, page):
        for child in self.pages_root.winfo_children():
            child.grid_forget()

        page.grid(row=0, column=0, sticky="nsew")

    def put_the_chars(self, parent):
        scrollbar_frame = FrameScrollBar(parent, width=700, height=600, corner_radius=0, fg_color="transparent")
        scrollbar_frame.grid(row=0, column=0, padx=10, pady=50, sticky="nsew")

        figures_frame = customtkinter.CTkFrame(scrollbar_frame)
        figures_frame.grid(row=0, column=0, sticky="nsew")

        for row, fig in enumerate(self.red_neu_util.generated_figure):
            figure_frame = customtkinter.CTkFrame(figures_frame)
            figure_frame.grid(row=row, column=0, sticky="nsew")
            self.show_figure_in_frame(fig, figure_frame)

    def show_figure_in_frame(self, fig, parent):
        canvas = FigureCanvasTkAgg(fig, master=parent)
        plt.close(fig)
        canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    def show_report_simple(self, parent):
        cards_frame = FrameScrollBar(parent, width=600, height=600, corner_radius=0, fg_color="transparent")
        cards_frame.grid(row=0, column=0, padx=20, pady=20)

        content_frame = customtkinter.CTkFrame(cards_frame)
        content_frame.grid(row=0, column=0, sticky="news")
        content_frame.grid_columnconfigure(0, weight=1)

        self.put_generations(self.red_neu_util.list_epoch[-1], content_frame, 0)
        self.put_generations(self.red_neu_util.list_epoch[0], content_frame, 1)

        cards_frame.grid_rowconfigure(0, weight=1)
        cards_frame.grid_columnconfigure(0, weight=1)

    def put_generations(self, epoch, parent, row):
        generation_frame = customtkinter.CTkFrame(parent, width=600)
        generation_frame.grid(row=row, column=0, pady=10, padx=10, sticky="ew")

        label_title_generation = customtkinter.CTkLabel(generation_frame, text=f"Generation {epoch.id} :",
                                                        font=self.title_font)
        label_title_generation.grid(row=0, column=0, pady=(10, 0), padx=10, sticky="w")
        generation_frame.grid_columnconfigure(0, weight=1)

        report_frame = customtkinter.CTkFrame(generation_frame, width=600)
        report_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nwes")
        report_frame.grid_columnconfigure(0, weight=1)

        label_info_norma = customtkinter.CTkLabel(report_frame, text=f"Norma error: {epoch.error_norma}")
        label_info_norma.grid(row=1, column=0, pady=(10, 0), padx=10, sticky="we")

        label_info_info_weights = customtkinter.CTkLabel(report_frame, text=f"Worst f(x): {epoch.weights.__str__()}")
        label_info_info_weights.grid(row=2, column=0, pady=(10, 0), padx=10, sticky="we")

        self.label_progressbar.configure(text=f"[INFO] Reportando:{epoch.id}")
