from tkinter import *
from tkinter import messagebox
from Recognizer import *

# ------------------------------------------CONSTANTS/VARIABLES------------------------------------------
WIN_W = 1100
WIN_H = 1000
BACKGROUND = '#4d4d4d'
BACKGROUND2 = '#ffffff'
BTN_BG = '#1a1a1a'
TEXT_FG = '#f2f2f2'
ENT_BG = '#999999'

entries_nTs = []
entries_rS = []
frames_array = []
label_array = []

do_forever = False  # So there isn't an error when displaying the production frames.

root = Tk()
root.title('Reconocedor de Gramaticas')
root.geometry('1100x1000')
root.configure(bg=BACKGROUND)


# ------------------------------------------GENERAL_FUNCTIONS-------------------------------------------
def __show_error(t):
    msg = ''
    if t == 1:
        msg = 'Formato de número inválido'
    elif t == 2:
        msg = 'Error en la diligencia de alguna producción'
    elif t == 3:
        msg = 'Hilera no válida'
    else:
        msg = 'Unknown'
    messagebox.showinfo("ERROR", msg)


def __create_prod_frames(num):  # Called from validate_number
    global entries_nTs
    global entries_rS
    global frames_array
    entries_nTs.clear()
    entries_rS.clear()
    frames_array.clear()

    i = 0
    while i < num:  # While to save the frames and entries in list
        frm_aux = Frame(frm_1_bot, bg=BACKGROUND)
        frames_array.append(frm_aux)

        etr_nT = Entry(frames_array[i], bg='#999999', width=10)
        entries_nTs.append(etr_nT)

        etr_rightS = Entry(frames_array[i], bg='#999999')
        entries_rS.append(etr_rightS)

        i += 1

    for idx, frm in enumerate(frames_array):  # x is not gonna be used
        frm.grid(row=idx + 1, column=1)
        # Now to place within frames_array[idx]

        Label(frm, text=str(idx + 1) + '. <', bg=BACKGROUND, fg='#f2f2f2').grid(row=1, column=1)
        entries_nTs[idx].grid(row=1, column=2)
        Label(frm, text='> --> ', bg=BACKGROUND, fg='#f2f2f2').grid(row=1, column=3)
        entries_rS[idx].grid(row=1, column=4)


def __erase_prod_frames():
    global frames_array
    for fr in frames_array:
        fr.grid_forget()


def __display_first_stage():
    frm_1_top.place(anchor='n', relx=0.5, rely=0.1, relwidth=0.35, relheight=0.15)
    lbl_insert_len.grid(row=1, column=1)
    etr_grammar_len.grid(row=2, column=1)
    btn_confirm_num.grid(row=3, column=1)
    frm_1_bot.place(anchor='n', relx=0.5, rely=0.3, relwidth=0.35, relheight=0.7)


def __display_second_stage():
    __display_graph_pile()
    __display_operations()
    __display_reader()
    btn_new.place(anchor='se', relx=0.96, rely=0.96)
    btn_identify_g.place(anchor='s', relx=0.5, rely=0.96)


def __display_graph_pile():
    frm_2_left.place(anchor='w', relx=0.05, rely=0.5, relwidth=0.5, relheight=0.8)

    mein = get_recognizer_elements()
    input_symbols = mein[0]
    pile_symbols = mein[1]
    grammar = mein[2]
    grammar_l = grammar.get_all()

    # These for's will place the pile and input titles in the grid
    for i, sym in enumerate(input_symbols):
        Button(frm_2_left, state=DISABLED, text=sym, bg=BACKGROUND, fg=ENT_BG, width=5).grid(row=1, column=i + 2)
    for i, sym in enumerate(pile_symbols):
        Button(frm_2_left, state=DISABLED, text=sym, bg=BACKGROUND, fg=ENT_BG, width=7).grid(row=i + 2, column=1)

    # This for will place the operation number in their respective place in the grid
    for i, production in enumerate(grammar_l):
        NT = production.get_not_terminal()
        RiS = production.get_right_side()[0]
        row = pile_symbols.index(NT) + 2

        if RiS[0] == '<' or RiS == EMPTY_SEQUENCE:
            sel_set = grammar.get_selection_set(i)
            for terminal in sel_set:
                column = input_symbols.index(terminal) + 2
                Button(frm_2_left, state=DISABLED, text='#' + str(i + 1), bg=BACKGROUND, fg=TEXT_FG, width=5).grid(
                    row=row, column=column)
        else:
            column = input_symbols.index(RiS) + 2
            Button(frm_2_left, state=DISABLED, text='#' + str(i + 1), bg=BACKGROUND, fg=TEXT_FG, width=5).grid(row=row,
                                                                                                               column=column)

    # Now we place the transitions that have to do with terminals
    for term in input_symbols:
        if term in pile_symbols:
            column = input_symbols.index(term) + 2
            row = pile_symbols.index(term) + 2
            Button(frm_2_left, state=DISABLED, text='#0', bg=BACKGROUND, fg=TEXT_FG, width=5).grid(row=row,
                                                                                                   column=column)

    c = input_symbols.index(END_OF_SEQUENCE) + 2
    r = pile_symbols.index(EMPTY_PILE) + 2
    Button(frm_2_left, state=DISABLED, text='Acpt', bg=BACKGROUND, fg=TEXT_FG, width=5).grid(row=r, column=c)


def __display_operations():
    frm_2_mid.place(anchor='w', relx=0.6, rely=0.5, relwidth=0.15, relheight=0.8)
    global label_array
    label_array.clear()
    operations = get_operations()

    for idx, op in enumerate(operations):
        label_array.append(Label(frm_2_mid, text='#' + str(idx) + ': ' + op, bg=ENT_BG, fg=TEXT_FG))
        label_array[idx].grid(row=idx + 1, column=1)


