import requests
from bs4 import BeautifulSoup
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# URL of the reservation page
url = "https://www.dpsnnn.com/reserve_g"
name = '단편선'
theme = ''

# Email configuration (use enviromental variable)
email = "your_email@gmail.com"
password = "your_email_password"
to_email = "jake50071227@gmail.com"
smtp_server = "smtp.gmail.com"
smtp_port = 587

# Function to send email notification
def send_email_notification():
    try:
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = to_email
        msg['Subject'] = "Reservation Available!"
        
        body = name + " " + theme + " 예약 가능" + url
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email, password)
        text = msg.as_string()
        server.sendmail(email, to_email, text)
        server.quit()
        
        print("Email notification sent!")
    except Exception as e:
        print(f"Failed to send email notification: {e}")

# Function to check reservation availability
def check_reservation():
    try:
        # Send a request to the website
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the specific element that indicates reservation status
            # This will depend on the actual HTML structure of the page
            # Example:
            reservation_status = soup.find(id='reservation_status').get_text(strip=True)
            
            # Check if reservations are available
            if "Available" in reservation_status:
                print("Reservations are available!")
                return True
            else:
                print("Reservations are not available.")
                return False
        else:
            print(f"Failed to fetch the page. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

# Constantly check for reservation availability
while True:
    available = check_reservation()
    if available:
        send_email_notification()
        # Exit the loop if reservations are available
        break
    # Wait for a specified amount of time before checking again (e.g., 60 seconds)
    time.sleep(60)
