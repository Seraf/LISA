from datetime import datetime
from twisted.python import log
from pymongo import MongoClient
from tasks import ScheduledTask
from dateutil.rrule import *
from twisted.python.reflect import namedAny
from twisted.python import log
from sys import path

class TraceTask(ScheduledTask):

    def before_execute(self):
        log.msg('current time is: %s' % datetime.now())
        log.msg('tasks last runtime was: %s' % self.last_runtime)
        log.msg('tasks next runtime is: %s' % self.next_scheduled_runtime)

    def after_execute(self):
        log.msg('current time is: %s' % datetime.now())
        log.msg('tasks last runtime was: %s' % self.last_runtime)
        log.msg('tasks next runtime is: %s' % self.next_scheduled_runtime)

class ScheduledTaskManager(object):
    '''Manages a group of tasks.
    '''
    def __init__(self, configuration):
        self.configuration = configuration
        mongo = MongoClient(configuration['database']['server'], configuration['database']['port'])
        self.database = mongo.lisa
        self.build_tasks()

    def build_tasks(self):
        self.tasks = []
        for cron in self.database.crons.find( { "enabled": True } ):
            rule = rrulestr(str(cron['rule']))
            object = namedAny(cron['module'] + '.' + cron['class'])()
            func = namedAny(cron['module'] + '.' + cron['class'] + '.' + cron['method'])
            if cron['args']:
                if cron['debug'] == True:
                    self.tasks.append(TraceTask(cron['name'], rule, func, object, cron['args']))
                else:
                    self.tasks.append(ScheduledTask(cron['name'], rule, func, object, cron['args']))
            else:
                if cron['debug'] == True:
                    self.tasks.append(TraceTask(cron['name'], rule, func, object))
                else:
                    self.tasks.append(ScheduledTask(cron['name'], rule, func, object))

    def add_task(self, task):
        '''Adds a task to be run.
        
        Expects a :class:`txscheduler.tasks.ScheduledTask` instance.
        '''
        self.tasks.append(task)

    def reload(self):
        '''Reload the self.tasks
        '''
        self.build_tasks()
        return "OK"

    def remove_task(self, task):
        '''Removes a task to be run.
        
        Expects a :class:`txscheduler.tasks.ScheduledTask` instance.
        '''
        self.tasks.remove(task)
        
    def run(self):
        '''Checks for tasks which need to be run and runs them.
        '''
        if self.configuration['debug']['debug_scheduler'] == True:
            log.msg('ScheduledTaskManager: checking for tasks to run...')
            log.msg(self.tasks)
        tasks_to_run = [task for task in self.tasks if
                            task.next_scheduled_runtime < datetime.now()]
        if self.configuration['debug']['debug_scheduler'] == True:
            log.msg('Scheduledtaskmanager: %d tasks found.' % len(tasks_to_run))
        for task in tasks_to_run:
            task.run()
