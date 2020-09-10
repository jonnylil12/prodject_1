import smtplib

sender = "testingcodingemail1@gmail.com"
rec = "bobdoe945@gmail.com"
password = "Password1234$"
message = "Ur book is due ih 2 days"

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(sender, password)
print("Login success")
server.sendemail(sender, rec, message)
print("Email has been sent to ", rec)
 print('new')