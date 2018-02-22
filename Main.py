import matplotlib.pyplot as plt
import os
import tkinter.filedialog as filedialog
from tkinter import *
from tkinter.ttk import *
# from itertools import cycle
import importlib

from GUI import execute, NetListGenerator, Library


class Interface(object):
    def __init__(self):
        self.window = Tk()
        self.window.title('Platform')
        self.window.geometry('1200x500')

        self.label_topline = Label(self.window, text=Library.TITLE, font=('Arial', 20), width=30, height=2)

        self.label_parts = Label(self.window, text='parts:', font=('Arial', 0), width=16, height=2)
        self.parts_options = StringVar()
        self.parts_options_tuple = (Library.PARTS)
        self.parts_options.set(self.parts_options_tuple)
        self.lb_parts = Listbox(self.window, listvariable=self.parts_options, height=6, exportselection=False)

        self.label_simulation = Label(self.window, text='simulation:', font=('Arial', 0), width=16, height=2)
        self.simulation_options = StringVar()
        self.simulation_options_tuple = (Library.SIMULATION)
        self.simulation_options.set(self.simulation_options_tuple)
        self.lb_simulation = Listbox(self.window, listvariable=self.simulation_options,
                                             height=6, exportselection=False)

        self.label_TID_level = Label(self.window, text='TID level:', font=('Arial', 0), width=16, height=2)
        self.TID_options = StringVar()
        self.TID_options_tuple = ()
        self.TID_options.set(self.TID_options_tuple)
        self.lb_TID = Listbox(self.window, listvariable=self.TID_options,
                                      height=len(self.TID_options_tuple), exportselection=False)

        self.label_output_x = Label(self.window, text='X Label:', font=('Arial', 0), width=16, height=2)
        self.output_options_x = StringVar()
        self.output_options_tuple_x = ()
        self.output_options_x.set(self.output_options_tuple_x)
        self.lb_output_x = Listbox(self.window, listvariable=self.output_options_x,
                                           height=len(self.output_options_tuple_x), exportselection=False)

        self.label_output_y = Label(self.window, text='Y Label:', font=('Arial', 0), width=16, height=2)
        self.output_options_y = StringVar()
        self.output_options_tuple_y = ()
        self.output_options_y.set(self.output_options_tuple_y)
        self.lb_output_y = Listbox(self.window, listvariable=self.output_options_y,
                                         height=len(self.output_options_tuple_y), exportselection=False)

        self.button_import = Button(self.window, text='Import', width=15, height=2, command=self.import_hit)
        self.button_execute = Button(self.window, text='Execute', width=15, height=2, command=self.execute_hit)

        self.result_text = StringVar()
        self.label_result_text = Label(self.window, textvariable=self.result_text, font=('Arial', 12), width=80, height=5)

        self.netlist_filepath = relative_path('Netlist/test.cir')
        self.output_filepath = ''
        self.color_gen = cycle('bgrcmykw')
        return

    def import_hit(self):
        filename = filedialog.askopenfilename(initialdir=relative_path('Netlist'))
        # print(filename)
        f = open(filename, 'r')
        line = next(f)
        while line[0:5] != 'Title':
            line = next(f, None)
            if line is None:
                print('Missing title')
        title = line.split(':')[1].replace(' ', '').split('/')
        my_simulation = title[0]
        my_part = title[1]
        my_voltage_source = list()
        my_circuit_core = list()
        my_input = list()
        my_output = list()
        my_subcircuit = list()
        my_library = list()

        my_parameters = list()
        my_functions = list()

        line = next(f)
        while line is not None:
            if line.find('*Input Voltage Source') != -1:
                line = next(f)
                while line.find('*End Input Voltage Source') == -1:
                    if line is None:
                        print('Missing \'*End Input Voltage Source\', abort import')
                        return
                    elif line.find('*****') == -1:
                        my_voltage_source.append(line.replace('\n', ''))
                    line = next(f)
            elif line.find('*Circuit Core') != -1:
                line = next(f)
                while line.find('*End Circuit Core') == -1:
                    if line is None:
                        print('Missing \'*End Circuit Core\', abort import')
                        return
                    elif line.find('*****') == -1:
                        my_circuit_core.append(line.replace('\n', ''))
                    line = next(f)
            elif line.find('*Input') != -1:
                line = next(f)
                while line.find('*End Input') == -1:
                    if line is None:
                        print('Missing \'*End Input\', abort import')
                        return
                    elif line.find('*****') == -1:
                        my_input.append(line.replace('\n', ''))
                    line = next(f)
            elif line.find('*Output') != -1:
                line = next(f)
                while line.find('*End Output') == -1:
                    if line is None:
                        print('Missing \'*End Output\', abort import')
                        return
                    elif line.find('**') == -1 and line.find('.print') == -1:
                        my_output.append(line.replace('\n', ''))
                    line = next(f)
            elif line.find('*Subcircuit') != -1:
                line = next(f)
                while line.find('*End Subcircuit') == -1:
                    if line is None:
                        print('Missing \'*End Subcircuit\', abort import')
                        return
                    elif line.find('*****') == -1:
                        my_subcircuit.append(line.replace('\n', ''))
                    line = next(f)
            elif line.find('*Library') != -1:
                line = next(f)
                while line.find('*End Library') == -1:
                    if line is None:
                        print('Missing \'*End Library\', abort import')
                        return
                    elif line.find('*****') == -1:
                        my_library.append(line.replace('\n', ''))
                    line = next(f)
            line = next(f, None)
        f.close()
        # print(my_part)
        # print(my_voltage_source)
        # print(my_circuit_core)
        # print(my_input)
        # print(my_output)
        # print(my_subcircuit)
        # print(my_library)
        Library.PARTS.append(my_part)
        Library.PARTS = list(set(Library.PARTS))
        Library.save_name_to_json(Library.TITLE, Library.PARTS, Library.SIMULATION, Library.TID_LEVEL, Library.TID_LIST,
                          Library.EXCEL_FILE_PATH, Library.COL_NAME, Library.SHEET_NAME, Library.NUM_OF_PARAMETER)
        Library.INPUT_VOLTAGE_SOURCE[my_part] = my_voltage_source
        Library.CIRCUIT_CORE[my_part] = my_circuit_core
        Library.INPUT[my_part] = my_input
        Library.OUTPUT_OPTION[my_part] = my_output
        temp = dict()
        temp[my_simulation] = my_subcircuit
        Library.SUBCIRCUIT[my_part] = temp
        if Library.LIBRARY_JFET.get(my_part) is None:
            Library.LIBRARY_JFET[my_part] = []

        Library.save_library_to_json(Library.INPUT_VOLTAGE_SOURCE, Library.CIRCUIT_CORE, Library.SCALE,
                                      Library.FUNCTIONS, Library.INPUT, Library.OUTPUT_OPTION, Library.SUBCIRCUIT,
                                      Library.LIBRARY_TID_LEVEL_MODEL, Library.LIBRARY_JFET)
        self.refresh()
        return

    def execute_hit(self):
        # try:
        if self.input_check():
            part = self.lb_parts.get(self.lb_parts.curselection())
            simulation = self.lb_simulation.get(self.lb_simulation.curselection())
            TID_level = self.lb_TID.get(self.lb_TID.curselection())
            output_option_x = self.lb_output_x.get(self.lb_output_x.curselection())
            output_option_y = self.lb_output_y.get(self.lb_output_y.curselection())
            # if (part == Library.PART_LT1175):
            #     output_option = self.lb_output.get(self.lb_output.curselection())
            # else:
            #     output_option = Library.AD590_OUTPUT_OPTION[0]
            self.output_filepath = relative_path('Output/' + part + '_' + TID_level + '_test.txt')

            netListGenerator.generate(part, simulation, TID_level, output_option_x, output_option_y, self.output_filepath, self.netlist_filepath)
            my_result = execute.execute_module3(self.netlist_filepath)
            print(my_result)
            message = 'part: ' + part + ', TID level = ' + TID_level + '\n' + 'result file path = ' + self.output_filepath
            # message = my_result
            self.result_text.set(message)

            X_label, Y_label, X, Y = self.load_and_finalize_output(part, TID_level)
            self.plotfigure(X_label, Y_label, X, Y, part, simulation, TID_level)
        # except Exception as error:
        #     print(error)
        #     self.result_text.set('Error! Do you have ' + str(error) + ' data in excel?')
        return

    def refresh(self):
        importlib.reload(Library)
        self.parts_options_tuple = (Library.PARTS)
        self.parts_options.set(self.parts_options_tuple)
        self.lb_parts.selection_clear(0, len(self.parts_options_tuple))
        self.simulation_options_tuple = (Library.SIMULATION)
        self.simulation_options.set(self.simulation_options_tuple)
        self.lb_simulation.select_clear(0, len(self.simulation_options_tuple))
        self.TID_options_tuple = ()
        self.TID_options.set(self.TID_options_tuple)
        self.output_options_tuple_x = ()
        self.output_options_x.set(self.output_options_tuple_x)
        self.output_options_tuple_y = ()
        self.output_options_y.set(self.output_options_tuple_y)
        self.result_text.set('')
        return

    def input_check(self):
        if self.lb_TID.curselection() == () or \
                self.lb_parts.curselection() == () or \
                self.lb_simulation.curselection() == () or \
                self.lb_output_x.curselection() == () or \
                self.lb_output_y.curselection() == ():
            self.result_text.set('please check your input')
            return False
        self.result_text.set('in process, please wait...')
        return True

    def TID_option_update(self):
        cur_sim = self.lb_simulation.get(self.lb_simulation.curselection())
        self.TID_options_tuple = Library.TID_LIST[cur_sim]
        self.TID_options.set(self.TID_options_tuple)

    def part_onselect(self, evt):
        try:
            index = int(self.lb_parts.curselection()[0])
            part = self.lb_parts.get(index)
            self.output_options_tuple_x = (Library.OUTPUT_OPTION[part])
            self.output_options_x.set(self.output_options_tuple_x)
            self.output_options_tuple_y = (Library.OUTPUT_OPTION[part])
            self.output_options_y.set(self.output_options_tuple_y)
            # if value == Library.PART_LT1175:
            #     self.label_output.grid()
            #     self.lb_output.grid()
            # elif value == Library.PART_AD590:
            #     self.label_output.grid_remove()
            #     self.lb_output.grid_remove()
        except:
            pass
        return

    def simulation_onselect(self, evt):
        try:
            self.TID_option_update()
        except:
            pass
        return

    def start(self):
        # row 0
        self.label_topline.grid(row=0, columnspan=3)

        # row 1
        self.label_parts.grid(row=1)
        self.label_simulation.grid(row=1, column=1)
        self.label_TID_level.grid(row=1, column=2)
        self.label_output_x.grid(row=1, column=3)
        self.label_output_y.grid(row=1, column=4)

        # row 2
        self.lb_parts.grid(row=2)
        self.lb_simulation.grid(row=2, column=1)
        self.lb_TID.grid(row=2, column=2)
        self.lb_output_x.grid(row=2, column=3)
        self.lb_output_y.grid(row=2, column=4)

        # row 3
        self.button_import.grid(row=3, column=0)
        self.button_execute.grid(row=3, sticky='E', columnspan=3, pady=10)

        # row 4
        self.label_result_text.grid(row=4, column=0, columnspan=3)

        # bind onselect function with widget
        self.lb_parts.bind('<<ListboxSelect>>', self.part_onselect)
        self.lb_simulation.bind('<<ListboxSelect>>', self.simulation_onselect)

        # remove output option listbox
        # self.label_output_x.grid_remove()
        # self.lb_output_x.grid_remove()

        self.window.mainloop()
        return

    def load_and_finalize_output(self, part, TID_level):

        X_label = ''
        Y_label = ''
        XnY = []
        X = []
        Y = []
        f = open(self.output_filepath, 'r')
        # lines = f.readlines()

        # n = open(self.output_filepath, 'w')
        # n.write('part: ' + part + ', TID level = ' + TID_level + '\n')
        # n.writelines(lines)
        for line in f:
            line = line.strip('\n')
            my_line = line.split(' ')
            cnt = 0
            for word in my_line:
                if cnt < 2 and word != '':
                    if X_label == '':
                        X_label = word
                    elif Y_label == '':
                        Y_label = word
                    else:
                        try:
                            XnY.append(float(word))
                            cnt += 1
                        except:
                            cnt = cnt
        f.close()

        for i in range(len(XnY)):
            if i % 2 == 0:
                X.append(XnY[i])
            else:
                Y.append(XnY[i])
        return X_label, Y_label, X, Y

    def plotfigure(self, X_label, Y_label, X, Y, part, simulation, TID_level):
        # figure_num = {Library.PART_LT1175: 1,
        #               Library.PART_AD590: 2}
        # location = {Library.PART_LT1175: 'upper left',
        #               Library.PART_AD590: 'lower right'}
        plt.figure(part + simulation + ' X=' + X_label + ' Y=' + Y_label, figsize=(10,8))
        plt.plot(X, Y, next(self.color_gen), label="Part=" + part + "TID level=" + TID_level)
        plt.xlabel(X_label)
        plt.ylabel(Y_label)
        # plt.plot(X, Y, 'b*')
        plt.legend(loc='upper left')
        plt.show()
        return


def relative_path(path):
    dirname = os.path.dirname(os.path.realpath('__file__'))
    path = os.path.join(dirname, path)
    return os.path.normpath(path)


if __name__ == "__main__":
    interface = Interface()
    execute = execute.Execute()
    netListGenerator = NetListGenerator.NetListGenerator()
    interface.start()
