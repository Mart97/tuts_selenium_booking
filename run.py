from booking.booking import Booking

try:
    with Booking() as bot:
        bot.land_first_page()
        bot.change_currency(currency='BRL')
        bot.select_place_to_go(input('Where do you want to go to? '))
        bot.select_dates(check_in_date=input('When do you want to go? '), check_out_date=input('When do you want to return? '))
        bot.select_adults(int(input('How many adults in this trip? ')))
        bot.click_search()
        bot.drop_popup()
        bot.apply_filtrations()
        bot.driver.refresh()   # A workaround to let our bot grab the data properly
        bot.report_results()

except Exception as e:
    if 'no such element' in str(e):
        print('The bot could not find the element to click! Exiting...')
    elif 'element not interactable' in str(e):
        print('Something went wrong while dealing with the page! Exiting...')
    else:
        raise
