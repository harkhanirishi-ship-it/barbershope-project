from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# In-memory storage for appointments
appointments = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        # Basic validation
        if not all([request.form['name'], request.form['date'], request.form['time'], request.form['phone']]):
            return render_template('book.html', error="Please fill all fields")
        
        # Check if date is in the future
        appointment_date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        if appointment_date < datetime.now().date():
            return render_template('book.html', error="Please select a future date")
        
        # Create appointment with unique ID
        appointment = {
            'id': str(uuid.uuid4())[:8],
            'name': request.form['name'],
            'date': request.form['date'],
            'time': request.form['time'],
            'phone': request.form['phone'],
            'service': request.form['service'],
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        appointments.append(appointment)
        return redirect(url_for('confirmation', appointment_id=appointment['id']))
    
    return render_template('book.html')

@app.route('/confirmation/<appointment_id>')
def confirmation(appointment_id):
    appointment = next((apt for apt in appointments if apt['id'] == appointment_id), None)
    if not appointment:
        return redirect(url_for('home'))
    return render_template('confirmation.html', appointment=appointment)

@app.route('/appointments')
def appointments_view():
    # Sort appointments by date and time
    sorted_appointments = sorted(appointments, key=lambda x: (x['date'], x['time']))
    return render_template('appointments.html', appointments=sorted_appointments)

@app.route('/cancel/<appointment_id>')
def cancel_appointment(appointment_id):
    global appointments
    appointments = [apt for apt in appointments if apt['id'] != appointment_id]
    return redirect(url_for('appointments_view'))

if __name__ == '__main__':
    app.run(debug=True)  
