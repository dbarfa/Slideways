# PyQt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from board import Board
from players import *


class App(QMainWindow):
    '''
    Main Graphical User Interface class.
    :attribute current_player: Player who should act on the board right now
    :attribute waiting_player: The other player
    :attribute time_interval: integer giving the delay before an AI action
    '''
    TITLE = 'INFOF-106 SlideWays'

    def __init__(self):
        '''
        Constructor of class `App`.
        '''
        super().__init__()
        self.init_vars()
        self.current_player = None
        self.waiting_player = None
        self.initUI()

    def initUI(self):
        '''
        Instantiation of the interface per se: create all the widgets and
        layouts, and associate them altogether.
        :return: None
        '''
        self.setWindowTitle(App.TITLE)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.main_vbox = QVBoxLayout()

        self.settings_groupbox = QGroupBox('Settings')
        self.settings_grid = QGridLayout()
        self.settings_groupbox.setLayout(self.settings_grid)
        label = QLabel('Player 1:')
        self.settings_grid.addWidget(label, 0, 0, alignment=Qt.AlignRight)
        self.cb_player1 = QComboBox()
        self.cb_player1.addItems(['Minimax', 'Human'])
        self.settings_grid.addWidget(self.cb_player1, 0, 1)
        label = QLabel('Player 2:')
        self.settings_grid.addWidget(label, 1, 0, alignment=Qt.AlignRight)
        self.cb_player2 = QComboBox()
        self.cb_player2.addItems(['Minimax', 'Human'])
        self.settings_grid.addWidget(self.cb_player2, 1, 1)
        label = QLabel('Timer interval:')
        self.settings_grid.addWidget(label, 2, 0, alignment=Qt.AlignRight)
        self.time_slider = QSlider(Qt.Horizontal)
        self.time_slider.setTickPosition(QSlider.TicksBelow)
        self.time_slider.sliderReleased.connect(self.release_slider)
        self.time_slider.setTickInterval(10)
        self.time_slider.setValue(1)
        self.settings_grid.addWidget(self.time_slider, 2, 1)
        self.main_vbox.addWidget(self.settings_groupbox)

        self.hbox = QHBoxLayout()

        self.left_buttons = ButtonPanel(
            self, '<', 4, self.handle_click_event, LEFT)
        self.hbox.addWidget(self.left_buttons)

        self.canvas = Canvas(self.board, parent=self.central_widget)
        self.canvas.mousePressEvent = self.handle_click_event
        self.hbox.addWidget(self.canvas)

        self.right_buttons = ButtonPanel(
            self, '>', 4, self.handle_click_event, RIGHT)
        self.hbox.addWidget(self.right_buttons)

        self.main_vbox.addLayout(self.hbox)

        self.start_button = QPushButton('Start')
        self.start_button.clicked.connect(self.start_game)
        self.main_vbox.addWidget(self.start_button)

        self.central_widget.setLayout(self.main_vbox)
        self.show()

    def release_slider(self):
        '''
        Callback of SliderReleased event: update the time interval.
        :return: None
        '''
        self.time_interval = self.time_slider.value() * 10

    def handle_click_event(self, event, offset=None):
        '''
        Callback of Clicked event on ButtonPanel instances and on the Canvas.
        :param event: contains the (x, y) position of the click event
        :param offset: tuple (direction, row)
        :return: None
        '''
        if self.current_player is None or not self.current_player.is_currently_playing():
            return
        if not isinstance(self.current_player, HumanPlayer):
            return
        try:
            self.current_player.play(event, offset)
        except InvalidActionException:
            pass  # Just keep going...
        else:
            self.toggle_players()

    def init_vars(self):
        '''
        Initialise the game related variables.
        :return: None
        '''
        self.board = Board()
        self.time_interval = 10

    @staticmethod
    def make_player(text, player_id, board):
        '''
        Create a player depending on the given parameter.
        :param text: either 'AI' or 'Human'
        :param player_id: id of the player to create
        :param board: an instance of the class `Board`
        :return: an instance of the class `Player`
        :raise: `ValueError` if text does not match correct inputs
        '''
        if text == 'Minimax':
            return MinimaxPlayer(player_id, board)
        elif text == 'Human':
            return HumanPlayer(player_id, board)
        else:
            raise ValueError(
                'Only \'Minimax\' and \'Human\' are valid player types')

    def start_game(self):
        '''
        Callback of Clicked event on the start/restart button.
        :return: None
        '''
        self.start_button.setText('Restart')
        self.board.reset()
        self.player_1 = App.make_player(
            self.cb_player1.currentText(), 1, self.board)
        self.player_2 = App.make_player(
            self.cb_player2.currentText(), 2, self.board)
        self.current_player = self.player_2
        self.waiting_player = self.player_1
        self.canvas.update()
        self.toggle_players()  # So that player 1 starts

    def toggle_players(self):
        '''
        Swap current player and waiting player.
        :return: None
        '''
        self.canvas.update()
        self.current_player.not_your_turn()
        if self.board.winner():
            self.exhibit_end_of_game()
            return
        self.current_player, self.waiting_player = self.waiting_player, self.current_player
        self.current_player.your_turn()
        if isinstance(self.current_player, AIPlayer):
            QTimer.singleShot(self.time_interval, self.toggle_players)

    def exhibit_end_of_game(self):
        '''
        Show that the game is over and display the winner.
        '''
        # self.player_1.not_your_turn()
        popup = WinnerPopup(self.board.winner(), self)
        popup.exec_()  # Use exec_ instead of show to block main window
        self.start_button.setText('Start')


