class NotInSameVoiceChannelError(Exception):
    def __init__(self, message='You have to be in the same voice channel as the music bot'):
        self.message = message
        super().__init__(self.message)
