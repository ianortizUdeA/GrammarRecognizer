# ---------------NT stands for 'Not Terminal' which is what's on the left side of a production----------

EMPTY_SEQUENCE = '¡'
END_OF_SEQUENCE = '¬'


def remove_repeated_elements(lt):
    return list(dict.fromkeys(lt))


class Production:
    def __init__(self, not_terminal, right_side):
        self.__not_terminal = '<' + not_terminal + '>'  # String
        self.__right_side = []  # List of Strings
        self.__organize_right_size(right_side)

    def __organize_right_size(self, RS):
        opening = 0
        skip = False
        for idx, car in enumerate(RS):
            if car == '<':
                opening = idx
                skip = True  # Changes to True
            elif car == '>':
                self.__right_side.append(RS[opening:idx + 1])
                skip = False  # Changes to False
            else:
                if skip:
                    continue
                self.__right_side.append(car)

    def get_not_terminal(self):
        return self.__not_terminal

    def get_right_side(self):
        return self.__right_side


# ------------------------------------------------------------------------------------
class Grammar:
    def __init__(self, productions):
        self.__all_productions = productions  # It's a list

        # ++++++++++++++++++++++++++ Global Variables ++++++++++++++++++++++++++++++++++++++
        self.__NT_list = []
        self.__terminals = []
        self.__voidable_NT = []
        self.__first_sets = {}  # Dictionary of lists of strings/chars
        self.__following_sets = {}
        self.__selection_sets = []  # List of lists of strings

        self.__find_elements()
        self.__create_selection_sets()

        # ++++++++++++++++++++++++++++++ Functions +++++++++++++++++++++++++++++++++++++++++

    def __find_elements(self):
        for production in self.__all_productions:
            NT = production.get_not_terminal()
            if NT not in self.__NT_list:
                self.__NT_list.append(NT)

            RS = production.get_right_side()
            for str in RS:
                if str[0] != '<' and str != EMPTY_SEQUENCE and str not in self.__terminals:
                    self.__terminals.append(str)
        self.__terminals.sort()

    ###################################
    def __find_voidables(self):
        for production in self.__all_productions:
            aux_stg = production.get_right_side()
            if aux_stg[0] == EMPTY_SEQUENCE \
                    and production.get_not_terminal() not in self.__voidable_NT:
                self.__voidable_NT.append(production.get_not_terminal())
                continue

            if aux_stg[0][:1] == '<':
                is_voidable = True
                for sub_stg in aux_stg:
                    if sub_stg not in self.__voidable_NT:
                        is_voidable = False
                if is_voidable and production.get_not_terminal() not in self.__voidable_NT:
                    self.__voidable_NT.append(production.get_not_terminal())

    ###########################################
    def __find_firsts_set(self, NT):
        pending_changes = []
        list_to_append = []
        # This first 'for' will go through productions of the NotTerminal of interest
        for production in self.__all_productions:
            if production.get_not_terminal() == NT:
                right_side = production.get_right_side()
                # This next 'for' will go through elements(Terminal/NT) of the production. It will append elements
                # until it finds a terminal, an empty sequence or a NotTerminal that is not voidable
                for str in right_side:
                    if str[0] == '<':
                        # It's read : To the set of firsts of the not terminal NT add the set of first of 'str'
                        aux_tuple = (NT, str)
                        pending_changes.append(aux_tuple)
                        if str not in self.__voidable_NT:
                            break
                    elif str[0] == EMPTY_SEQUENCE:
                        break
                    else:
                        list_to_append.append(str)
                        break

        list_to_append = remove_repeated_elements(list_to_append)
        self.__first_sets[NT] = list_to_append
        return pending_changes

    #############################################
    def __find_following_set(self, NT):
        pending_changes = []
        list_to_append = []
        if NT == self.get_initial_symbol():
            list_to_append.append(END_OF_SEQUENCE)

        # This whole thing is structured in case there are multiple appearances of the NT in a production
        for production in self.__all_productions:
            right_side = production.get_right_side()
            if NT in right_side:
                append = False  # This is so we can know which elements should be appended or not

                for idx, str in enumerate(right_side):

                    if str == NT and idx == (len(right_side) - 1):  # If it's the last
                        aux_tuple = (NT, production.get_not_terminal())
                        pending_changes.append(aux_tuple)
                        break

                    if str == NT and append == False:
                        append = True
                        continue
                        # Becomes True, meaning that everything that follows should be appended until certain
                        # conditions are met

                    if append:
                        if str[0] == '<':
                            list_to_append = list_to_append + self.__first_sets[str]
                            if str not in self.__voidable_NT:
                                # This next 'if' is for a very specific case: You're looking for the followings of <A>,
                                # and a production happens to have on its right side <A><A>(...), AND <A> happens to be
                                # not voidable. After reading the first <A> we get the set of firsts of the second <A>,
                                # if at this point we change 'append' to False, then what's next to the second <A>
                                # would not be taken into consideration, which is not correct
                                if str == NT:
                                    continue

                                append = False  # False to carry on searching for a second instance of the NT
                        else:
                            list_to_append.append(str)
                            append = False  # False to carry on searching for a second instance of the NT

                # If at this point 'append' is true, it means that the last element of right_side was a voidable NT
                # so we must find the followings of the left side of this production
                aux_tuple = (NT, production.get_not_terminal())
                pending_changes.append(aux_tuple)

        list_to_append = remove_repeated_elements(list_to_append)
        self.__following_sets[NT] = list_to_append
        return pending_changes

    ###################################
    def __update_sets(self, pendings, d):
        if d == 'firsts':
            while pendings:
                tup = pendings.pop()        # Don't know if handle it like a pile or a queue
                lst = self.__first_sets[tup[0]]
                lst = lst + self.__first_sets[tup[1]]
                lst = remove_repeated_elements(lst)
                self.__first_sets[tup[0]] = lst
        elif d == 'foll':
            while pendings:
                tup = pendings.pop()
                lst = self.__following_sets[tup[0]]
                lst = lst + self.__following_sets[tup[1]]
                lst = remove_repeated_elements(lst)
                self.__following_sets[tup[0]] = lst

    ###################################
    def __create_selection_sets(self):
        # First, voidable NotTerminals are stored
        # This while will attempt to find voidable NT's until it no longer finds NT to append to the list
        # When this happens the length of the list will not vary and the while will cease to execute
        previous_len = -1
        while len(self.__voidable_NT) != previous_len:
            previous_len = len(self.__voidable_NT)
            self.__find_voidables()
        del previous_len

        # Now we find the set of Firsts of all NT
        # pending_changes is a pile that stores operation remaining to do
        pending_changes = []
        for NT in self.__NT_list:
            pending_changes = pending_changes + self.__find_firsts_set(NT)
        self.__update_sets(pending_changes, 'firsts')

        # Now to find the set of Following of all NT
        pending_changes.clear()
        for NT in self.__NT_list:
            pending_changes = pending_changes + self.__find_following_set(NT)
        self.__update_sets(pending_changes, 'foll')

        # And finally, we create the selection sets
        for prod in self.__all_productions:
            list_to_append = []
            add_followings = False
            right_side = prod.get_right_side()
            for str in right_side:
                if str[0] == '<':
                    list_to_append = list_to_append + self.__first_sets[str]
                    add_followings = True
                    if str not in self.__voidable_NT:
                        add_followings = False
                        break
                elif str == EMPTY_SEQUENCE:
                    list_to_append = list_to_append + self.__following_sets[prod.get_not_terminal()]
                    add_followings = False
                    break
                else:
                    list_to_append.append(str)
                    add_followings = False
                    break

            if add_followings:
                list_to_append = list_to_append + self.__following_sets[prod.get_not_terminal()]

            list_to_append = remove_repeated_elements(list_to_append)
            self.__selection_sets.append(list_to_append)

        # print(self.__following_sets) TODO fix this :C
        # print(self.__selection_sets)

    # ########################### Getters ##################################
    def get_all(self):
        return self.__all_productions

    def get_initial_symbol(self):
        return self.__NT_list[0]

    def get_selection_set(self, i):
        if i >= 0:
            return self.__selection_sets[i]
        return 0    # Error

    def get_not_terminals(self):
        return self.__NT_list

    def get_terminals(self):
        return self.__terminals
