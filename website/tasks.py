from celery import Celery
from .my_celery import make_celery
import subprocess
import os
from website.email import send_email

celery = make_celery()

@celery.task
def process_job(face_filename, hairstyle_filename, recipient_email):
    print('Processing started...')
    try:
        # Path to the script that processes the images
        script_path = os.path.join(os.getcwd(), 'Barbershop', 'run_process.sh')
        
        # Run the processing script
        subprocess.run([script_path, face_filename, hairstyle_filename], check=True)
        print('Processing completed successfully.')
        
        # Path to the processed image
        face_filename_base = os.path.splitext(face_filename)[0]
        hairstyle_filename_base = os.path.splitext(hairstyle_filename)[0]
        processed_filename = f"{face_filename_base}_{hairstyle_filename_base}_{hairstyle_filename_base}_realistic.png"
        processed_file_path = os.path.join(os.path.dirname(os.getcwd()), 'Femme', 'Barbershop', 'output', processed_filename)
        
        # Send the email with the processed image as an attachment
        send_email(
            from_addr='sanmiareoye1@gmail.com',
            to_addr=recipient_email,
            subject='Your Processed Image is Ready!',
            content='Your processed image is attached.',
            attachment_path=processed_file_path
        )
        print('Email sent successfully.')
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running the processing script: {e}")
