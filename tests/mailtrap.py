# import smtplib

# sender = "Private Person <mailtrap@neon-dev.us>"
# receiver = "A Test User <mmm.marchuk@mail.ru>"

# message = f"""\
# Subject: Hi Mailtrap
# To: {receiver}
# From: {sender}

# This is a test e-mail message."""

# with smtplib.SMTP("smtp.mailtrap.io", 587) as server:
#     server.login("d46d4f8f52ae94", "970d0dac663217")
#     server.sendmail(sender, receiver, message)


import smtplib

sender = "Private Person <from@example.com>"
receiver = "A Test User <to@example.com>"

message = f"""\
Subject: Hi Mailtrap
To: {receiver}
From: {sender}

This is a test e-mail message."""

with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
    server.login("d46d4f8f52ae94", "970d0dac663217")
    server.sendmail(sender, receiver, message)