class WinnerPopup(QDialog):
    '''
    Popup displaying the winner(s) of the game
    '''

    def __init__(self, winners, parent):
        '''
        Constructor of class `WinnerPopup`
        :param winners: a list of winners
        :param parent: the parent Qt widget
        '''
        super().__init__(parent)
        assert len(winners) > 0
        if len(winners) == 1:
            text = f'Player {winners[0]} won!'
        else:
            text = 'Draw game: nobody won. Try again!'
        self.setFixedSize(QSize(500, 100))
        self.label = QLabel(text, self)
        self.label.setFont(QFont("Calibri", 20, QFont.Bold))
        # TODO fix the label width and label heigth to the current version
        # label_width = self.label.fontMetrics().boundingRect(self.label.text()).width()
        # label_height = self.label.fontMetrics().boundingRect(self.label.text()).height()

        # self.label.move((self.width()-label_width)/2,
        #                 (self.height()-label_height)/2)


class ButtonPanel(QWidget):
    '''
    Qt-compatible widget representing a panel containing several buttons intended for board offsets.
    :attribute buttons: list of QPushButton instances
    '''

    def __init__(self, parent, button_text, nb_buttons, button_callback, direction):
        '''
        Constructor of class `ButtonPanel`.
        :param parent: the parent Qt widget
        :param button_text: text to write on every single button
        :param nb_buttons: number of buttons to add vertically on the panel
        :param button_callback: function to call when a button is clicked
        :param direction: direction of the offset (either +1 or -1)
        '''
        # do not forget to call the constructor of the parent class
        super().__init__(parent=parent)
        self.setFixedSize(QSize(20, HEIGHT))
        self.buttons = list()
        for row in range(nb_buttons):
            self.buttons.append(QPushButton(button_text, parent=self))
            self.buttons[-1].setMaximumWidth(20)
            self.buttons[-1].clicked.connect(
                lambda _, row=row: button_callback(event=None, offset=(direction, row)))
            self.buttons[-1].move(0, OFFSET + CELL_SIZE //
                                  2 + row*(CELL_SIZE + OFFSET) - 10)


class Canvas(QWidget):
    '''
    Qt-compatible widget representing the canvas on which the board is drawn repeatedly.
    :attribute board:
    '''

    def __init__(self, board, parent=None):
        '''
        Constructor of the class `Canvas`
        :param board: instance of the class `Board` that shall be represented
        :param parent: the parent Qt widget
        '''
        super().__init__(parent=parent)
        self.board = board
        self.setFixedSize(QSize(WIDTH, HEIGHT))

    def paintEvent(self, event=None):
        '''
        Callback of the Update event on the canvas.
        :param event: ignored
        '''
        qp = QPainter()
        qp.begin(self)
        self.draw(qp)
        qp.end()

    def draw(self, qp):
        '''
        Draw the board onto the canvas.
        :param qp: instance of class `QPainter`
        '''
        grid = self.board.get_grid()
        offset = self.board.get_offset()
        self.draw_grid_debug(qp)
        # associated color to each possible value of the board cells:
        # empty is drawn *white*, player 1 is drawn *yellow*, and player 2 is drawn *red*
        colors = [Qt.white, Qt.yellow, Qt.red]
        qp.setPen(Qt.black)
        for row in range(4):
            qp.setBrush(Qt.darkBlue)
            # First draw the rectangle of the current row
            y = row * (CELL_SIZE + OFFSET) + OFFSET + CELL_SIZE//2
            x = (CELL_SIZE + OFFSET) * (offset[row]+3) + OFFSET + CELL_SIZE//2
            # (x, y) represents the middle of the left cell of considered row
            qp.drawRect(
                x - CELL_SIZE//2 + 5,
                y - CELL_SIZE//2 + 5,
                3*OFFSET + 4*CELL_SIZE - 10,
                CELL_SIZE - 10
            )
            # Then draw each circle within that row
            for col in range(4):
                qp.setBrush(colors[grid[row][col]])
                qp.drawEllipse(
                    x - CELL_SIZE//2 + 10,
                    y - CELL_SIZE//2 + 10,
                    CELL_SIZE - 20,
                    CELL_SIZE - 20
                )
                x += CELL_SIZE + OFFSET

    def draw_grid_debug(self, qp):
        '''
        Draw debug lines on the canvas. Only used when adapting the size of the cells/rows.
        :param qp: instace of class `QPainter`
        '''
        if not GRID_DEBUG:
            return
        qp.setPen(Qt.red)
        x = 0
        for i in range(10):
            x += OFFSET
            qp.drawLine(x, 0, x, HEIGHT)
            x += CELL_SIZE
            qp.drawLine(x, 0, x, HEIGHT)
        y = 0
        for i in range(4):
            y += OFFSET
            qp.drawLine(0, y, WIDTH, y)
            y += CELL_SIZE
            qp.drawLine(0, y, WIDTH, y)
