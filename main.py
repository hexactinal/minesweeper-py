DEBUG_GAME = False

class Field:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.field = []
        self.reveal_elem = []
        # change this to make it randomize for each later.
        counter = 0
        for i in range(self.cols):
            element = ''
            reveals = []
            row = []
            for j in range(self.rows):
                if counter % 2 == 0 and counter % 3 != 0 and counter % 4 != 0 and counter % 5 != 0:
                    element = '[1]'
                else:
                    element = '[,]'

                row.append(element)
                reveals.append(DEBUG_GAME)
                counter = counter + 1

            row.append('newline') # end of each line of the field matrix
            reveals.append(True)
            reveal_this_row = []
            for i in range(len(row)):
                a = (row[i], reveals[i])
                reveal_this_row.append(a)

            self.reveal_elem.append(reveal_this_row)

            self.field.append(row)
        counter = 0
        this_elem = 0
        for row in self.field:
            for i in row:
                if i == '[1]':
                    self.field[counter][this_elem + 1] = '[m]'
                    if DEBUG_GAME:
                        self.reveal_elem[counter][this_elem + 1] = ('[m]', True)
                    else:
                        self.reveal_elem[counter][this_elem + 1] = ('[m]', False)
                this_elem = this_elem + 1
            counter = counter + 1
            this_elem = 0
        
        self.mines_amount = counter
        if DEBUG_GAME:
            print('number of mines: {}'.format(mines_amount))
        


    def __str__(self):
        s = ''
        for rows in self.reveal_elem:
            for i,j in rows:
                if i == 'newline':
                    s = s + '\n'
                    continue
                if j:
                    s = s + i + ' '
                else:
                    s = s + '[ ]' + ' '

        return s

def comma_and_period_error_checking(usr_in):
    error_occurred = False
    usr_comma_loc = usr_in.find(',')
    usr_period_loc = usr_in.find('.')
    if usr_comma_loc == -1:
        error_occurred = True
        print('[ERROR] Forgot to put a comma, try again!')
    if usr_comma_loc == 0:
        error_occurred = True
        print('[ERROR] Input must start with a number, try again!')
    if usr_period_loc == -1 or usr_period_loc == 0:
        error_occurred = True
        print('[ERROR] Input must end with a period, try again!')
    if usr_comma_loc > usr_period_loc:
        error_occurred = True
        print('[ERROR] Period must be after comma, try again!')
    if usr_period_loc == usr_comma_loc + 1:
        error_occurred = True
        print('[ERROR] Must include a number to use for the column in between the comma and the period, try again!')
    return error_occurred

def row_and_col_error_checking(field, usr_in):
    usr_comma_loc = usr_in.find(',')
    usr_period_loc = usr_in.find('.')
    try:
        usr_row = int(usr_in[0:usr_comma_loc])
    except ValueError:
        print('[ERROR] Row must be a number!')
        return True
    try:
        usr_col = int(usr_in[usr_comma_loc + 1:usr_period_loc])
    except ValueError:
        print('[ERROR] Column must be a number!')
        return True
    if usr_row < 0 or usr_col < 0:
        print('[ERROR] The lowest tile number to check is 1, try again!')
        return True

    if usr_row >= field.rows:
        print('[ERROR] Cannot index past the end of the rows, try again!')
        return True
    if usr_col >= field.cols:
        print('[ERROR] Cannot index past the end of the columns, try again!')
        return True
    return False

def print_win_msg():
    print('__   _____  _   ___        _____  _   _ ')
    print('\ \ / / _ \| | | \ \      / / _ \| \ | |')
    print(' \ V | | | | | |  \ \ /\ / | | | |  \| |')
    print('  | || |_| | |_|   \ V  V /| |_| | |\  |')
    print('  |_| \___/ \___/   \_/\_/  \___/|_| \_|')
    exit()

def print_loss_msg():
    print('m     m  mmmm  m    m        m       mmmm   mmmm mmmmmmm')
    print(' "m m"  m"  "m #    #        #      m"  "m #"   "   #   ')
    print('  "#"   #    # #    #        #      #    # "#mmm    #   ')
    print('   #    #    # #    #        #      #    #     "#   #   ')
    print('   #     #mm#  "mmmm"        #mmmmm  #mm#  "mmm#"   #   ')
    exit()

def replace_with_commas(field, usr_row, usr_col):
    NEW_COMMA_TUPLE = ('[,]', True)
    # to left
    
    local_left = usr_col
    while local_left >= 0:
        try:
            if field.field[usr_row][local_left] != '[,]':
                break
            field.reveal_elem[usr_row][local_left] = NEW_COMMA_TUPLE
            local_left = local_left - 1
        except IndexError:
            break

    # to right
    local_right = 0
    while local_right <= field.cols:
        try:
            if field.field[usr_row][local_right] != '[,]':
                old_local, _ = field.reveal_elem[usr_row][local_right]
                field.reveal_elem[usr_row][local_right] = (old_local, True)
                break
            field.reveal_elem[usr_row][local_right] = NEW_COMMA_TUPLE
            local_right = local_right + 1
        except IndexError:
            break

    # to upper
    local_upper = usr_row
    while local_upper >= 0:
        try:
            if field.field[local_upper][usr_col] != '[,]':
                break
            field.reveal_elem[local_upper][usr_col] = NEW_COMMA_TUPLE
            local_upper = local_upper - 1
        except IndexError:
            break
    
    # to lower
    local_lower = 0
    while local_lower < field.rows:
        if field.field[local_lower][usr_col] != '[,]':
            break
        field.reveal_elem[local_lower][usr_col] = NEW_COMMA_TUPLE
        local_lower = local_lower + 1
        

def check_tile(field, usr_in):
    usr_comma_loc = usr_in.find(',')
    usr_period_loc = usr_in.find('.')
    usr_row = int(usr_in[0:usr_comma_loc])
    usr_col = int(usr_in[usr_comma_loc + 1:usr_period_loc])
    s = ''
    num_of_newlines = 0
    count = 0
    s = field.field[usr_row][usr_col]
    print(s)
    if s != '[,]' or DEBUG_GAME:
        field.reveal_elem[usr_row][usr_col] = (s, True)
    else:
        replace_with_commas(field, usr_row, usr_col)

    if s == '[m]':
        print_loss_msg()
    if s == '[1]':
        return 1 # to increment the counter

def game_loop(field):
    found_another_hint = 0
    while True:
        print(field)
        print('What tile do you want to reveal?')
        usr_in = input('(format is "Row,Column."): ')

        comma_or_period_error = comma_and_period_error_checking(usr_in)
        if comma_or_period_error:
            continue

        row_or_col_error = row_and_col_error_checking(field, usr_in)
        if row_or_col_error:
            continue
        
        check_tile(field, usr_in)
        found_another_hint = found_another_hint + 1
        if found_another_hint == field.mines_amount:
            print_win_msg()

def main():
    print('Welcome to Minesweeper!')
    field = Field(10, 10)
    game_loop(field)

if __name__ == '__main__':
    main()
