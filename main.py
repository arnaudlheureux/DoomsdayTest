import kivy
kivy.require('1.0.6') # replace with your current kivy version !
from datetime import date
from random import randint
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.properties import StringProperty


# Return doomsday of year
def doomsday(year) :
    # For Gregorian calendar
    return (2 + year + year//4 - year//100 + year//400) % 7

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

adj = [3, 28, 0, 4, 9, 6, 11, 8, 5, 10, 7, 12]

adjLeap = [4, 29, 0, 4, 9, 6, 11, 8, 5, 10, 7, 12]

# A year is a leap year if divisible by 4 but not 100 except if it is divisible by 400
def leapYear(year) :
    if( year % 4 != 0) :
        return False
    elif (year % 100 != 0) :
        return True
    elif (year % 400 != 0) :
        return False
    else : return True 

def dayOfTheWeek(day, month, year) :
    if(leapYear(year)):
        return (day - adjLeap[month - 1] + doomsday(year)) % 7
    else :
        return (day - adj[month - 1] + doomsday(year)) % 7

def getVerb(day, month, year, today):
    todayY = int(today[6:10])
    todayM = int(today[3:5])
    todayD = int(today[0:2])

    #today is in the format 
    if(todayY > year) :
        return "was"
    elif(todayY < year) :
        return "will be"
    else :
        if(todayM > month):
            return "was"
        elif(todayM < month):
            return "will be"
        else :
            if(todayD > day):
                return "was"
            elif(todayD < day):
                return "will be"
            else :
                return "is"

class Game :
    def __init__(self):
        self.restart()

    def restart(self):
        day = randint(1,31)

        month = randint(1,12)

        if((day == 31 or day == 30 or day == 29) and month == 2) :
            day = 28
        elif(day == 31 and (month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12)) :
            day = 30

        year = randint(1800, 2199)

        today = date.today()

        # dd/mm/YY
        d1 = today.strftime("%d/%m/%Y")

        verb = getVerb(day, month, year, d1)

        self.clue = months[month - 1] + " " + str(day) + ", " + str(year) + " " + verb + " a... "
        self.answer = dayOfTheWeek(day, month, year)
        self.exp = months[month - 1] + " " + str(day) + ", " + str(year) + " " + verb + " a " + days[self.answer] + " (The doomsday " + verb + " a " + days[doomsday(year)] +")"
        self.over = False

game = Game()

class MyWidget(Widget):
    display = StringProperty()

    def __init__(self, **kwargs):
        super(MyWidget, self).__init__(**kwargs)
        #new game is starteds

        self.display = game.clue
    
    def answer(self, dayNumber):
        if(game.over) :
            for i in range(0,7):
                tempId = "button" + str(i)
                self.ids[tempId].background_color = 1,1,1,1

            game.restart()
            self.display = game.clue
        else :
            if(dayNumber == game.answer) :
                #right answer
                correctId = "button" + str(dayNumber)
                self.ids[correctId].background_color = .0, 1, .4, .85 

            else :
                #incorrect answer
                self.display = game.exp

                incorrectId = "button" + str(dayNumber)
                correctId = "button" + str(game.answer)

                self.ids[correctId].background_color = .0, 1, .4, .85
                self.ids[incorrectId].background_color = 1, .3, .4, .85
            game.over = True


class MyApp(App):
    def build(self):
        self.title = 'Doomsday Algorithm Test'
        Config.set('graphics', 'width', '700')
        Config.set('graphics', 'height', '80')

        return MyWidget()

if __name__ == '__main__':
    MyApp().run()











