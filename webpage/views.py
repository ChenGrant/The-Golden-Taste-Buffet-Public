from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import redirect
from django.conf import settings
from .models import Reservation
from datetime import date, time, datetime

# name should have no digits


website_link = 'http://www.thegoldentastebuffet.com/'
wzw_email = '************'
min_deliv_hours = 3
max_deliv_days = 30

def is_legal_date(day, month, year):
    isValidDate = True
    try:
        datetime(int(year), int(month), int(day))
    except ValueError:
        isValidDate = False
    return isValidDate


def convert24(time):
    if time[-2:] == "am" and time[:2] == "12":
        return "00" + time[2:-2]
    elif time[-2:] == "am":
        return time[:-2]
    elif time[-2:] == "pm" and time[:2] == "12":
        return time[:-2]
    else:
        return str(int(time[:2]) + 12) + time[2:8]


def is_valid_delivery_date(delivery_dt):
    today_dt = datetime.now()
    time_delta = delivery_dt - today_dt
    return time_delta.days >= 0


def delivery_date_is_today(delivery_dt):
    today_dt = datetime.now()
    delta = delivery_dt - today_dt
    return today_dt.date() == delivery_dt.date()

def delivery_date_is_in_future(delivery_dt):
    today_dt = datetime.now()
    delta = delivery_dt - today_dt
    return today_dt.date() < delivery_dt.date()

def delivery_date_valid_today(delivery_dt):
    today_dt = datetime.now()
    delta = delivery_dt - today_dt
    return delta.total_seconds() / 3600 > min_deliv_hours

def delivery_date_valid_future(delivery_dt):
    today_dt = datetime.now()
    delta = delivery_dt - today_dt
    return delta.total_seconds() / 86400 < max_deliv_days

def create_datetime(year, month, day, hour, minute, am_pm):
    problems = []
    # Check if they chose a non-zero day, month, and Year (must be true)
    if day != "0" and month != "0" and year != "0" and hour != "00" and minute != "-1":
        # convert month to number
        all_month = ['January', 'February', 'March', 'April','May', 'June', 'July', 'August','September', 'October', 'November', 'December']
        index = 0
        for x in all_month:
            index = index + 1
            if month == x:
                month = index
                break
        # check if date is legal
        if is_legal_date(day, month, year):
            # make time
            time = convert24(hour + ":" + minute + ":00 " + am_pm)
            hour = time[0:2]
            minute = time[3:5]
            # datetime(year, month, day, hour, minute)
            delivery_dt = datetime(int(year), int(month), int(day), int(hour), int(minute))
            # if datetime is a valid delivery date (today or in the future):
            if is_valid_delivery_date(delivery_dt):
                if delivery_date_is_today(delivery_dt):
                    if delivery_date_valid_today(delivery_dt):
                        return [delivery_dt]
                    else:
                        problems.append("Since the reservation is today, the reservation time must be at least "+str(min_deliv_hours  )+" hours from the time of reservation.")
                if delivery_date_is_in_future(delivery_dt):
                    if delivery_date_valid_future(delivery_dt):
                        return [delivery_dt]
                    else:
                        problems.append("The reservation time has to be within the next "+str(max_deliv_days )+" days.")
            else:
                problems.append("The date is not in the future.")
        else:
            problems.append("The combination of the chosen date, month, and year is impossible.")
    else:
        if day == "0":
            problems.append("No day is chosen.")
        if month == "0":
            problems.append("No month is chosen.")
        if year == "0":
            problems.append("No year is chosen.")
        if hour == "00":
            problems.append("No hour is chosen.")
        if minute == "-1":
            problems.append("No minute is chosen.")
    return [problems]



def valid_phone_number(number):
    if len(number.strip()) != 0 and number.isnumeric():
        return True
    return False

def valid_guests(number):
    try:
        number = int(number)
        if number > 0:
            return True
        return False
    except ValueError:
        return False



















