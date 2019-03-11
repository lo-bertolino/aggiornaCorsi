import http.client
import smtplib
import string
import os

def mail(mittente, destinatario, materia, news,pswd):
	email = smtplib.SMTP("smtp.gmail.com", 587) # impostare a seconda della propria mail
	email.ehlo() #effettuo l'hello col Server
	email.starttls()
	email.login(mittente, pswd)
	msg = "Subject: nuovo avviso nel corso di " + materia #oggetto
	msg += "\n\n" + news #corpo del messaggio
	for receiver in destinatario:
		email.sendmail(mittente, receiver, msg)
		print(receiver)
	email.quit()


def noaccent (char):
	if char == 'è':
		return "e'"
	elif char == 'é':
		return "e'"
	elif char == 'à':
		return "a'"
	elif char == 'ì':
		return "i'"
	elif char == 'ò':
		return "o'"
	elif char == 'ù':
		return "u'"
	else:
		return char


def newsCreation(page, charPosition): #parsing del codice
	page = page[charPosition: charPosition + 1000]
	charPosition = 0
	news = str()
	for c in page:
		charPosition += 1
		if c == '>':
			break
	page = page[charPosition:]
	# print(page, charPosition)#debug
	i = 0

	while page[i] != '<':
		#chiedo perdono al protettore dei codici per questo costrutto condizionale
		if page[i] == '&':
			if page[i+1] == 'e':
				news += "e'"
			if page[i+1] == 'a':
				news += "a'"
			if page[i+1] == 'o':
				news += "o'"
			if page[i+1] == 'u':
				news += "u''"
			i += 6
		else:
			news += noaccent(page[i])
		i += 1
	print(news)
	return news


def control(news, subject, sender, receiver, pswd, scriptPath): #controllo se la news è stata aggiornata
	NewMessage = False
	try:
		salvato = open(scriptPath + subject + "_avviso", "r") #todo implementare scriptPath
		msgSalvato = salvato.read()
		if msgSalvato != news:
			NewMessage = True
		salvato.close()
	except:
		NewMessage = True
		print("nessun file")

	if NewMessage:
		salvato = open(scriptPath +subject + "_avviso", "w")
		salvato.write(news)
		salvato.close()
		#mail(sender, receiver, subject, news, pswd)
		print("nuovo avviso nel corso di " + subject)
	else:
		print("nessun nuovo avviso :(")


sender = ""
receiver = [""]
pswd = ""
scriptPath=os.path.dirname(os.path.realpath(__file__))
scriptPath=os.path.join(scriptPath,"")
#print("path", scriptPath)#debug

#oop
conn = http.client.HTTPSConnection("softeng.polito.it")
conn.request("GET", "/courses/09CBI/")
r1 = conn.getresponse()
print("connection status:" + r1.reason + "\n")
page = r1.read().decode("UTF-8") #il decode è necessario solo in fase di debug
#print(page) #debug
charPosition = (page.find("<h2 id=\"News\">News</h2>")) + 100 #posizionamento all'inizio della tabella news
news = newsCreation(page, charPosition)
control(news,"programmazione ad oggetti",sender, receiver, pswd,scriptPath)
conn.close()
#fine oop
print("\n")
#databases
conn = http.client.HTTPConnection("dbdmg.polito.it") #attenzione, il sito non supporta https (bello vero)
conn.request("GET", "/wordpress/teaching/basi-di-dati-infcorso1/")
r1 = conn.getresponse()
print("connection status:" + r1.reason)
page = r1.read().decode("UTF-8")
#print(page) #debug
charPosition = (page.find("NEW</strong>"))
news = newsCreation(page, charPosition)
print("\n")
control(news,"basi di dati",sender, receiver,pswd,scriptPath)
conn.close()
#fine databases
