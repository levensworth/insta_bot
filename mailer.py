import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_notification(subject, body):
    ##############################################
    # You fill out the following variables
    # and let Python do the rest...
    fromaddr = "bpstudio96@gmail.com"
    password = "ca210946"
    toaddr = "ivanandrestaba@gmail.com"  # WARNING: change this
    subject = subject
    body = body
    ##############################################

    print("Sending email from {} to {} ...".format(fromaddr, toaddr))
    # the rest of the code
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, password)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

    print("Email sent!")


if __name__ == '__main__':
    send_notification("te aviso","esta prueba es para vo")
