DATA_FILE_PATH = 'csv_files'
observation_size = 24
action_size = 3


class Commands(object):
    Stop = 'stop'
    Start = 'start'
    Restart = 'restart'


class BotStatuses(object):
    Sleeping = 'Sleeping'
    Relaxing = 'Relaxing'
    Running = 'Running'
    StopLoss = 'Stop_loss'
    TakeProfit = 'Take_profit'
