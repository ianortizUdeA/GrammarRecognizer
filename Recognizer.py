from Grammar import Grammar
from Grammar import Production

EMPTY_SEQUENCE = '¡'
END_OF_SEQUENCE = '¬'
EMPTY_PILE = '█'
__this_grammar = Grammar
__entry_symbols = []
__pile_symbols = []
__NT_range = {}

# ----------------------------------------------------------------------------------------
def __append_cause(reason, production, nT, terminal):  # TODO test
    # $ = production    ! = Not terminal    + = terminal
    messages = ['No es S porque la producción $ tiene la secuencia nula',  # 0
                'No es S porque la producción $ comienza con el no terminal !',  # 1
                'No es S porque para el no terminal ! 2 o más producciones comienzan con el terminal +',  # 2
                'No es Q porque la producción $ comienza con el no terminal !',  # 3
                'No es Q porque para el no terminal !, el terminal + no es disyunto con el conjunto de '
                'selección de la producción $',  # 4
                'No es LL(1) porque para el no terminal ! los conjuntos de seleccion de sus prodducciones '
                'no son disyuntos']  # 5
    m = messages[reason]
    i = m.find('$')
    if i != -1:
        m = m.replace('$', str(production + 1))

    i = m.find('!')
    if i != -1:
        m = m.replace('!', nT)

    i = m.find('+')
    if i != -1:
        m = m.replace('+', terminal)
    return m


# ----------------------------------------------------------------------------------------
def __has_duplicates(list_of_elems):
    # Checks if there are duplicates by copying the elements into a set and checking whether they're already there
    # Returns the first duplicate that encounters
    set_of_elems = set()
    for elem in list_of_elems:
        if elem in set_of_elems:
            return elem
        else:
            set_of_elems.add(elem)
    return '¬'


# ----------------------------------------------------------------------------------------
def identify_grammar():
    global __this_grammar
    is_S = True
    is_Q = True
    is_LL1 = True

    previous = __this_grammar.get_initial_symbol()
    same_not_terminal = []  # Saves the starting terminals of the same not terminal
    production_list = __this_grammar.get_all()  # The list of productions is taken in order to analyse it
    why_is_not = []  # List of strings to store the reasons why is not certain grammar

    # Let's check if it's LL(1)

    for idx, prod in enumerate(production_list):
        not_T = prod.get_not_terminal()
        right_side = prod.get_right_side()

        if not_T != previous:
            same_not_terminal.clear()

        if right_side[0] == EMPTY_SEQUENCE:
            is_S = False
            why_is_not.append(__append_cause(0, idx, not_T, right_side[0]))

            same_not_terminal = same_not_terminal + __this_grammar.get_selection_set(idx)
            aux_var = __has_duplicates(same_not_terminal)
            if aux_var != '¬':
                is_Q = False
                is_LL1 = False
                why_is_not.append(__append_cause(4, idx, not_T, aux_var))
                why_is_not.append(__append_cause(5, idx, not_T, aux_var))
                break

        if right_side[0][0] == '<':
            is_S = False
            is_Q = False
            why_is_not.append(__append_cause(1, idx, not_T, right_side[0]))
            why_is_not.append(__append_cause(3, idx, not_T, right_side[0]))

            same_not_terminal = same_not_terminal + __this_grammar.get_selection_set(idx)
            aux_var = __has_duplicates(same_not_terminal)
            if aux_var != '¬':
                is_LL1 = False
                why_is_not.append(__append_cause(5, idx, not_T, aux_var))
                break

        if right_side[0][0] in same_not_terminal:
            is_S = False
            is_Q = False
            is_LL1 = False

            why_is_not.append(__append_cause(2, idx, not_T, right_side[0]))
            why_is_not.append(__append_cause(4, idx, not_T, right_side[0]))
            why_is_not.append(__append_cause(5, idx, not_T, right_side[0]))
            break

        else:  # Here means that the first char is a new terminal
            same_not_terminal.append(right_side[0])
        previous = not_T

    for m in why_is_not:
        print(m)

    if is_S:
        return 'Es S', why_is_not
    if is_Q:
        return 'Es Q', why_is_not
    if is_LL1:
        return 'Es LL(1)', why_is_not
    else:
        return 'No es ni S, ni Q, ni LL(1)', why_is_not