def home_english(request):
    if request.method == 'POST':
        name = request.POST.get('reservation_form_name')
        email = request.POST.get('reservation_form_email')
        phone_number = request.POST.get('reservation_form_phone_number')
        number_of_guests = request.POST.get('reservation_form_number_of_guests')
        message = request.POST.get('reservation_form_message')
        month = request.POST.get('delivery_month')
        day = request.POST.get('delivery_day')
        year = request.POST.get('delivery_year')
        hour = request.POST.get('delivery_hour')
        minute = request.POST.get('delivery_minute')
        am_pm = request.POST.get('delivery_am_pm')

        # creates email body
        email_body = "Name: "+name
        email_body = email_body+ "\nEmail: "+email
        email_body = email_body+ "\nPhone Number: "+phone_number
        email_body = email_body+ "\nNumber of Guests: "+number_of_guests
        if len(message)!=0:
            email_body = email_body +"\nMessage: "+message
        email_body = email_body+ "\nReservation Date: "+month+ " "+day+ ", "+year
        email_body = email_body+ "\nReservation Time: "+hour+ ":"+minute+ " "+am_pm

        # created delivery_datetime for database
        reservation_datetime = create_datetime(year, month, day, hour, minute, am_pm)[0]
        valid_reservation_date = isinstance(reservation_datetime, datetime)


        if len(name.strip())!=0 and len(email.strip())!= 0 and valid_phone_number(phone_number) and valid_guests(number_of_guests) and valid_reservation_date:
            #create instance of reservation model for database
            Reservation.total_reservations = Reservation.objects.count()+1
            currReservation = Reservation(
                reservation_number = Reservation.total_reservations + 11729,
                customer_name = name,
                customer_email = email,
                number_of_guests = number_of_guests,
                phone_number = phone_number,
                message = message,
                reservation_datetime = reservation_datetime
            )
            currReservation.save()

            email_body = "Reservation Number: "+str(currReservation.reservation_number)+"\n"+email_body
            #send to wzw
            company_email_body = "Incoming Reservation.\n\n"+email_body
            send_mail("Incoming Reservation #"+str(currReservation.reservation_number), company_email_body, settings.EMAIL_HOST_USER,[wzw_email], fail_silently=False)

            #send to user
            user_email_body = "Thank you for your reservation. Below is the information in the form:\n\n"+email_body+"\n\nCancel the reservation: "+website_link+"email_cancel/"
            send_mail("Reservation Confirmation #"+str(currReservation.reservation_number), user_email_body, settings.EMAIL_HOST_USER,[email], fail_silently=False)

            return render(request, 'webpage/email_sent_english.html', {'email': email})

        else:
            reservation_errors = []
            if len(name.strip())==0:
                reservation_errors.append("Name field is empty")

            if len(email.strip())==0:
                reservation_errors.append("Email field is empty")

            if not valid_phone_number(phone_number):
                reservation_errors.append("Invalid phone number")

            if not valid_guests(number_of_guests):
                reservation_errors.append("Invalid number of guests")

            if not valid_reservation_date:
                for date_error in reservation_datetime:
                    reservation_errors.append(date_error)

            return render(request, 'webpage/email_failed_english.html', {'reservation_errors': reservation_errors})

    return render(request, 'webpage/home_english.html')


def email_sent_english(request):
    return render(request, 'webpage/email_sent_english.html' )


def email_failed_english(request):
    return render(request, 'webpage/email_failed_english.html' )


def email_cancel_english(request):
    if request.method == 'POST':
        reservation_number = request.POST.get('reservation_number')
        reservation_email = request.POST.get('reservation_email')
        if not reservation_number.isdigit() or len(reservation_email) == 0:
            if not reservation_number.isdigit():
                messages.success(request, f'Reservation number is not a positive integer {reservation_number}.')
            if len(reservation_email)==0:
                messages.success(request, f'Email is empty.')
            return redirect("email_cancel_english")
        else:
            reservation = Reservation.objects.filter(
                customer_email = reservation_email,
                reservation_number = int(reservation_number)
            ).first()
            if not isinstance(reservation, Reservation):
                messages.success(request, f'No reservation exists with the corresponding reservation number and email.')
                return redirect("email_cancel_english")
            else:
                if reservation.cancelled == True:
                    messages.success(request, f'This Reservation is already cancelled.')
                    return redirect("email_cancel_english")
                else:
                    reservation.cancelled = True
                    reservation.save()
                    body = "The following reservation has been cancelled.\n\n"
                    body = body + "Reservation Number: " + str(reservation.reservation_number) + "\n"
                    body = body + "Name: " + reservation.customer_name + "\n"
                    body = body + "Email: " + reservation.customer_email + "\n"
                    body = body + "Phone Number: " + reservation.phone_number + "\n"
                    body = body + "Number of Guests: "+ str(reservation.number_of_guests) + "\n"
                    if len(reservation.message)!=0:
                        body = body +"Message: "+reservation.message+ "\n"
                    body = body + "\nReservation Time: " + reservation.str_reservation_date_and_time() + "\n"
                    body = body + "Reserved On: " + reservation.str_reserved_datetime() + "\n"

                    #send email to wzw that reservation is cancelled
                    send_mail("Cancel Reservation #"+str(reservation.reservation_number), body, settings.EMAIL_HOST_USER,[wzw_email], fail_silently=False)
			        #send email to user that reservation was cancelled
                    send_mail("Cancel Reservation Confirmation#"+str(reservation.reservation_number), body, settings.EMAIL_HOST_USER,[reservation.customer_email], fail_silently=False)
                    return redirect ("email_cancel_confirm_english")

    return render(request, 'webpage/email_cancel_english.html' )


def email_cancel_confirm_english(request):
    return render(request, 'webpage/email_cancel_confirm_english.html')


'''

def home_chinese(request):
    # form handling, but chinese email sent
    return render(request, 'webpage/home_chinese.html')

def email_sent_chinese(request):
    return render(request, 'webpage/email_sent_chinese.html' )


def email_failed_chinese(request):
    return render(request, 'webpage/email_failed_chinese.html' )


def email_cancel_chinese(request):
    return render(request, 'webpage/email_cancel_chinese.html' )

def email_cancel_confirm_chinese(request):
    return render(request, 'webpage/email_cancel_confirm_chinese.html' )

'''