def __display_reader():
    frm_2_right.place(anchor='w', relx=0.8, rely=0.5, relwidth=0.15, relheight=0.5)
    Label(frm_2_right, text='Para esta gramática,\n la hilera:', bg=ENT_BG, fg=TEXT_FG).place(anchor='n', relx=0.5,
                                                                                              rely=0.1)
    etr_str.place(anchor='n', relx=0.5, rely=0.3)
    btn_check_str.place(anchor='n', relx=0.5, rely=0.5)
    lbl_result.place(anchor='n', relx=0.5, rely=0.75)


def __start_over():
    clear_window(2)
    btn_new.place_forget()
    btn_identify_g.place_forget()
    __display_first_stage()

    global label_array
    for lay in label_array:
        lay.grid_forget()


#############################
def clear_window(stage):
    if stage == 1:
        frm_1_top.place_forget()
        frm_1_bot.place_forget()
    elif stage == 2:
        frm_2_left.place_forget()
        frm_2_mid.place_forget()
        frm_2_right.place_forget()


# -----------------------------------------------BTN_FUNCTIONS--------------------------------------------------
def show_help():
    UM = '1- El primer paso es determinar el número de producciones de la gramática. Ingrese el número en el ' \
         'cuadro de texto y presione Confirmar.\n' \
         '1.1- En cualquier momento puede ingresar otro número de producciones y presionar para confirmar, ' \
         'pero esto borrara el contenido de los cuadros de texto de las producciones.\n' \
         '2- Ingrese las producciones.\n' \
         '2.1- Para los lados izquierdos de estas no es necesario encerrar el no terminal entre <>, el programa' \
         ' lo hace automáticamente. Si ingresa <S> el no terminal resultante es <<S>>. \n' \
         '3- Presione el botón Crear. Esto mostrará el autómata de pila al lado izquierdo, sus operaciones ' \
         'en el medio, y el reconocedor de hileras al lado derecho. \n' \
         '4- Para reconocer una hilera ingrésela en el cuadro de texto a la derecha de la aplicación y precione' \
         ' Pertenece? Debajo de este se mostrará el resultado. \n' \
         '5- Si desea probar otra gramática presione Crear Nueva Gramatica.'
    messagebox.showinfo("Manual de Usuario", UM)


def show_grammar():
    tup = identify_grammar()
    head = tup[0]
    why = tup[1]
    body = ''
    for msg in why:
        body += '- ' + msg + '\n'
    messagebox.showinfo(head, body)


def validate_num():
    in_num = etr_grammar_len.get()
    try:
        if __name__ == '__main__':
            in_num = int(in_num)
            global do_forever
            if do_forever:
                __erase_prod_frames()
            __create_prod_frames(in_num)
            do_forever = True
            btn_create.place(anchor='s', relx=0.5, rely=0.95, relwidth=0.12, height=30)

    except:
        __show_error(1)


def take_grammar():
    try:
        not_terminals = []
        right_sides = []
        for i, x in enumerate(entries_nTs):  # Once again x won't be used :P
            NT = entries_nTs[i].get()
            RS = entries_rS[i].get()
            not_terminals.append(NT)
            right_sides.append(RS)
        create_grammar(not_terminals, right_sides)

        clear_window(1)
        __display_second_stage()


    except:
        __show_error(2)


def check_string():
    try:
        s = etr_str.get()
        if does_recognize(s):
            aux_s = 'ACEPTADA'
            color = '#256e10'
        else:
            aux_s = 'RECHAZADA'
            color = '#db2e25'

        lbl_result['fg'] = color
        lbl_result['text'] = 'es ' + aux_s
    except:
        __show_error(3)


# -----------------------------------------------MAIN--------------------------------------------------------

btn_help = Button(root, command=show_help, text='?', bg=BTN_BG, fg=TEXT_FG)  # button /1st screen
btn_help.place(anchor='ne', relx=0.98, rely=0.04, width=40)

# ################################-elements in stage 1-###############################################

frm_1_top = Frame(root, bg=BACKGROUND)
lbl_insert_len = Label(frm_1_top, text='Ingrese el número de producciones de la gramatica', bg=BACKGROUND, fg=TEXT_FG)
etr_grammar_len = Entry(frm_1_top, bg=ENT_BG)
btn_confirm_num = Button(frm_1_top, command=validate_num, text='Confirmar', bg=BTN_BG, fg=TEXT_FG)  # button /1st screen
frm_1_bot = Frame(root, bg=BACKGROUND)
btn_create = Button(frm_1_bot, command=take_grammar, text='Crear', bg=BTN_BG, fg=TEXT_FG)
__display_first_stage()

# ################################-elements in stage 2-################################################
frm_2_left = Frame(root, bg=ENT_BG)
frm_2_mid = Frame(root, bg=ENT_BG)
frm_2_right = Frame(root, bg=ENT_BG)
btn_identify_g = Button(root, command=show_grammar, text='S? Q? LL?', bg=BTN_BG, fg=TEXT_FG)
etr_str = Entry(frm_2_right, bg=BACKGROUND)
btn_check_str = Button(frm_2_right, command=check_string, text='Pertenece?', bg=BTN_BG, fg=TEXT_FG)
lbl_result = Label(frm_2_right, bg=ENT_BG)
btn_new = Button(root, command=__start_over, text='Crear nueva\n gramática', bg=BTN_BG, fg=TEXT_FG)

# ----------------------------END----------------------------------
root.mainloop()
