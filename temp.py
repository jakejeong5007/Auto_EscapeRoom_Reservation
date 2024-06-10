# Open --> <div class="booking_list  hide_badge"><a href="/reserve_ss/?idx=47&amp;day=2024-06-14" class="tabled full-width" onclick=""> <div class="title table-cell"><div class="holder"><span class="text">별 / 10:00</span> <span class="count"></span></div></div></a></div>
# Closed --> <div class="booking_list waiting closed disable hide_badge"><a href="/reserve_ss/?idx=46&amp;day=2024-06-14" class="tabled full-width" onclick="return false"> <div class="title table-cell"><div class="holder"><span class="text">별 / 11:30</span> <span class="count"></span></div></div></a></div>
import requests
from bs4 import BeautifulSoup
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# URL of the reservation page
url = "https://www.dpsnnn.com/reserve_g"
name = '단편선'
theme = '그없상'

# Email configuration (use enviromental variable)
email = "your_email@gmail.com"
password = "your_email_password"
to_email = "to_email@gmail.com"

smtp_server = "smtp.gmail.com"
smtp_port = 587

# Function to send email notification
def send_email_notification():
    try:
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = to_email
        msg['Subject'] = "방탈출 예약 가능!"
        
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

            # looks at the text of each <h2> element, converts to lowercase, and checks wether the substring "python" is found anywhere. 
            reservation_status = soup.find_all("h2", string=lambda text: "python" in text.lower()) 

            
            # Check if reservations are available
            if "onclick=return true" in reservation_status:
                print("예약 가능!")
                return True
            else:
                print("예약 불가능.")
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
