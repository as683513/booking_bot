from booking.booking import Booking

# inst = Booking()

# inst.set_window_position(0,0)
# print('resizing window...')
# inst.set_window_size(993, 963)
# inst.land_first_page()

with Booking(teardown=True) as bot:
    #open window on second monitor
    bot.set_window_rect(x=2000, y=0, width=1920, height=964)
    bot.land_first_page()
    bot.change_currency(currency='GBP') 
    bot.select_place_to_go('Columbus, Ohio')
    bot.select_dates(check_in_date = '2022-06-28', check_out_date='2022-06-30')
    bot.select_adults(20)
    bot.submit()
