from subprocess import Popen, PIPE
from random import choice
from datetime import datetime, timedelta, date

startFromSunday = datetime.strptime('2013-03-24', '%Y-%m-%d').date()
contributionCalendar = [
    [0,0,1,0,1,0,1,1,0,1,0,0,1,0,0,1,1,1,0,0,0,1,1,1,0,1,0,1,1,1,0,1,0,1,0,1,0,1,0,1,1,0,0],
    [0,0,3,0,3,0,3,0,0,3,0,0,3,0,0,3,0,3,0,0,0,3,0,0,0,3,0,0,3,0,0,3,0,3,0,3,0,3,0,3,0,3,0], #mondays
    [0,0,3,0,3,0,3,0,0,3,0,0,3,0,0,3,0,3,0,0,0,3,0,0,0,3,0,0,3,0,0,3,0,3,0,3,0,3,0,3,0,3,0],
    [0,0,3,3,3,0,3,3,0,3,0,0,3,0,0,3,0,3,0,0,0,3,0,3,0,3,0,0,3,0,0,3,3,3,0,3,0,3,0,3,3,0,0],
    [0,0,6,0,6,0,6,0,0,6,0,0,6,0,0,6,0,6,0,0,0,6,0,6,0,6,0,0,6,0,0,6,0,6,0,6,0,6,0,6,0,6,0],
    [0,0,6,0,6,0,6,0,0,6,0,0,6,0,0,6,0,6,0,0,0,6,0,6,0,6,0,0,6,0,0,6,0,6,0,6,0,6,0,6,0,6,0], #fridays
    [0,0,9,0,9,0,9,9,0,9,9,0,9,9,0,9,9,9,0,0,0,9,9,9,0,9,0,0,9,0,0,9,0,9,0,9,9,9,0,9,9,0,0],
]

def execute(cmd):
    Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE).wait()

def log(msg):
    execute('echo `date` - %s >> log' % msg)

def prepare_stage():
    execute('date >> data')
    execute('git add data')

def commit(message = 'Add new feature'):
    execute('git commit -m "%s"' % message)

def push():
    execute('git push origin master')

def generate_commit_message():
    action = choice(['add', 'update', 'optimize', 'remove', 'fix', 'hotfix', 'rewrite', 'move', 'refactor', 'change'])
    object1 = choice(['', 'rest', 'soap', 'javascript', 'php', 'python', 'public', 'security'])
    object2 = choice(['api', 'method', 'property', 'interface', 'class', 'unit tests', 'config'])
    return '%s %s %s' % (action, object1, object2)

def get_commits_number(testDate):
    daysDifference = (testDate - startFromSunday).days
    week = int(round(daysDifference / 7))
    if week > len(contributionCalendar[0]):
        log('finished')
        exit()
    day = daysDifference - week * 7
    return contributionCalendar[day][week]

def test_print():
    for a in range(0, len(contributionCalendar)):
        for b in range(0, len(contributionCalendar[0])):
            testDate = startFromSunday + timedelta(days=a, weeks=b)
            result = get_commits_number(testDate)
            if result == 0:
                print ' ',
            else:
                print result,
        print

if __name__ == '__main__':
    testDate = date.today()
    commits = get_commits_number(testDate)
    log('%d commits' % commits)
    if commits > 0:
        for n in xrange(0, commits):
            prepare_stage()
            commit(generate_commit_message())
        push()
