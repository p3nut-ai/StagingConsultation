from flask import Flask, request, redirect, url_for, session, render_template, flash, jsonify
from email_sender import *
from sqlalchemy import or_
from models import db, User, Consultation, Availability, FAQS
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from termcolor import colored
import colorama

colorama.init()

def register_routes(app):
  
    def check_login():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        else:
            return True    

    @app.route('/approve/<int:id>', methods=['POST']) 
    def approve_consultation(id):
        consultation = Consultation.query.get(id)
        user_id = request.form.get('user_id')
        users = Consultation.query.get(id)
        approved_by = User.query.filter_by(id = session['user_id']).first()

        users.approved_by = approved_by.username

        consultant = approved_by.username
        sender_email = "kaizensolution1@gmail.com"
        receiver_email = users.email
        firstName = users.name
        lastName = users.lastname
        approved_date = consultation.date
        approved_Start_time = consultation.start_time
   
        if consultation:
            # check if status is approved or not
            if consultation.status != 'approved':
                consultation.status = 'approved'
                approve_email_reporter(receiver_email, firstName, lastName, sender_email, approved_date,approved_Start_time, consultant)
                db.session.commit()
            else:
                print(colored("[!] Consultation already approved [!]" , "yellow"))    
        return redirect(url_for('admin'))  

    @app.route('/reject/<int:id>', methods=['POST'])
    def reject_consultation(id):
        consultation = Consultation.query.get(id)
        approved_by = User.query.filter_by(id = session['user_id']).first()
        users = Consultation.query.get(id)

        consultant = approved_by.username
        sender_email = "kaizensolution1@gmail.com"
        receiver_email = users.email
        firstName = users.name
        lastName = users.lastname
        approved_date = consultation.date
        approved_Start_time = consultation.start_time
        consultation.approved_by = approved_by.username
        if consultation:
             # check if status is rejected or not
            if consultation.status != 'rejected':
                consultation.status = 'rejected'
                rejected_email_reporter(receiver_email, firstName, lastName, sender_email, approved_date,approved_Start_time, consultant)
                db.session.commit()
            else:
                print(colored("[!] Consultation already rejected [!]" , "yellow"))    
        return redirect(url_for('admin'))  

    @app.route('/reconsidered/<int:id>', methods=['POST'])
    def reconsidered(id):
        consultation = Consultation.query.get(id)
        approved_by = User.query.filter_by(id = session['user_id']).first()
        users = Consultation.query.get(id)
        consultant = approved_by.username
        sender_email = "kaizensolution1@gmail.com"
        receiver_email = users.email
        firstName = users.name
        lastName = users.lastname
        approved_date = consultation.date
        approved_Start_time = consultation.start_time
        consultation.approved_by = approved_by.username
        if consultation:
            consultation.status = 'reconsidered'
            reconsidered_email_reporter(receiver_email, firstName, lastName, sender_email, approved_date,approved_Start_time, consultant)
            db.session.commit()
        return redirect(url_for('admin'))  

    # add new faq to the DB
    @app.route('/add_faq', methods=['POST'])
    def submit_faq():
        faq_title = request.form.get("faq-title")
        faq_description = request.form.get("faq-description")

        if faq_title and faq_description:
            new_faq = FAQS(faq_title=faq_title, faq_description=faq_description)
            db.session.add(new_faq)
            db.session.commit()
        else:
            print(colored("[-] No faq submitted [-]", "red"))    

        return redirect(url_for('admin', faq_title=faq_title, faq_description=faq_description))
    
    # FAQ edit endpoint
    @app.route('/edit_faq/<int:id>' , methods=['POST'])
    def edit_faq(id):
        data = request.json
        print(f"Received data {data}")
        faq = FAQS.query.get(id)
        if faq:
            faq.faq_title = data['title']
            faq.faq_description = data['description']
            db.session.commit()
            return jsonify({'message': 'FAQ updated successfully'}), 200
        return redirect(url_for('admin')) 

    # FAQ delete endpoint
    @app.route('/delete_faq/<int:id>' , methods=['POST'])
    def delete_faq(id):
        faq = FAQS.query.get(id)
        if faq:
            db.session.delete(faq)
            db.session.commit()
        return jsonify({'success': True, 'message': 'FAQ deleted'})

    @app.route('/add_availability', methods=['POST'])
    def add_availability():
        date = request.form.get('date')
        start_time = request.form.get('start-time')
        end_time = request.form.get('end-time')
        
        user_id = session['user_id']  # Get the logged-in user's ID

        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        day_of_week = date_obj.strftime('%A')  
        start_time_obj = datetime.strptime(start_time, '%H:%M').time()
        end_time_obj = datetime.strptime(end_time, '%H:%M').time()

        # Create a new availability record
        new_availability = Availability(
            date=date_obj,
            day_of_week=day_of_week,
            start_time=start_time_obj.strftime('%I:%M %p'),
            end_time=end_time_obj.strftime('%I:%M %p'),
            user_id=user_id  
        )
        
        db.session.add(new_availability)
        db.session.commit()

        return redirect(url_for('admin'))

    @app.route('/submit', methods=['POST'])
    def submit_consultation():
        name = request.form.get('name')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        consultation_type = request.form.get('consultation-type')
        date = request.form.get('date')
        time = request.form.get('time')
        purpose = request.form.get('purpose')
        
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        day_of_week = date_obj.strftime('%A')
        
        time_obj = datetime.strptime(time, '%H:%M').time()
        time_obj_formatted = time_obj.strftime('%I:%M %p')

        # Create a new consultation record
        new_consultation = Consultation(
            name=name,
            lastname=lastname,
            email=email,
            consultation_type=consultation_type,
            date=date_obj,
            day_of_week=day_of_week,
            start_time=time_obj_formatted,
            purpose=purpose
        )
        db.session.add(new_consultation)
        db.session.commit()
    
        return redirect(url_for('index'))

    @app.route('/logout')
    def logout():
        session.pop('user_id', None)
        return redirect(url_for('login'))

    @app.route('/delete/<int:id>', methods=['POST'])
    def delete_consultation(id):
        consultation = Consultation.query.get(id)
        if consultation:
            db.session.delete(consultation)
            db.session.commit()
        return redirect(url_for('admin')) 

    @app.route('/delete_sched/<int:id>', methods=['POST'])
    def delete_sched(id):
        sched = Availability.query.get(id)
        print(sched)
        if not sched:
            return jsonify({'message': 'Schedule not found.'}), 404

        try:
            # Delete the schedule
            db.session.delete(sched)
            db.session.commit()  # Commit the changes
            
            # Return a success message for deletion
            return jsonify({'message': 'Schedule deleted successfully.'}), 200
            
        except Exception as e:
            # Rollback if there's an error
            db.session.rollback()
            print(f"Error occurred during commit: {e}")
            return jsonify({'message': 'Failed to delete the schedule', 'error': str(e)}), 

    @app.route('/approved_list')
    def approved_list():
        current_datetime = datetime.now()



        approves = (Consultation.query
                .filter(Consultation.status.in_(['approved', 'reconsidered']))
                .filter(Consultation.date >= current_datetime.date())  
                .order_by(Consultation.date, Consultation.start_time)  
                .all())

        # check for the user's search
        query = request.args.get("q")
        searched_item = []
        if query:
            searched = True
            searched_item = Consultation.query.filter( 
                or_(Consultation.name.ilike(f'%{query}%'),
                    Consultation.lastname.ilike(f'%{query}%'))).all()
        else:
            searched = False

        valid_approves = bool(approves) 
        return render_template('approved.html', searched_item=searched_item,searched=searched,approves=approves, valid_approves=valid_approves)


    @app.route('/rejected_list')
    def rejected_list():
        current_datetime = datetime.now()

        rejects = (Consultation.query
                .filter(Consultation.status == 'rejected')
                .filter(Consultation.date >= current_datetime.date())  
                .order_by(Consultation.date, Consultation.start_time)  
                .all())
        

        
        # check for the user's search
        query = request.args.get("q")
        searched_item = []
        if query:
            searched = True
            searched_item = Consultation.query.filter( 
                or_(Consultation.name.ilike(f'%{query}%'),
                    Consultation.lastname.ilike(f'%{query}%'))).all()
        else:
            searched = False

        valid_rejects = bool(rejects) 

        return render_template('rejected.html', searched_item=searched_item, searched=searched,rejects=rejects, valid_rejects=valid_rejects)

    @app.route('/admin') 
    def admin():
        if 'user_id' not in session:
            return redirect(url_for('login'))


        
        approves = Consultation.query.filter_by(status='approved').all()
        rejects = Consultation.query.filter_by(status='rejected').all()
        reconsidered = Consultation.query.filter_by(status='reconsidered').all()
        
        userName = User.query.filter_by(id = session['user_id']).first()

        #kukunin niya yung specific na sched ng user by matching yung user_id at user_id sa session
        availability = db.session.query(Availability, User).join(User).filter(Availability.user_id == session['user_id']).all()
        

        formatted_availability = []
        for availability_instance, user_instance in availability:
            formatted_availability.append({
                'date': availability_instance.date,
                'day_of_week': availability_instance.day_of_week,
                'start_time': availability_instance.start_time,
                'end_time': availability_instance.end_time,
                'username': user_instance.username,
                'user_id': availability_instance.user_id,  
                'availability_id': availability_instance.availability_id,  
            })




        consultations = db.session.query(Consultation).filter(
        Consultation.approved_by.is_(None)  # Fetches consultations with NULL approved_by
        ).all()
        current_user = db.session.query(User).filter_by(id=session['user_id']).first()
        # current_date = date(2025, 11, 2)
        current_date = date.today()
        current_datetime = datetime.now()


        latest_approved = (Consultation.query
                .filter(Consultation.status.in_(['approved', 'reconsidered']))
                .filter(Consultation.date >= current_datetime.date())  
                .order_by(Consultation.date, Consultation.start_time)  
                .first())

        latest_rejected = (Consultation.query
                .filter(Consultation.status == 'rejected')
                .filter(Consultation.date >= current_datetime.date())  
                .order_by(Consultation.date, Consultation.start_time)  
                .first())

        # latest_approved = Consultation.query.filter(
        #     Consultation.status.in_(['approved', 'reconsidered'])
        # ).order_by(Consultation.id.desc()).first()
        


        # latest_rejected = Consultation.query.filter_by(status='rejected').order_by(Consultation.id.desc()).first()

        approves_list = bool(latest_approved)
        rejected_list = bool(latest_rejected)

        matches = db.session.query(User, Consultation).filter(
        User.username == Consultation.approved_by,
        User.id == current_user.id).all()
        print(f"Consultation {matches}")

        reconsidered_len = len(reconsidered)
        approves_len = len(approves)
        consultations_data = reconsidered_len + approves_len
        Rejected_form = len(rejects)
        
        getAllConsultation = Consultation.query.all()
        
        for requestToBeCheck in getAllConsultation:
            if requestToBeCheck.date < current_date:
                sender_email = "kaizensolution1@gmail.com"
                receiver_email = requestToBeCheck.email
                firstName = requestToBeCheck.name
                lastName = requestToBeCheck.lastname
                if requestToBeCheck.status != "expired":
                    requestToBeCheck.status = "expired"
                    expiredRequest(receiver_email, firstName, lastName, sender_email)
                    db.session.commit()
                else:
                    print(colored("[!] Consultation already expired [!]" , "yellow"))    
    
        # check for the user's search
        query = request.args.get("q")
        searched_item = []
        if query:
            searched = True
            searched_item = Consultation.query.filter( 
                or_(Consultation.name.ilike(f'%{query}%'),
                    Consultation.lastname.ilike(f'%{query}%'))).all()
        else:
            searched = False


        faq_title = request.args.get('faq_title')
        faq_description = request.args.get('faq_description')


        # check if nag papasa yung end point ng FAQ sa admin endpoint
        FAQS_entities = FAQS.query.all()
        if faq_title and faq_description:
            isFAQS = True
        else:
            isFAQS = False
            print(colored("[-]  No FAQ submitted [-] ", "red"))    
        

        return render_template('admin.html',isFAQS=isFAQS,FAQS_entities=FAQS_entities,searched_item=searched_item,searched=searched,latest_rejected=latest_rejected,latest_approved=latest_approved,current_date=current_date,matches=matches,Rejected_form=Rejected_form,consultations_data=consultations_data,userName=userName,rejected_list=rejected_list,approves_list=approves_list,consultations=consultations, availabilities=formatted_availability, approves=approves, rejects=rejects)

    # Endpoint for date range search
    @app.route('/search_approved_date', methods=['POST'])
    def search_approved_date():
        start_date_str = request.form.get("start_date")
        end_date_str = request.form.get("end_date")
        
        if not (start_date_str and end_date_str):
            return redirect(url_for('approved_list'))
        
        try:
            # Parse the submitted dates
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            # If parsing fails, redirect to base listing
            return redirect(url_for('approved_list'))
        print(f"start and end {start_date}, {end_date}")
        approves = (Consultation.query
                    .filter(Consultation.status.in_(['approved', 'reconsidered']))
                    .filter(Consultation.date.between(start_date, end_date))
                    .order_by(Consultation.date, Consultation.start_time)
                    .all())
        valid_approves_search = bool(approves)
        
        return render_template('approved.html',
                            approves=approves,
                            valid_approves=valid_approves_search)
    
     # Endpoint for date range search rejected
    
    @app.route('/search_rejected_date', methods=['POST'])
    def search_rejected_date():
        start_date_str = request.form.get("start_date")
        end_date_str = request.form.get("end_date")
        
        if not (start_date_str and end_date_str):
            return redirect(url_for('rejected_list'))
        
        try:
            # Parse the submitted dates
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            # If parsing fails, redirect to base listing
            return redirect(url_for('rejected_list'))
        print(f"start and end {start_date}, {end_date}")
        rejects = (Consultation.query
                    .filter(Consultation.status == 'rejected')
                    .filter(Consultation.date.between(start_date, end_date))
                    .order_by(Consultation.date, Consultation.start_time)
                    .all())
        valid_rejected_search = bool(rejects)
        
        return render_template('rejected.html',
                            rejects=rejects,
                            valid_rejected_search=valid_rejected_search)
    
   
    
    # Search end route for admin dashboard
    @app.route('/search', methods=['POST'])
    def search_entity():
        item_to_be_searched = request.form.get("item")
       

        return redirect(url_for('admin', q = item_to_be_searched))
    
    # Search end route for approved list
    @app.route('/search_approved_list', methods=['POST'])
    def search_approved():
        item_to_be_searched = request.form.get("item")
       

        return redirect(url_for('approved_list', q = item_to_be_searched))
    
    
    # Search end route for rejected list
    @app.route('/search_rejected_list', methods=['POST'])
    def search_rejected():
        item_to_be_searched = request.form.get("item")
        print(f"RECEIVED {item_to_be_searched}")

        return redirect(url_for('rejected_list', q = item_to_be_searched))


    # edit ng form thru modal
    @app.route('/edit/<int:id>', methods=['POST'])
    def edit_form(id):
        data = request.json
        # Find the schedule in the database by ID
        schedule = Availability.query.get(id)
        # print(schedule)
        if schedule:
            try:
                print("entered")
                new_date = datetime.strptime(data['day'], '%Y-%m-%d').date()

                today = datetime.today().date()
                print(f"TODAY: {today}")
                print(f"DATE: {new_date}")
                if new_date < today:
                    print("error outdated")
                    return jsonify({'message': 'The date cannot be set to a past date'}), 400

                schedule.date = new_date
                schedule.day_of_week = new_date.strftime('%A')
                schedule.start_time = data['timeStart']
                schedule.end_time = data['timeEnd']
                db.session.commit()  # Commit the changes
                return jsonify({'message': 'Schedule updated successfully'}), 200
            except Exception as e:
                error_inserting_date_db = False
                return jsonify({'message': 'Failed to edit the schedule', 'error': str(e)}), 500  
        else:
            print("else")
            return jsonify({'error': 'Schedule not found'}), 404

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            user = User.query.filter_by(email=email).first()
            
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                flash('Login successful!', 'success')
                return redirect(url_for('admin'))
            else:
                flash('Invalid credentials. Please try again.', 'danger')

        return render_template('login.html')

    # search log endpoint
    @app.route('/search_log', methods=['POST'])
    def search_logs():
        item_to_be_searched = request.form.get("item")
        return redirect(url_for('logs', q=item_to_be_searched))

    @app.route('/search_logs_date', methods=['POST'])
    def search_logs_date():
        start_date_str = request.form.get("start_date")
        end_date_str = request.form.get("end_date")
        
        if not (start_date_str and end_date_str):
            return redirect(url_for('rejected_list'))
        
        try:
            # Parse the submitted dates
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            # If parsing fails, redirect to base listing
            return redirect(url_for('logs'))
        
        logs = (Consultation.query
                    .filter(Consultation.date.between(start_date, end_date))
                    .order_by(Consultation.date, Consultation.start_time)
                    .all())
        valid_logs_search = bool(logs)
        
        return render_template('logs.html',
                            logs=logs,
                            valid_logs_search=valid_logs_search)

    @app.route('/logs')
    def logs():
         # check for the user's search
        query = request.args.get("q")
        searched_item = []
        if query:
            searched = True
            searched_item = Consultation.query.filter( 
                or_(Consultation.name.ilike(f'%{query}%'),
                    Consultation.lastname.ilike(f'%{query}%'))).all()
        else:
            searched = False

        all_logs = Consultation.query.all()
        return render_template('logs.html', searched=searched,searched_item=searched_item,all_logs=all_logs)

    @app.route('/')
    def index():
        
        availability = db.session.query(Availability, User).join(User).filter(Availability.user_id == User.id).all()
        formatted_availability = []
        for availability_instance, user_instance in availability:
            formatted_availability.append({
                'date': availability_instance.date,
                'day_of_week': availability_instance.day_of_week,
                'start_time': availability_instance.start_time,
                'end_time': availability_instance.end_time,
                'username': user_instance.username, 
                'email': user_instance.email, 
            })

        Faqs = FAQS.query.all()     
        return render_template("index.html", Faqs=Faqs, availabilities=formatted_availability)