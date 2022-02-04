"""Import packages and modules."""
import os
from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from events_app.models import Event, Guest

# Import app and db from events_app package so that we can run app
from events_app import app, db

main = Blueprint('main', __name__)


##########################################
#                Routes                  #
##########################################


#------------------------------/

@main.route('/')
def index():
    """Show upcoming events to users!"""
    events=Event.query.all()
    return render_template('index.html', events=events)


#------------------------------/create

@main.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        
        new_event_title = request.form.get('title')
        new_event_description = request.form.get('desc')
        date = request.form.get('date')
        time = request.form.get('time')

        try:
            date_and_time = datetime.strptime(
                f'{date} {time}',
                '%Y-%m-%d %H:%M')
        except ValueError:
            return render_template('create.html',  
                error='Incorrect datetime format! Please try again.') 


        new_event = Event(title = new_event_title, desc = new_event_description, date_time = date_and_time)
        db.session.add(new_event)
        db.session.commit()
        flash('Event created.')
        return redirect(url_for('main.index'))
    else:
        return render_template('create.html')



#------------------------------/show one

@main.route('/event/<event_id>', methods=['GET'])
def event_detail(event_id):
    event = Event.query.filter_by(id=event_id).first_or_404()
    guests = Guest.query.all()
    total_guests = Guest.query.count()

    # date = 
    # time = 
    return render_template('event_detail.html', event = event, total_guests = total_guests, guests = guests)


#------------------------------/rsvp

@main.route('/event/<event_id>', methods=['POST'])
def rsvp(event_id):
    # TODO: Get the event with the given id from the database
    guests = Guest.query.all()
    events = Event.query.all()
    total_guests = Guest.query.count()
    is_returning_guest = request.form.get('returning')
    guest_name = request.form.get('guest_name')
    add_event = Event.query.filter_by(id=event_id).one()

    if is_returning_guest:
        guest = Guest.query.filter_by(name=guest_name).first()
        print(guest, "IM HERE")
        if guest is not None:
            print("guest is not none")
            # add_event = Event.query.filter_by(id=event_id).one()
            add_event.guests.append(guest)

            db.session.add(add_event)
            db.session.commit()
        else:
            print("guest is none")

            return render_template('event_detail.html', error = "Guest not in database!", event=add_event, event_id=event_id, guests = guests, total_guests = total_guests)

    else:
        guest_email = request.form.get('email')
        guest_phone = request.form.get('phone')

        new_guest = Guest(name=guest_name, email=guest_email,phone=guest_phone)
        add_event = Event.query.filter_by(id=event_id).one()
        add_event.guests.append(new_guest)

        db.session.add(new_guest)
        db.session.commit()
        
    
    flash('You have successfully RSVP\'d! See you there!')
    return redirect(url_for('main.event_detail', event_id=event_id, total_guests = total_guests, guests = guests, event=add_event)), print(total_guests)


#------------------------------/show one guest

@main.route('/guest/<guest_id>')
def guest_detail(guest_id):
    # TODO: Get the guest with the given id and send to the template
    guest = Guest.query.filter_by(id=guest_id).one()
    
    return render_template('guest_detail.html', guest = guest)
