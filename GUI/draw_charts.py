#!/usr/bin/env python

import julia
from julia import Julia
import os

os.chdir("C:\\Users\\mazur\\AppData\\Local\\Programs\\Julia 1.5.3\\bin") #sciezka do folderu z julia
julia.install("C:\\Users\\mazur\\AppData\\Local\\Programs\\Julia 1.5.3\\bin\\julia.exe") # sciezka do julia.exe
j = julia.Julia(runtime = "C:\\Users\\mazur\\AppData\\Local\\Programs\\Julia 1.5.3\\bin\\julia.exe")
wykresy = j.include("C:\\Users\\mazur\\OneDrive\\Pulpit\\pakiety prezentacja\\wykresy.jl") #sciezka do funkcji wykresy
wykresy2 = j.include("C:\\Users\\mazur\\OneDrive\\Pulpit\\pakiety prezentacja\\wykresy2.jl") #sciezka do funkcji wykresy2

os.environ['KIVY_NO_ARGS'] = '1'
from kivy.app import App
from kivy.garden.matplotlib.backend_kivy import FigureCanvasKivy
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
import numpy as np
import matplotlib.pyplot as plt
import math


def make_list(plot_list:str):
    plot_list = plot_list[1:-1]
    index = plot_list.find(']')
    first = eval(plot_list[:index+1])
    second = eval(plot_list[index+1:])
    return [first, second]

def make_list2(plot_list:str):
    plot_list = plot_list[1:-1]
    index = plot_list.find(']')
    first = eval(plot_list[:index+1])
    plot_list = plot_list[index+1:]
    index = plot_list.find(']')
    second = eval(plot_list[:index+1])
    plot_list = plot_list[index+1:]
    index = plot_list.find(']')
    third = eval(plot_list[:index+1])
    plot_list = plot_list[index+1:]
    fourth = eval(plot_list)
    return [first, second, third, fourth]


