# Copyright (c) 2008 TechAdept Inc.

'''
'''

from datetime import datetime
from twisted.python import log
from twisted.internet.defer import maybeDeferred

class ScheduledTask(object):
    '''Represents a scheduled task.
    
    :param name: a string with the name of this task
    :param rrule: a dateutil.rrule instance
    :param callable: a callable with the actual work to be done
    :param args: args to send to the callable
    :param kwargs: kwargs to send to the callable
    '''
    def __init__(self, name, rrule, callable, *args, **kwargs):
        self.name = name
        self.callable = callable
        self.recurrence = rrule
        self.next_scheduled_runtime = None
        self.last_runtime = None
        self.running = False

        self.args = args
        self.kwargs = kwargs

        # schedule the task for the first run
        self._reschedule()
        
    def before_execute(self):
        '''Override this method to perform tasks before the callable is executed.
        '''
        log.msg('before_execute called')

    def after_execute(self):
        '''Override this method to perform tasks after the callable is executed.
        '''
        log.msg('after_execute called')

    def _reschedule(self):
        '''Determines the next time that the task should be run.
        '''
        last_time = self.last_runtime
        if last_time is None:
            last_time =  datetime.now()
        next_time = self.recurrence.after(last_time)
        self.next_scheduled_runtime = next_time

    def _post_execute(self, result):
        '''Callback run after the task has finished a run.
        
        Calls the 'after_execute' hook and reschedules the task.
        '''
        self._reschedule()
        self.after_execute()
        return result

    def _execute(self):
        '''Actually runs the task.
        '''
        log.msg('self.args: ')
        log.msg(self.args)
        self.last_runtime = datetime.now()
        self.running = True
        # run the callable
        d = maybeDeferred( self.callable, *self.args, **self.kwargs )
        d.addBoth(self._post_execute)
        return d

    def run(self):
        '''Runs the task.
        
        Client code (usually a ScheduledTaskManager) should call this to 
        get the task to run.
        '''
        self.before_execute()
        d = maybeDeferred( self._execute )
        return d
        
        
        
