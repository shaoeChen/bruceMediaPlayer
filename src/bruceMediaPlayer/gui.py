import vlc
import PySimpleGUI as sg
from src.bruceMediaPlayer.bmp import BruceMediaPlayer
from dataclasses import dataclass


@dataclass
class MetaDataStructure:
    values: float = 0


meta_volume = MetaDataStructure(50)
meta_speed = MetaDataStructure(1.0)

def on_slider_move(event):
    pass

def init_layout():
    global g_speed
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
         sg.Slider(range=(0, 100), default_value=50, orientation='h', size=(20, 15), key='-VOLUME-',
                   metadata=meta_volume, resolution=1, enable_events=True)],
        [sg.Text('Speed (0.5 - 2):'),
         sg.Slider(range=(0.5, 2), default_value=1, resolution=0.25, orientation='h', size=(20, 15), key='-SPEED-',
                   metadata=meta_speed, enable_events=True)],
        [sg.Text('Current Time: ', font=('Arial', 12)),
         sg.Text('00:00', font=('Arial', 12), size=(10, 1), key='-TIME-')],
        [sg.Button('Play'), sg.Button('Pause'), sg.Button('Stop')]
    ]
    window = sg.Window('Bruce Media Player', layout)
    return window


def get_intervals(window) -> list:
    """取得撥放區間清單

    取得pysimplegui關於撥放區間清單設置的開始、結束秒數
    欄位取得的資料皆為文字，需要調整為整數

    如果設置的結束時間比開始時間還要小，那就直接忽略該條設置
    舉例來說，當結束時間為60並且開始時間為70的時候，該條設置直接忽略
    或者單純的設置開始或是結束時間也會忽略該設置

    :param window: PySimpleGUI的window
    :return interval: 時間區間，list[int, int]，[開始時間, 結束時間]
    """
    intervals = []
    for i in range(1, 6):
        start_key = f'-INT{i}_START-'
        end_key = f'-INT{i}_END-'
        start = window[start_key].get()
        end = window[end_key].get()

        if (end != '' and start != '') and (int(end) < int(start)):
            continue

        if start and end:
            intervals.append((int(start), int(end)))
    return intervals


def callback_change_time(event, player, window):
    minutes, seconds = player.get_music_current_time()
    window['-TIME-'].update(f'{minutes:0>1d}:{seconds:0>2d}')

    speed = window['-SPEED-'].metadata.values
    volume = window['-VOLUME-'].metadata.values
    player.set_speed(speed)
    player.set_volume(int(volume))


class GUI:
    def __init__(self):
        """初始化

        初始化先取整個視窗的設置，再取得區間設置
        如果沒有任何區間設置的話，那就直接撥放音樂就可以
        """
        self.window = init_layout()
        self.intervals = None
        self.media = BruceMediaPlayer()

    def play(self):
        """撥放音樂

        如果間隔設置沒有任何東西就視為標準的音樂撥放即可

        todo: 後續可再抽象這個執行函數
        todo: callback function的部份可以再調整成以dict做為選單選取的方式
        """
        # self.media.set_music(self.window['-FILE-'].get())
        self.intervals = get_intervals(self.window)
        if len(self.intervals) == 0:
            self.media.set_player(player_type='single')
            self.media.add_call_back(vlc.EventType.MediaPlayerTimeChanged, callback_change_time, self.media,
                                     self.window)
            self.media.play(self.window['-FILE-'].get())
        else:
            self.media.set_player(player_type='player_list')
            self.media.add_call_back(vlc.EventType.MediaPlayerTimeChanged, callback_change_time, self.media,
                                     self.window)
            self.media.play(self.window['-FILE-'].get(), self.intervals)

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
                speed = gui_values['-SPEED-']
                meta_speed.values = speed
            elif gui_event == '-VOLUME-':
                volume = gui_values[gui_event]
                meta_volume.values = volume
            elif gui_event == sg.WINDOW_CLOSED:
                self.release()
                break
