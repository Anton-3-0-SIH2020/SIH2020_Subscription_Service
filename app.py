import os
from get_daily_data import get_daily_data
from convert_daily_data_to_pdf import store_file_as_pdf
from get_user_list import get_user_list


def app(event=None, context=None):
    latest_ca = get_daily_data()
    response, filename = store_file_as_pdf(latest_ca)
    if not response:
        print("Some error occurred")
        return
    else:
        if os.path.exists(filename):
            os.remove(filename)
        else:
            print("The file does not exist")
        mailing_list = [user.get('email') for user in get_user_list()]
        print(mailing_list)
