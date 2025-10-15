from datetime import datetime,timedelta, date
from collections import defaultdict
import json

class Task:
    def __init__(self, category, description, year, mth, day, priority, status= 'Pending'):
        self.category = category
        self.description = description
        self.due_date = datetime(year,mth,day)
        self.priority = priority
        self.status = status
    
    def __str__(self):
        return f'''*[{self.status}]* {self.category} | -- {self.description} --\n- deadline {self.due_date.strftime('%d %B %Y')}!!!\n- priority: {self.priority}'''
        
    def convert_to_dict(self):
        return {'category' : self.category, 'description': self.description, 'due date': self.due_date.strftime('%Y-%m-%d'), 'priority': self.priority, 'status': self.status}

class CycleTracker:
    def __init__(self, year,mth,day, cycle_lenght =28):
        self.category = 'HEALTH'
        self.start_day = datetime(year,mth,day)
        self.cycle_lenght = cycle_lenght

    def __str__(self):
        return f'**[{self.category}]**\nLogged period - {self.start_day.strftime("%d %B %Y")}'

    
class TaskManager:
    def __init__(self):
        self.task = defaultdict(list)

    def add_task(self,category, description, year, mth, day, priority, status= 'Pending'):
        task = Task(category, description, year, mth, day, priority, status)
        self.task[category].append(task)
        return f'Task added - {task}'

    def change_deadline(self,keyword, day, mth, year):
        for category, tasks in self.task.items():
            for task in tasks:
                if keyword.lower() in task.description:
                    new_deadline  = datetime(year, mth, day)
                    added_days = (new_deadline - task.due_date).days
                    task.due_date = new_deadline
                    return f'Deadline for [[{task.category}]] -- {task.description} set on {task.due_date}\n{added_days} added days - HURRY UP'
            
    def days_left(self,keywords):
        today = datetime.today()
        for category, tasks in self.task.items():
            for task in tasks:
                if keywords.lower() in task.description.lower():
                    days_left = (task.due_date - today).days
                    return f'Deadline for [[{task.category}]] -- {task.description} --will finish in {days_left} days !!'

    def mark_if_done(self, keyword):
        self.completed_tasks = []
        for category, tasks in self.task.items():
            for task in tasks:
                if keyword.lower() in task.description.lower():
                    self.completed_tasks.append(task)
                    task.status = 'DONE'
        return f'** Marekd as DONE: {[t.description for t in self.completed_tasks]} **'
    
    def remove_task(self,keyword):
        removed_tasks = []
        for category, tasks in self.task.items():
            for task in tasks:
                if keyword.lower() in task.description.lower():
                    tasks.remove(task)
                    removed_tasks.append(task.description)
                    return f'{task.category} - {task.description} removed'
                return 'Not matching task found'

    def show_tasks(self):
        print('All ACTIVE tasks:\n')
        for category, tasks in self.task.items():
            print(f'Category: {category}')
            for task in tasks:
                print(f'{task}\n')

    def save_to_file(self, filename = 'my_tasks.json' ):
        if not filename.endswith('.json'):
            filename += '.json'
        my_tasks = {}
        for category, tasks in self.task.items():
            my_tasks[category]=[task.convert_to_dict() for task in tasks]
        with open(filename, 'w') as f:
            json.dump(my_tasks, f ,indent=4)
        return my_tasks
    
class CycleTrackerManager:
    def __init__(self):
        self.periods = []

    def log_period(self, year,mth,day):
        period = CycleTracker(year,mth,day)
        self.periods.append(period)
        return str(period)
    
    def next_period(self):
        if not self.periods:
            return 'No period logs'
        last_period = self.periods[-1]
        next_period_predict = last_period.start_day + timedelta(days = last_period.cycle_lenght)
        days_until_next_period = next_period_predict.date() - datetime.today().date()
        return f'Next period predict start - {next_period_predict.strftime("%d %B %Y")} - in {days_until_next_period.days} days'
    
    def average_cycle_days(self):
        lenght_day = []
        if len(self.periods) >=2:
            for i in range (len(self.periods)-1):
                lenght = self.periods[i+1].start_day - self.periods[i].start_day
                lenght_day.append(lenght.days)
            avg_lenght = sum(lenght_day) // len(lenght_day)
        return f'Average period lenght is {avg_lenght} days'
    
    def get_next_period_day(self):
        if not self.periods:
            return 'No period logs'
        last_period = self.periods[-1]
        return last_period.start_day + timedelta(days= last_period.cycle_lenght)
    
    def ovulation_day(self):
        ovulation = self.get_next_period_day() - timedelta(days = 14)
        return f'Ovulation - {ovulation.strftime("%d %B %Y")}'

if __name__ == '__main__':
    manager = TaskManager()
    manager.add_task('LEARNING', 'obiektowka', 2025,8,18, 'HIGH', status='Pending')
    manager.add_task('WORK', 'Clean email',2025,7,20,'LOW', 'PENDING')
    manager.add_task('LOVE', 'Wedding anniversary - find some restaurant', 2025,8,5, 'HIGH',status='Pending')
    manager.add_task('LEARNING','SOLID rules', 2025,7,25, 'MEDIUM', status='Pending')
    # print(manager.add_task('LEARNING', 'obiektowka', 2025,8,18, 'HIGH', status='Pending'))
    # manager.show_tasks()
    # manager.mark_if_done('email')
    # print(manager.mark_if_done('email'))
    # print(manager.days_left('obiektowka'))
    # print(manager.change_deadline('email', 25,7,2025))
    # print(manager.remove_task('solid'))
    # print(manager.save_to_file(filename='my tasks.json'))

    cycle = CycleTrackerManager()
    cycle.log_period(2024,10,19)
    cycle.log_period(2024,11,16)
    cycle.log_period(2024,12,16)
    cycle.log_period(2025,1,9)
    cycle.log_period(2025,2,8)
    cycle.log_period(2025,3,6)
    cycle.log_period(2025,4,4)
    cycle.log_period(2025,5,5)
    cycle.log_period(2025,5,29)
    cycle.log_period(2025,6,30)
    # print(cycle.next_period())
    # print(cycle.average_cycle_days())
    print(cycle.ovulation_day())