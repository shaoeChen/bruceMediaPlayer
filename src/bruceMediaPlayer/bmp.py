import vlc


class BruceMediaPlayer:
    def __init__(self):
        self.instance = vlc.Instance()
        self.play_type = None
        self.player = None
        self.mlp_player = None

    def set_player(self, player_type: str = 'single'):
        """撥放模式是屬於單首撥放還是區段撥放"""
        self.player = self.instance.media_player_new()

        if player_type == 'single':
            self.play_type = 'single'
        elif player_type == 'player_list':
            self.play_type = 'player_list'
            self.mlp_player = self.instance.media_list_player_new()
            self.mlp_player.set_media_player(self.player)

    def play(self, file_path=None, intervals=None):
        if file_path is not None and self.play_type == 'single':
            media = self.instance.media_new(file_path)
            self.player.set_media(media)
            self.player.play()
        elif file_path is not None and intervals is not None and self.play_type == 'player_list':
            media_list = self.instance.media_list_new()

            for start, end in intervals:
                media = self.instance.media_new(file_path)
                media.add_options(f'start-time={start}')
                media.add_options(f'stop-time={end}')
                media_list.add_media(media)

            self.mlp_player.set_media_list(media_list)
            self.mlp_player.play()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def get_time(self):
        return self.player.get_time()

    def set_time(self, time_seconds: int):
        self.player.set_time(time_seconds * 1000)

    def get_music_current_time(self):
        """取得目前音樂撥放時間

        :return (分, 秒)
        """
        current_time = self.get_time() / 1000
        minutes = int(current_time // 60)
        seconds = int(current_time % 60)
        return minutes, seconds

    def set_volume(self, volume: int):
        self.player.audio_set_volume(volume)

    def set_speed(self, speed: float):
        self.player.set_rate(speed)

    def get_speed(self):
        return self.player.get_rate()

    def add_call_back(self, event_type, callback, *args, **kwargs):
        self.player.event_manager().event_attach(event_type, callback, *args, *kwargs)

    def release(self):
        self.player.release()
        if self.play_type == 'play_list':
            self.mlp_player.release()


    #
    # def set_music(self, file_path: str):
    #     """設置來源音樂"""
    #     self.media = self.instance.media_new(file_path)
    #
    #
    # def set_ab_repeat_v2(self, interval: tuple):
    #     """設置重覆撥放的區間
    #
    #     :param interval: 區間設置(起始時間, 結束時間)，以秒為單位
    #     :return:
    #     """
    #     for start, end in interval:
    #         media = self.media
    #         media.add_options(f'start-time={start}')
    #         media.add_options(f'stop-time={end}')
    #         self.media_list.add_media(media)
    #     self.player.set_media_list(self.media_list)
    #     self.play()
    #
    #
    #
    # def set_ab_repeat(self, interval: tuple):
    #     """設置重覆撥放的區間
    #
    #     :param interval: 區間設置，(起始時間, 結束時間)，以秒為單位
    #     """
    #     # start_time, end_time = interval
    #     # self.media.add_options(f'start-time={start_time}')
    #     # self.media.add_options(f'stop-time={end_time}')
    #     self.media.play()
