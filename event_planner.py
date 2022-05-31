from datetime import date, datetime
from dateutil.relativedelta import *


class EventPlanner:
    """ Event planner will spread the total_time across the days passed by the user and returns the consecutive dates
    to schedule the binge"""
    def __init__(self, name, days, daily_hours, total_time):
        self.__now = str(datetime.now()).split(' ')
        self.__now_date = self.__now[0]
        self.__now_time = self.__now[1]
        self.__now_day = datetime.today().weekday()
        self.__set_title(name)
        self.__days = [0, 0, 0, 0, 0, 0, 0]
        self.__set_days(days)
        self.__daily_hours = [0, 0, 0, 0, 0, 0, 0]
        self.__set_daily_hours(daily_hours)
        self.__event_time = int(total_time)  # show time should be in minutes
        self.__dates_generated = []

    def __set_title(self, title):
        if isinstance(title, str):
            self.__title = title

    def __get_title(self):
        return self.__title

    title = property(__get_title, __set_title)

    def __set_days(self, days):
        if isinstance(days, list) and len(days) == 7:
            count = 0
            for i in range(7):
                if days[i] == 1:
                    self.__days[i] = 1
                    count += 1
            if count == 0:
                raise ValueError("No days selected to plan")

    def __set_daily_hours(self, daily_hours):
        """ converts the user inputted daily watch hours to minutes and sets the __daily_hours """
        if isinstance(daily_hours, list) and len(daily_hours) == 7:
            count = 0
            for i in range(7):
                if isinstance(daily_hours[i], (int, float)) and daily_hours[i] != 0 and self.__days[i] == 1:
                    self.__daily_hours[i] = daily_hours[i] * 60  # converts to minutes
                    count += 1
            if count == 0:
                raise ValueError("No hours inputted for the selected days")

    def date_generator(self):
        time_to_schedule = self.__event_time
        index = self.__now_day
        date_sch = self.__now_date
        while time_to_schedule > 0:
            if self.__days[index] == 1:
                if date_sch == self.__now_date and self.check_schedule_today():

                    self.__dates_generated.append(date_sch)
                    time_to_schedule -= self.__daily_hours[index]
                    index, date_sch = self.add_to_dates_generated(index, date_sch)
                    time_to_schedule -= self.__daily_hours[index]

                else:
                    index, date_sch = self.add_to_dates_generated(index, date_sch)
                    time_to_schedule -= self.__daily_hours[index]

            else:
                index, date_sch = self.add_to_dates_generated(index, date_sch)
                time_to_schedule = time_to_schedule - int(self.__daily_hours[index])  # converting hours to minutes

        return self.__dates_generated

    def add_to_dates_generated(self, index, date_sch):
        index, day_increment = self.next_index(index)
        date_sch = datetime.fromisoformat(date_sch)
        date_sch = (str(date_sch + relativedelta(days=day_increment)).split(' '))[0]
        self.__dates_generated.append(date_sch)
        return index, date_sch

    def check_schedule_today(self):
        index = self.__now_day
        time_now = self.__now_time.split(':')
        if self.__days[index] == 1 and 23 - int(time_now[0]) + (60 - int(time_now[1]))/60 > self.__daily_hours[index]/60:
            return True
        else:
            return False

    def next_index(self, index, count=0):
        """ given an index, the function will return the next index and number of days for the next schedule"""
        ind = index
        count = count
        if ind == 6:
            for i in range(7):
                if self.__days[i] == 1:
                    ind = i
                    count += 1
                    return ind, count
                else:
                    count += 1
        else:
            for i in range(ind+1, 7):
                if self.__days[i] == 1:
                    ind = i
                    count += 1
                    return ind, count
                elif i == 6:
                    count += 1
                    return self.next_index(6, count)
                else:
                    count += 1


if __name__ == '__main__':
    ep = EventPlanner("test", [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], 480)
    print(ep.check_schedule_today())
    print(ep.next_index(1))
    ep.date_generator()






