from flask import Blueprint, render_template, request, send_from_directory, url_for, flash, current_app
from .forms import UploadForm
from . import photos
import os

views = Blueprint('views', __name__)

@views.route('/uploads/<filename>')
def get_file(filename):
    print('lol')
    return send_from_directory(current_app.config['UPLOADED_PHOTOS_DEST'], filename)

@views.route('/output/<filename>')
def output_file(filename):
    return send_from_directory(os.path.join(os.path.dirname(os.getcwd()), 'Femme', 'Barbershop', 'output'), filename)

@views.route('/', methods=['GET', 'POST'])
def upload_image():
    from website.tasks import process_job
    print('yoooo')
    form = UploadForm()
    file_url = None
    hairstyle_url = None
    processed_file_url = None
    recipient_email = None
    
    if form.validate_on_submit():
        # Save the uploaded images
        user_image_filename = photos.save(form.photo.data, name='face.png')
        target_image_filename = photos.save(form.hairstyle.data, name='hairstyle.png')

        # Create URLs for the uploaded images for preview
        file_url = url_for('views.get_file', filename=user_image_filename)
        hairstyle_url = url_for('views.get_file', filename=target_image_filename)
        
        print('love')
    
        recipient_email = form.recipient_email.data 

        # Run the processing script
        process_job.delay(user_image_filename, target_image_filename, recipient_email)
        
        flash('Images are being processed. You will receive an email once processing is complete.')
    return render_template('index.html', form=form, file_url=file_url, hairstyle_url=hairstyle_url, processed_file_url=processed_file_url)
