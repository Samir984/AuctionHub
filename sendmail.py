import smtplib

server=smtplib.SMTP("smtp.gmail.com",587)
server.starttls()
server.login("sasuki984@gmail.com", "dqox kjte tmba svjf")
server.sendmail("sasuki984@gmail.com", "samirneupane0011@gmail.com","hello this is mail send from python")
print("message send")
