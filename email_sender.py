import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


   
    
 


def approve_email_reporter(receiver, firstname, lastname, sender, date, time, consultant):
        """Send an email report."""
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        username = 'kaizensolution1@gmail.com'
        password = 'zdey mjgf vmhe ynct '

        sender_email = sender
        receiver_email = receiver  # Replace with the recipient's email
        subject = 'Consultation Update'
        body = f'''
                <!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>Email Notification</title>
                            <style>
                                body {{
                                    font-family: Arial, sans-serif;
                                    margin: 20px;
                                    line-height: 1.6;
                                }}
                                p{{
                                font-size:19px;
                                }}
                                .header {{
                                  font-size:35px;
                                    font-weight: bold;
                                }}
                                .footer {{
                                    margin-top: 20px;
                                    font-style: italic;
                                }}
                                .report {{
                                    background-color: #f9f9f9;
                                    border: 1px solid #ccc;
                                    padding: 10px;
                                    margin: 10px 0;
                                }}
                            </style>
                        </head>
                        <body>
                            <h1 class="header">Dear {firstname} {lastname},</h1>

                            <p>I hope this message finds you well.</p>

                            <p>
                               I am pleased to inform you that your consultation appointment has been approved. Below are the details:
                            </p>

                            <p>
                            Date: <i>{date}</i> <br> 
                            Time: <i>{time} </i> <br>
                            Location: Fcpc CCS Dean's office <br>
                            Consultant: {consultant} <br>

                            If you have any questions or need to reschedule, please let us know at your earliest convenience. We look forward to assisting you.</p>

                            

                         

                            <h3 class="footer">Best regards,<br>{consultant}</h3>
                        </body>
                        </html>

                '''

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(username, password)
                server.send_message(msg)
            print("Email sent successfully!")
        except Exception as e:
            print(f"Error: {e}")

   

def rejected_email_reporter(receiver, firstname, lastname, sender, date, time, consultant):
        """Send an email report."""
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        username = 'kaizensolution1@gmail.com'
        password = 'zdey mjgf vmhe ynct '

        sender_email = sender
        receiver_email = receiver  # Replace with the recipient's email
        subject = 'Consultation Update'
        body = f'''
                <!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>Email Notification</title>
                            <style>
                                body {{
                                    font-family: Arial, sans-serif;
                                    margin: 20px;
                                    line-height: 1.6;
                                }}
                                p{{
                                font-size:19px;
                                }}
                                .header {{
                                  font-size:35px;
                                    font-weight: bold;
                                }}
                                .footer {{
                                    margin-top: 20px;
                                    font-style: italic;
                                }}
                                .report {{
                                    background-color: #f9f9f9;
                                    border: 1px solid #ccc;
                                    padding: 10px;
                                    margin: 10px 0;
                                }}
                            </style>
                        </head>
                        <body>
                            <h1 class="header">Dear {firstname} {lastname},</h1>

                            <p>I hope this message finds you well.</p>

                            <p>
                               Thank you for reaching out to us. Unfortunately, we are unable to approve your consultation appointment at this time due to [reason, e.g., scheduling conflicts, unavailability, etc.].

                                We sincerely apologize for any inconvenience this may cause. If you would like to reschedule, please let us know your preferred date and time, and we will do our best to accommodate you.

                                Feel free to contact us if you have any questions or require further assistance.
                            </p>

                            <p>
                

                            If you have any questions or need to reschedule, please let us know at your earliest convenience. We look forward to assisting you.</p>

                            

                         

                            <h3 class="footer">Best regards,<br>{consultant}</h3>
                        </body>
                        </html>

                '''

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(username, password)
                server.send_message(msg)
            print("Email sent successfully!")
        except Exception as e:
            print(f"Error: {e}")




def reconsidered_email_reporter(receiver, firstname, lastname, sender, date, time, consultant):
        """Send an email report."""
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        username = 'kaizensolution1@gmail.com'
        password = 'zdey mjgf vmhe ynct '

        sender_email = sender
        receiver_email = receiver  # Replace with the recipient's email
        subject = 'Consultation Update'
        body = f'''
                <!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>Email Notification</title>
                            <style>
                                body {{
                                    font-family: Arial, sans-serif;
                                    margin: 20px;
                                    line-height: 1.6;
                                }}
                                p{{
                                font-size:19px;
                                }}
                                .header {{
                                  font-size:35px;
                                    font-weight: bold;
                                }}
                                .footer {{
                                    margin-top: 20px;
                                    font-style: italic;
                                }}
                                .report {{
                                    background-color: #f9f9f9;
                                    border: 1px solid #ccc;
                                    padding: 10px;
                                    margin: 10px 0;
                                }}
                            </style>
                        </head>
                        <body>
                            <h1 class="header">Dear {firstname} {lastname},</h1>

                            <p>I hope this message finds you well.</p>

                            <p>
                              We are pleased to inform you that upon further review, your consultation request has been reconsidered and approved. Below are the updated details:
                            </p>

                            <p>
                            Date: <i>{date}</i> <br> 
                            Time: <i>{time} </i> <br>
                            Location: Fcpc CCS Dean's office <br>
                            Consultant: {consultant} <br>

                            If you have any questions or need to reschedule, please let us know at your earliest convenience. We look forward to assisting you.</p>

                            

                         

                            <h3 class="footer">Best regards,<br>{consultant}</h3>
                        </body>
                        </html>

                '''

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(username, password)
                server.send_message(msg)
            print("Email sent successfully!")
        except Exception as e:
            print(f"Error: {e}")
            
def expiredRequest(receiver, firstname, lastname, sender):
        """Send an email report."""
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        username = 'kaizensolution1@gmail.com'
        password = 'zdey mjgf vmhe ynct '

        sender_email = sender
        receiver_email = receiver  # Replace with the recipient's email
        subject = 'Consultation Update'
        body = f'''
                <!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>Email Notification</title>
                            <style>
                                body {{
                                    font-family: Arial, sans-serif;
                                    margin: 20px;
                                    line-height: 1.6;
                                }}
                                p{{
                                font-size:19px;
                                }}
                                .header {{
                                  font-size:35px;
                                    font-weight: bold;
                                }}
                                .footer {{
                                    margin-top: 20px;
                                    font-style: italic;
                                }}
                                .report {{
                                    background-color: #f9f9f9;
                                    border: 1px solid #ccc;
                                    padding: 10px;
                                    margin: 10px 0;
                                }}
                            </style>
                        </head>
                        <body>
                            <h1 class="header">Dear {firstname} {lastname},</h1>

                            <p>I hope this message finds you well.</p>

                            <p>
                              We would like to inform you that, upon further review, your application has been reconsidered. However, we regret to inform you that the application has expired and is no longer eligible for processing.

                            </p>


                            <p>If you have any questions or need to reschedule, please let us know at your earliest convenience. We look forward to assisting you.</p>

                            

                         

                            <h3 class="footer">Best regards,<br>IT Department</h3>
                        </body>
                        </html>

                '''

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(username, password)
                server.send_message(msg)
            print("Email sent successfully!")
        except Exception as e:
            print(f"Error: {e}")