# ----------------------------------------------------------------------------------------
def __set_symbols():
    global __entry_symbols
    global __pile_symbols
    __entry_symbols = __this_grammar.get_terminals()
    __entry_symbols.append('¬')

    __pile_symbols = __this_grammar.get_not_terminals()
    all_prods = __this_grammar.get_all()
    for prod in all_prods:
        right_side = prod.get_right_side()
        for i, st in enumerate(right_side):
            if i == 0:
                continue
            if st[0] != '<':
                __pile_symbols.append(st)
    __pile_symbols = list(dict.fromkeys(__pile_symbols))
    __pile_symbols.append(EMPTY_PILE)


# ----------------------------------------------------------------------------------------
def __set_NTs_range(productions):
    # The only purpose of this function it's to make the does_recognize function a bit more efficient
    global __NT_range

    for idx, prod in enumerate(productions):
        NT = prod.get_not_terminal()
        if NT in __NT_range:
            __NT_range[NT].append(idx)
        else:
            __NT_range[NT] = [idx]


# ----------------------------------------------------------------------------------------
def create_grammar(not_terminals, right_sides):  # TODO eliminar funciones de terminal
    production_list = []
    for i, x in enumerate(not_terminals):
        prod = Production(not_terminals[i], right_sides[i])
        production_list.append(prod)

    global __this_grammar
    __this_grammar = Grammar(production_list)
    __set_NTs_range(production_list)
    print(i)


# ----------------------------------------------------------------------------------------
def __replace_alpha(automaton_pile, RS):
    automaton_pile.pop()  # replace(alpha^r)
    for elem in reversed(RS):
        automaton_pile.append(elem)
    automaton_pile.pop()


def __replace_beta(automaton_pile, RS):
    automaton_pile.pop()  # replace(B^r)
    for elem in reversed(RS):
        automaton_pile.append(elem)


# ----------------------------------------------------------------------------------------
def does_recognize(input_str):
    global __this_grammar
    global __NT_range
    prod_list = __this_grammar.get_all()
    Accept = True

    automaton_pile = [EMPTY_PILE, __this_grammar.get_initial_symbol()]

    for c in input_str:
        continuer = True
        while continuer:    # In case we need to analyse the same character
            continuer = False

            on_top = automaton_pile[-1:]                # What's on top of the pile? THIS SLICING RETURNS A LIST
            on_top = on_top[0]
            if on_top[0] == '<':                        # If it a NT
                this_range = __NT_range[on_top]         # Range of positions for this production

                is_char_in_NT = False
                for pos in this_range:                  # the input char is searched for in he selection sets
                    if c in __this_grammar.get_selection_set(pos):      # of all productions with this NT
                        is_char_in_NT = True
                        RS = prod_list[pos].get_right_side()

                        if RS[0] == c:                  # Given the first symbol of the right side, action is taken
                            __replace_alpha(automaton_pile, RS)
                            break           # continue in the outer for

                        elif RS[0] == '<':
                            __replace_beta(automaton_pile, RS)
                            continuer = True            # Withhold
                            break

                        elif RS[0] == EMPTY_SEQUENCE:
                            automaton_pile.pop()
                            continuer = True            # Withhold
                            break
                if not is_char_in_NT:
                    print('it entered in 1')
                    Accept = False
                    break

            else:                       # If it's a terminal
                if c == on_top:  # If on top of the pile is an input symbol, and is equal to the char
                    print('entró aqui')
                    automaton_pile.pop()  # it's been read then we unstack and move on.
                    break       # Out of the while
                Accept = False
                print('it entered in 2')

    on_top = automaton_pile[-1:]
    if on_top[0] != EMPTY_PILE:
        Accept = False

    return Accept


# ----------------------------------------------------------------------------------------
def get_operations():
    operations = ['desapile, avance.']  # list of strings
    all_prods = __this_grammar.get_all()

    for prod in all_prods:
        RS = prod.get_right_side()
        if RS[0][0] == '<':
            aux_string = 'replace('
            for elem in reversed(RS):
                aux_string += elem
            aux_string += '), retenga.'
            operations.append(aux_string)

        elif RS[0][0] == EMPTY_SEQUENCE:
            operations.append('desapile, retenga.')

        else:
            how_many = 0
            aux_string = 'replace('
            for elem in reversed(RS):
                aux_string += elem
                how_many = len(elem)
            aux_string = aux_string[:-how_many]
            aux_string += '), avance.'
            if 'replace()' in aux_string:
                aux_string = aux_string.replace('replace()', 'desapile')
            operations.append(aux_string)

    return operations


# ----------------------------------------------------------------------------------------
def get_recognizer_elements():
    __set_symbols()
    global __entry_symbols
    global __pile_symbols
    global __this_grammar
    return [__entry_symbols, __pile_symbols, __this_grammar]