class Charts(ScatterLayout):
    """
    Representation of the application drawing given function in the window
    """
    def __init__(self, **kwargs):
        """
        Layout of buttons, labels, text inputs, a checkbox and a canvas in the window
        """
        super(Charts, self).__init__(**kwargs)
        Window.clearcolor = (0.06, 0.33, 0.03, 1) #green
        Window.set_title("Wykresy")
        
        self.add_widget(Label(text='Wymiary środowiska: ', bold = True, size_hint = (0.09,0.05), pos_hint = {'top': 0.95, 'right': 0.2}, color = (1, 1, 0)))
        self.sizex = TextInput(multiline = True, size_hint = (0.05,0.05), pos_hint = {'top': 0.9, 'right': 0.15})
        self.add_widget(self.sizex)
        self.sizey = TextInput(multiline = True, size_hint = (0.05,0.05), pos_hint = {'top': 0.9, 'right': 0.22})
        self.add_widget(self.sizey)
        self.wrong_range = Label(font_size = '12sp', size_hint = (0.3,0.05), pos_hint = {'top': 0.75, 'right':0.3}, color = (0, 0, 0))
        self.add_widget(self.wrong_range)

       
        self.add_widget(Label(text='Liczba gołębi: ', bold = True, size_hint = (0.05,0.05), pos_hint = {'top': 0.95, 'right': 0.35}, color = (1, 1, 0)))
        self.n_gol = TextInput(font_size = '12sp', multiline = True, size_hint = (0.05,0.05), pos_hint = {'top': 0.9, 'right': 0.35})
        self.add_widget(self.n_gol)
        self.add_widget(Label(text='Liczba jastrzębi: ', bold = True, size_hint = (0.05,0.05), pos_hint = {'top': 0.95, 'right': 0.5}, color = (1, 1, 0)))
        self.n_jas = TextInput(font_size = '12sp', multiline = True, size_hint = (0.05,0.05), pos_hint = {'top': 0.9, 'right': 0.49})
        self.add_widget(self.n_jas)
        self.add_widget(Label(text='Liczba powtórzeń: ', bold = True, size_hint = (0.05,0.05), pos_hint = {'top': 0.95, 'right': 0.66}, color = (1, 1, 0)))
        self.p = TextInput(font_size = '12sp', multiline = True, size_hint = (0.05,0.05), pos_hint = {'top': 0.9, 'right': 0.67})
        self.add_widget(self.p)
        self.add_widget(Label(text='Pakiety żywnościowe: ', bold = True, size_hint = (0.05,0.05), pos_hint = {'top': 0.95, 'right': 0.85}, color = (1, 1, 0)))
        self.pack = TextInput(font_size = '12sp', multiline = True, size_hint = (0.05,0.05), pos_hint = {'top': 0.9, 'right': 0.85})
        self.add_widget(self.pack)

        self.add_widget(Label(text='Liczba chorych gołębi: ', bold = True, size_hint = (0.05,0.05), pos_hint = {'top': 0.85, 'right': 0.25}, color = (1, 1, 0)))
        self.ch_gol = TextInput(font_size = '12sp', multiline = True, size_hint = (0.05,0.05), pos_hint = {'top': 0.8, 'right': 0.25})
        self.add_widget(self.ch_gol)
        self.add_widget(Label(text='Liczba chorych jastrzębi: ', bold = True, size_hint = (0.05,0.05), pos_hint = {'top': 0.85, 'right': 0.5}, color = (1, 1, 0)))
        self.ch_jas = TextInput(font_size = '12sp', multiline = True, size_hint = (0.05,0.05), pos_hint = {'top': 0.8, 'right': 0.5})
        self.add_widget(self.ch_jas)
        self.add_widget(Label(text='Śmiertelność w procentach: ', bold = True, size_hint = (0.05,0.05), pos_hint = {'top': 0.85, 'right': 0.75}, color = (1, 1, 0)))
        self.deadliness = TextInput(font_size = '12sp', multiline = True, size_hint = (0.05,0.05), pos_hint = {'top': 0.8, 'right': 0.75})
        self.add_widget(self.deadliness)

        self.draw_button = Button(text = "WARIANT PODSTAWOWY", size_hint = (0.3, 0.05), pos_hint = {'top': 0.7, 'center_x': 0.2}, background_color = (1, 1, 1, 1), on_press = self.draw) #pink
        self.add_widget(self.draw_button)

        self.draw_button2 = Button(text = "WARIANT PONADPODSTAWOWY", size_hint = (0.3, 0.05), pos_hint = {'top': 0.7, 'center_x': 0.5}, background_color = (1, 1, 1, 1), on_press = self.draw2) #pink
        self.add_widget(self.draw_button2)

        self.draw_button3 = Button(text = "WARIANT PONADPODSTAWOWY 2", size_hint = (0.3, 0.05), pos_hint = {'top': 0.7, 'center_x': 0.8}, background_color = (1, 1, 1, 1), on_press = self.draw3) #pink
        self.add_widget(self.draw_button3)

        self.plot_canvas = FigureCanvasKivy(plt.gcf(), size_hint = (0.57,0.57), pos_hint = {'top': 0.6, 'center_x': 0.5})
        self.add_widget(self.plot_canvas)

    
    def draw(self, event):
        """
        Draw given functions on canvas

        @return: (None) if given data is incorrect (e.g. if functions or ranges are incorrect)
        """
        plt.clf()
        self.wrong_range.__setattr__("text", "")

        try:
            sizex = eval(self.sizex.text)
            sizey = eval(self.sizey.text)
            n_gol = eval(self.n_gol.text)
            n_jas = eval(self.n_jas.text)
            p = eval(self.p.text)
        except:
            self.wrong_range.__setattr__("text", "źle podane dane")
            return
        try:
            pack = eval(self.pack.text)
        except:
            pack = 1

        if not (sizex > 0 and sizey > 0 and n_gol >= 0 and n_jas >= 0 and p > 0):
            self.wrong_range.__setattr__("text", "źle podane dane")
            return
        
        if not (sizex % 3 == 0 and sizey % 3 == 0):
            self.wrong_range.__setattr__("text", "źle podane dane")
            return
    
        plots = make_list(wykresy(sizex, sizey, n_gol, n_jas, p, pack))
        xs = [i for i in range(len(plots[0]))]
        plt.plot(xs, plots[0], label='gołębie')
        plt.plot(xs, plots[1], label='jastrzębie')
        plt.legend()
        plt.gcf().canvas.draw_idle()


    def draw2(self, event):
        """
        Draw given functions on canvas

        @return: (None) if given data is incorrect (e.g. if functions or ranges are incorrect)
        """
        plt.clf()
        self.wrong_range.__setattr__("text", "")

        try:
            sizex = eval(self.sizex.text)
            sizey = eval(self.sizey.text)
            ch_gol = eval(self.ch_gol.text)
            ch_jas = eval(self.ch_jas.text)
            n_gol = eval(self.n_gol.text)
            n_jas = eval(self.n_jas.text)
            p = eval(self.p.text)
            deadliness = eval(self.deadliness.text)
        except:
            self.wrong_range.__setattr__("text", "źle podane dane")
            return

        if not (sizex > 0 and sizey > 0 and n_gol >= 0 and n_jas >= 0 and p > 0 and ch_gol >= 0 and ch_jas >= 0 and deadliness >= 0):
            self.wrong_range.__setattr__("text", "źle podane dane")
            return

        if not (sizex % 3 == 0 and sizey % 3 == 0):
            self.wrong_range.__setattr__("text", "źle podane dane")
            return
    
        plots = make_list2(wykresy2(sizex, sizey, n_gol, n_jas, ch_gol, ch_jas, p, deadliness))
        xs = [i for i in range(len(plots[0]))]
        plt.plot(xs, plots[0], label='gołębie')
        plt.plot(xs, plots[1], label='jastrzębie')
        plt.plot(xs, plots[2], label='chore gołębie')
        plt.plot(xs, plots[3], label='chore jastrzębie')
        plt.legend()
        plt.gcf().canvas.draw_idle()


    def draw3(self, event):
        """
        Draw given functions on canvas

        @return: (None) if given data is incorrect (e.g. if functions or ranges are incorrect)
        """
        plt.clf()
        self.wrong_range.__setattr__("text", "")

        try:
            sizex = eval(self.sizex.text)
            sizey = eval(self.sizey.text)
            ch_gol = eval(self.ch_gol.text)
            ch_jas = eval(self.ch_jas.text)
            n_gol = eval(self.n_gol.text)
            n_jas = eval(self.n_jas.text)
            p = eval(self.p.text)
            deadliness = eval(self.deadliness.text)
        except:
            self.wrong_range.__setattr__("text", "źle podane dane")
            return

        if not (sizex > 0 and sizey > 0 and n_gol >= 0 and n_jas >= 0 and p > 0 and ch_gol >= 0 and ch_jas >= 0 and deadliness >= 0):
            self.wrong_range.__setattr__("text", "źle podane dane")
            return

        if not (sizex % 3 == 0 and sizey % 3 == 0):
            self.wrong_range.__setattr__("text", "źle podane dane")
            return
    
        plots = make_list2(wykresy2(sizex, sizey, n_gol, n_jas, ch_gol, ch_jas, p, deadliness))
        xs = [i for i in range(len(plots[0]))]
        plot1 = []
        plot2 = []
        for i in range(len(plots[0])):
            plot1 += [plots[0][i]+plots[1][i]]
            plot2 += [plots[2][i]+plots[3][i]]

        plt.plot(xs, plot1, label='gołębie')
        plt.plot(xs, plot2, label='jastrzębie')
        plt.legend()
        plt.gcf().canvas.draw_idle()
            
    
    def exit_window(self, event):
        """
        Close the window
        """
        exit()
    

class MyApp(App):

    """
    Application for drawing given functions
    """

    def build(self):
        self.title = "Gołębie i jastrzębie"
        return Charts()

if __name__ == '__main__':

    MyApp().run()