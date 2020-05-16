Dim strPass
Dim strIn

strPass="abcdefghijklmnopqrstuvwxyz"
strIn = InputBox("Enter password:", "password")

DO UNTIL IsEmpty(strIn) Or Mid(strPass,12,2) = strIn
	strIn = InputBox("Wrong password:"+strIn+vbCrlf++vbCrlf+"Try Again:", "password")
LOOP

