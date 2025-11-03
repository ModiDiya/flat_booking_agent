from flask import Flask, render_template, request, jsonify
from backend.google_calendar import get_available_slots, create_event
from datetime import datetime, timezone, timedelta, date
import json

app = Flask(__name__)
# Convert datetime to IST string with AM/PM
def format_slot(slot_start, slot_end):
    ist = timezone(timedelta(hours=5, minutes=30))
    return f"{slot_start.astimezone(ist).strftime('%I:%M %p')} - {slot_end.astimezone(ist).strftime('%I:%M %p')}"

# Generate dates for the next 7 days (excluding weekends)
def generate_available_dates():
    today = date.today()
    dates = []
    
    for i in range(7):
        current_date = today + timedelta(days=i)
        # Skip weekends (optional - remove if you want to include weekends)
        if current_date.weekday() < 5:  # 0-4 = Monday to Friday
            dates.append(current_date)
    
    return dates

# Format date for display
def format_date_display(date_obj):
    return date_obj.strftime("%a, %b %d")

# API endpoint to get available dates
@app.route('/api/available_dates')
def api_available_dates():
    dates = generate_available_dates()
    formatted_dates = [{
        'value': date.strftime('%Y-%m-%d'),
        'display': format_date_display(date)
    } for date in dates]
    
    return jsonify(formatted_dates)

# API endpoint to get available slots for a specific date
@app.route('/api/available_slots/<date_str>')
def api_available_slots(date_str):
    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        slots = get_available_slots(selected_date)
        
        if not slots:
            return jsonify({'slots': [], 'message': 'No slots available for this date.'})
        
        formatted_slots = [format_slot(s, e) for s, e in slots]
        return jsonify({'slots': formatted_slots})
        
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

# API endpoint to create a booking
@app.route('/api/create_booking', methods=['POST'])
def api_create_booking():
    try:
        data = request.get_json()
        
        email = data.get('email')
        date_str = data.get('date')
        time_slot = data.get('time')
        description = data.get('description', '')
        recurring = data.get('recurring', False)
        
        # Validate required fields
        if not email or not date_str or not time_slot:
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Convert selected date
        selected_day = datetime.strptime(date_str, "%Y-%m-%d").date()
        
        # Get available slots for validation
        slots = get_available_slots(selected_day)
        if not slots:
            return jsonify({'error': 'No slots available for this date'}), 400
        
        # Find the selected time slot
        slot_index = None
        for i, (start_time, end_time) in enumerate(slots):
            if format_slot(start_time, end_time) == time_slot:
                slot_index = i
                break
        
        if slot_index is None:
            return jsonify({'error': 'Selected time slot is not available'}), 400
        
        start_time, end_time = slots[slot_index]
        
        # Create Google Calendar event
        event_link = create_event(
            summary="Real Estate Consultation",
            start_time=start_time,
            end_time=end_time,
            client_email=email,
            description=description,
            recurring=recurring
        )
        
        return jsonify({
            'success': True,
            'event_link': event_link,
            'email': email,
            'date': selected_day.strftime('%Y-%m-%d'),
            'time_slot': time_slot
        })
        
    except Exception as e:
        return jsonify({'error': f'Booking failed: {str(e)}'}), 500

# Chatbot route
@app.route("/")
def index():
    return render_template("chatbot.html")

# Success page for chatbot bookings
@app.route("/chatbot_success")
def chatbot_success():
    event_link = request.args.get('link', '')
    email = request.args.get('email', '')
    return render_template("chatbot_success.html", link=event_link, email=email)

# Legacy form route (optional - keep if you want both interfaces)
@app.route("/form", methods=["GET", "POST"])
def form_booking():
    if request.method == "POST":
        # Get form data
        email = request.form["email"]
        date_str = request.form["date"]
        slot_index = int(request.form["slot"])
        description = request.form.get("description", "")
        recurring = request.form.get("recurring") == "on"

        # Convert selected date
        selected_day = datetime.strptime(date_str, "%Y-%m-%d").date()

        # Get available slots for the selected date
        slots = get_available_slots(selected_day)
        if not slots:
            return render_template("index.html", slots=[], today=selected_day, message="No slots available for this date.")

        start_time, end_time = slots[slot_index]

        # Create Google Calendar event
        event_link = create_event(
            summary="Real Estate Consultation",
            start_time=start_time,
            end_time=end_time,
            client_email=email,
            description=description,
            recurring=recurring
        )

        return render_template("success.html", link=event_link, email=email)

    # GET request – show booking form
    today = datetime.now().date()
    slots_today = get_available_slots(today)
    slots_formatted = [format_slot(s, e) for s, e in slots_today]

    return render_template("index.html", slots=slots_formatted, today=today, message=None)

if __name__ == "__main__":
    app.run(debug=True)