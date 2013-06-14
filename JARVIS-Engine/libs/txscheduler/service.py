'''
'''
from twisted.application.internet import TimerService

#~ class SchedulerService(service.Service):
class ScheduledTaskService(TimerService):
    '''Service for running scheduled tasks.
    '''
    def __init__(self, task_manager, interval=1, *args, **kwargs):
        '''
        '''
        self.step = interval
        self.clock = None
        self.call = (task_manager.run, args, kwargs)


    #~ def startService(self):
        #~ pass
        
    #~ def stopService(self):
        #~ pass