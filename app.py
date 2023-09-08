from flask import Flask, request, redirect, url_for, flash, render_template
import os
import pandas as pd
# app.py
from data_visualization import create_tiered_progress_bar, create_progress_bar, create_poster_pie_chart, generate_plot
from data_processing import clean_data, process_csv, remove_duplicates, handle_missing_values, count_service_lines_by_contact_id
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
allowed_extensions = {'csv'}

app = Flask(__name__, static_folder='static')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def process_and_save_file(file, upload_folder):
    try:
        df = pd.read_csv(file)
        print("About to clean data...")
        df = clean_data(df)
        print("Data cleaned.")
        
        generate_plot(df)
        create_poster_pie_chart(df)
        
        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_folder, filename)
        df.to_csv(file_path, index=False)
        
        print(f"File saved at {file_path}.")
        return filename
    except Exception as e:
        print(f"Error while processing file: {e}")
        raise

    
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        
        # Check if the folder exists; if not, create it
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
            
        # Print the current working directory to debug
        print(f"Current Working Directory: {os.getcwd()}")
        
        if file and allowed_file(file.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            
            # Save the file
            file.save(filename)
            
            flash('File successfully uploaded')
            
            # Redirect to dashboard
            return redirect(url_for('dashboard', filename=secure_filename(file.filename)))   
         
    return render_template('index.html')



def generate_dashboard_data(filename, full_path):
    df = process_csv(full_path)  
    contact_id_counts = count_service_lines_by_contact_id(df)
    

    # Create the tiered progress bar
    total_service_lines = sum(contact_id_counts.values())
    create_tiered_progress_bar(total_service_lines, 350000, 400000, 450000)

    return {
        'target_bar': 'static/tiered_progress_bar.png',
        'other_plot': 'static/plot.png',
        'poster_pie_chart': 'static/poster_pie_chart.png',
        'contact_id_counts': contact_id_counts  # <-- Pass the entire dictionary
    }

@app.route('/dashboard')
def dashboard():
    
    filename = request.args.get('filename')  # Get the filename from the URL parameters
    full_path = os.path.join(UPLOAD_FOLDER, filename)  # Using UPLOAD_FOLDER here
    
    print(f"Full path: {full_path}")  # Debugging line

    if not filename or not os.path.exists(full_path):
        flash('No file uploaded. Redirecting to upload page.')
        return redirect(url_for('upload_file'))


    if filename and os.path.exists(full_path):  # Updated check
        df = process_csv(full_path)  # Updated read
        contact_id_counts = count_service_lines_by_contact_id(df)
        
        service_lines_by_kevin = contact_id_counts.get('Kevin Moye', 0)
        
    else:
        return "CSV file not found or not specified", 404
   
   #Calls generate_dashboard_data and runs the needed arguments
    dashboard_data = generate_dashboard_data(filename, full_path)
    return render_template('dashboard.html', **dashboard_data)



app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'csv'}
app.secret_key = "supersecretkey"


if __name__ == '__main__':
        app.run(debug=True)
