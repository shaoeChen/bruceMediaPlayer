import PySimpleGUI as sg
import os

os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')

import vlc

# Initialize PySimpleGUI theme and create a layout for the media player window
sg.theme('DarkGrey2')
layout = [
    [sg.Text('超陽春撥放器', justification='center')],
    [sg.Text('選擇歌曲：')],
    [sg.FileBrowse('開啟資料夾', file_types=(('MP3 file', '*.mp3'),)),
     sg.InputText(key='-FILE-', size=(40, 1), )],
    [sg.Text('設置撥放區間(mm:ss)')],
    [sg.Multiline(default_text='00:00 - 00:00', size=(40, 10), key='-INTERVAL-', no_scrollbar=True)],
    [sg.Text('音量', font=('', 12)),
     sg.Slider(range=(0, 100), orientation='h', size=(30, 20), default_value=50, key='-VOLUME-')],
    [sg.Text('撥放速度', font=('', 12)),
     sg.Slider(range=(0, 200), orientation='h', size=(30, 20), default_value=100, key='-SPEED-')],
    [sg.Text('重覆次數：', font=('', 12)),
     sg.InputText(default_text='1', size=(30, 20), font=('', 12), key='-REPEAT-')],
    # [sg.Text('Start Time (mm:ss)', font=('Arial', 12)),
    #  sg.InputText('00:00', font=('Arial', 12), size=(7, 1), key='-START-'),
    #  sg.Text('End Time (mm:ss)', font=('Arial', 12)),
    #  sg.InputText('00:00', font=('Arial', 12), size=(7, 1), key='-END-')],
    [sg.Text('目前撥放時間： ', font=('', 12)),
     sg.Text('0:00', font=('Arial', 12), size=(10, 1), key='-TIME-')],
    [sg.Button('Play'), sg.Button('Pause'), sg.Button('Stop')]
]

# Create the media player window
window = sg.Window('Media Player', layout)

# Create the VLC media player instance
instance = vlc.Instance('--no-xlib')

# Create the media player object and set the default media
player = instance.media_player_new()
media = instance.media_new('')
player.set_media(media)


def parser_interval(values):
    intervals = []
    mmss_list = values['-INTERVAL-'].split('\n')
    for start_end in mmss_list:
        start_time, end_time = start_end.split('-')
        start_time = start_time.split(':')
        end_time = end_time.split(':')
        start_time = int(start_time[0]) * 60 + int(start_time[1])
        end_time = int(end_time[0]) * 60 + int(end_time[1])
        intervals.append((start_time, end_time))

    return intervals

# Start the event loop
while True:
    event, values = window.read(timeout=100)

    # Exit the program if the window is closed
    if event == sg.WINDOW_CLOSED:
        break

    # Handle button clicks
    if event == 'Play':
        # Set the media to be played
        media = instance.media_new(values['-FILE-'])

        # Calculate the start and end times
        # start_time = values['-START-'].split(':')
        # end_time = values['-END-'].split(':')
        # start_time = int(start_time[0]) * 60 + int(start_time[1])
        # end_time = int(end_time[0]) * 60 + int(end_time[1])

        player_interval = parser_interval(values)

        repeat_times = values['-REPEAT-']
        for start_time, end_time in player_interval:
            print(start_time, end_time)
            # Set the media options for interval playback
            media.add_options(f'start-time={start_time}')
            media.add_options(f'stop-time={end_time}')
            media.add_options(f'input-repeat={repeat_times}')
            player.set_media(media)
            # Play the media
            player.play()

    elif event == 'Pause':
        player.pause()

    elif event == 'Stop':
        player.stop()

    # Handle volume changes
    volume = int(values['-VOLUME-'])
    player.audio_set_volume(volume)

    # Handle speed changes
    speed = int(values['-SPEED-']) / 100
    player.set_rate(speed)

    # Update the current time
    current_time = player.get_time() / 1000
    minutes = int(current_time // 60)
    seconds = int(current_time % 60)
    window['-TIME-'].update(f'{minutes:0>1d}:{seconds:0>2d}')
