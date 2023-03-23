import vlc
import PySimpleGUI as sg
from src.bruceMediaPlayer.bmp import BruceMediaPlayer


def init_layout():
    layout = [
        [sg.Text('Choice a Music:'),
         sg.InputText(key='-FILE-', size=(40, 1), ),
         sg.FileBrowse('Open Folder:', file_types=(('MP3 file', '*.mp3'),))],
        [sg.Text('Enter start and end times (in seconds) for each interval')],
        [sg.Text('Interval 1:'), sg.InputText(size=(5, 1), key='-INT1_START-'), sg.Text('-'),
         sg.InputText(size=(5, 1), key='-INT1_END-')],
        [sg.Text('Interval 2:'), sg.InputText(size=(5, 1), key='-INT2_START-'), sg.Text('-'),
         sg.InputText(size=(5, 1), key='-INT2_END-')],
        [sg.Text('Interval 3:'), sg.InputText(size=(5, 1), key='-INT3_START-'), sg.Text('-'),
         sg.InputText(size=(5, 1), key='-INT3_END-')],
        [sg.Text('Interval 4:'), sg.InputText(size=(5, 1), key='-INT4_START-'), sg.Text('-'),
         sg.InputText(size=(5, 1), key='-INT4_END-')],
        [sg.Text('Interval 5:'), sg.InputText(size=(5, 1), key='-INT5_START-'), sg.Text('-'),
         sg.InputText(size=(5, 1), key='-INT5_END-')],
        [sg.Text('Volume (0 - 100):'),
         sg.Slider(range=(0, 100), default_value=50, orientation='h', size=(20, 15), key='-VOLUME-')],
        [sg.Text('Speed (0.5 - 2):'),
         sg.Slider(range=(0.5, 2), default_value=1, resolution=0.25, orientation='h', size=(20, 15), key='-SPEED-')],
        [sg.Text('Current Time: ', font=('Arial', 12)),
         sg.Text('00:00', font=('Arial', 12), size=(10, 1), key='-TIME-')],
        [sg.Button('Play'), sg.Button('Pause'), sg.Button('Stop')]
    ]
    window = sg.Window('Bruce Media Player', layout)
    return window


def get_intervals(window):
    intervals = []
    for i in range(1, 6):
        start_key = f'-INT{i}_START-'
        end_key = f'-INT{i}_END-'
        start = window[start_key].get()
        end = window[end_key].get()
        if start and end:
            intervals.append((int(start), int(end)))
    return intervals


def callback_change_time(event, player, window):
    print('callback')
    minutes, seconds = player.get_music_current_time()
    window['-TIME-'].update(f'{minutes:0>1d}:{seconds:0>2d}')


def cb(event):
    print(f'fb: {event.type}, {dir(event)}')

class GUI:
    def __init__(self):
        """初始化

        初始化先取整個視窗的設置，再取得區間設置
        如果沒有任何區間設置的話，那就直接撥放音樂就可以
        """
        self.window = init_layout()
        self.intervals = None
        self.media = BruceMediaPlayer()

    # def set_music(self, file_path):
    #     """音樂設置"""
    #     self.media.set_music(file_path)

    def play(self):
        """撥放音樂

        如果間隔設置沒有任何東西就視為標準的音樂撥放即可

        .. note:: 為了能夠分段執行就只好調整成在撥放的時間再產生物件
        """
        # self.media.set_music(self.window['-FILE-'].get())
        self.intervals = get_intervals(self.window)
        if len(self.intervals) == 0:
            self.media.set_player(player_type='single')
            self.media.add_call_back(vlc.EventType.MediaPlayerTimeChanged, callback_change_time, self.media, self.window)
            self.media.play(self.window['-FILE-'].get())
        else:

            self.media.set_player(player_type='player_list')
            # self.media.add_call_back(vlc.EventType.MediaListPlayerNextItemSet, cb)
            self.media.play(self.window['-FILE-'].get(), self.intervals)
            # self.media.set_ab_repeat_v2(self.intervals)

    def release(self):
        self.media.release()
        self.window.close()

    def pause(self):
        self.media.pause()

    def stop(self):
        self.media.stop()

    def run_app(self):
        while True:
            gui_event, gui_values = self.window.read(timeout=100)
            if gui_event == 'Play':
                self.play()
            elif gui_event == 'Pause':
                self.pause()
            elif gui_event == 'Stop':
                self.stop()
            elif gui_event == '-SPEED-':
                print('in_speed')
                speed = gui_values['-SPEED-']
                self.media.set_speed(float(speed))
            elif gui_event == '-VOLUME-':
                print('in volume')
                volume = gui_values['-VOLUME-']
                self.media.set_volume(int(volume))
            elif gui_event == sg.WINDOW_CLOSED:
                self.release()
                break

            # try:
            #     minutes, seconds = self.media.get_music_current_time()
            #     self.window['-TIME-'].update(f'{minutes:0>1d}:{seconds:0>2d}')
            # except AttributeError as e:
            #     pass

