from apps.users.models import User
from typing import Any, List


class WeeklyScheduleUpdater:
    def __init__(self, user: User, weekly_schedule_data: list) -> None:
        self.user = user
        self.weekly_schedule_data = weekly_schedule_data        
        
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.update()
    
    def update(self):
        old_weekly_schedule = self.user.get_schedule()
        
        for old_daily_schedule in old_weekly_schedule:
            print('handle')
            daily_data = next((daily_data for daily_data in self.weekly_schedule_data if daily_data.get('week_day') == old_daily_schedule.week_day), None)
            
            if daily_data:
                is_day_off = daily_data.get('is_day_off')
                
                if old_daily_schedule.is_day_off and not is_day_off:
                    old_daily_schedule.mark_as_work_day(daily_data)
                    
                elif not old_daily_schedule.is_day_off and is_day_off:
                    old_daily_schedule.mark_as_day_off()
                    
                elif old_daily_schedule.is_day_off and is_day_off:
                    pass
                
                elif not old_daily_schedule.is_day_off and not is_day_off:
                    old_daily_schedule.update_work_time(daily_data)
                    
                else:
                    raise Exception('Incorrect updating week day case.')
                
        