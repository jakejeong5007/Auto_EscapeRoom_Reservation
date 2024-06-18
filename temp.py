import requests
from bs4 import BeautifulSoup
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
from datetime import datetime
import os

# URL of the reservation page
url = "https://www.dpsnnn.com/reserve_g" 
name = '단편선' # Escape room name
theme = '그없상' # Theme name

# Email configuration 
email = "jake50071227@gmail.com"
password = os.environ['GOOGLE_APP_KEY']# use enviromental variable when uploading to github
to_email = "jake50071227@gmail.com"

smtp_server = "smtp.gmail.com"
smtp_port = 587

# Function to send email notification
def send_email_notification(rev_time):
    try:
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = to_email
        msg['Subject'] = "방탈출 예약 가능!"
        
        body = name + " " + theme + " " + rev_time.strftime('%H:%M') + " 예약 가능" + url
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
        response = requests.get(url, headers={'User-agent':'Mozila/5.0'})
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the specific element that indicates reservation status
            # This will depend on the actual HTML structure of the page
            # Example:
            # reservation_status = soup.find(id='reservation_status').get_text(strip=True)

            # looks at the text of each <h2> element, converts to lowercase, and checks wether the substring "python" is found anywhere. 
            # reservation_status = soup.find_all("div", string=lambda text: "booking_list  hide_badge" in text.lower()) 
            pattern = re.compile(r'^\s*booking_list\s+hide_badge\s*$')
            elements = [div for div in soup.find_all('div') if 'class' in div.attrs and pattern.match(' '.join(div['class']))]
            
            # Check if reservations are available
            if elements:
                print("Found divs with 'booking_list' and 'hide_badge' classes:")
                for element in elements:
                    time_text = element.find('span', class_='text').text.strip()
                    # Extract the time part (e.g., "11:30")
                    time_match = re.search(r'(\d{2}:\d{2})', time_text)
                    if time_match:
                        time_str = time_match.group(1)
                        # Convert the time string to a datetime object
                        time_obj = datetime.strptime(time_str, '%H:%M').time()
                        
                        # Check if the time is after 18:00 (Able to select time)
                        if time_obj >= datetime.strptime('10:00', '%H:%M').time():
                            return True, time_obj # Available Time
                        else:
                            return False
            else:
                return False
                
        else:
            print(f"Failed to fetch the page. Status code: {response.status_code}")
            return False
    except Exception as e:
        
        print(f"An error occurred: {e}")
        return False

# Constantly check for reservation availability
while True: 
    available, rev_time = check_reservation()
    if available:
        print("예약가능")
        send_email_notification(rev_time)
        # Exit the loop if reservations are available
        break
    # Wait for a specified amount of time before checking again (e.g., 60 seconds)
    print("예약 불가능")
    time.sleep(60)

