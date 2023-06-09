import pandas as pd
import math
from datetime import timedelta
import sys

# dohvaćanje podataka iz exelica
df = pd.read_excel('ScenarioReview.xlsx', sheet_name='Chronology')
df2 = pd.read_excel('Trošak.xlsx', sheet_name='Cijene')
df3 = pd.read_excel('Trošak.xlsx', sheet_name='MjesecneCijene')
df4 =pd.read_excel('Trošak.xlsx', sheet_name='UkradeniPodaciCijena')
df5 =pd.read_excel('0dayexploitprices.xlsx', sheet_name="Sheet1")

CIJENASATA=51 # prosječna cijena sata rada etičkog hakera u SAD-u



# pretvaranje podataka u liste
array_of_rows = df.values.tolist()
trosak=df2.values.tolist()
mjesecnitrosak=df3.values.tolist()
cijenepodataka= df4.values.tolist()
exploitiIcijene = df5.values.tolist()

    



ukupnitrosak=0;
ukupnazarada=0;

# Open the file
with open('resursi.txt', 'r') as f:
    # Read all lines in the file
    lines = f.readlines()


elementi = [s.strip().lower() for s in lines] #svi napadačevi resursi (osim servera što CCS računa)


napadresursi=[] 

# dohvaćanje svih parametara akcija i identiciranje koji od njih su napadačevi resursi
for row in array_of_rows:
    
    element=row[6]
    	
    if isinstance(element, str):
        if len(element.split(":")) > 1:
                
            for objekt in element.split(":"):
                	
                if("\n" not in objekt):
                    napadresursi.append(objekt.lower().strip()) 
                else:
                    for o in objekt.split("\n"):
                    	napadresursi.append(o.lower().strip()) 
                    	    
               
                   
                    
                    
prodanipodaci=[] #lista prodanih podataka

    
koristeni=list(set(napadresursi).intersection(elementi)) #lista svih korištenih resursa tijekom napada
print("Koristeni resursi su :")
print(koristeni)

delta=array_of_rows[len(array_of_rows)-1][1]-array_of_rows[0][1]

months = delta.days / 30.4 

months=math.ceil(months) #broj mjeseci zaokruzen na veci broj


#identifikacija je li doslo zarade od blackmaila
for row in array_of_rows:
    
    
    
    if isinstance(row[3],str):
    	if("."in row[3]):
    	    if(row[3].split(".")[0].startswith("Your blackmail") and row[3].split(".")[1].strip().startswith("You have gained")):
       	        
       	        ukupnazarada+=int(row[3].split(".")[1].split(" ")[4]) #dodaj cifru blackmaila u zaradu
    

#identificiranje prodanih podataka
for row in array_of_rows:
    
    
    
    if isinstance(row[2],str):
    	if(row[2]=="SellData" and isinstance(row[3],str)):
    	    if(row[3].split(":")[0].strip()=="Sell Data"):
       	       # print(row[3].split(":")[1])
       	        if("'" in row[3].split(":")[1]):
       	        	prodanipodaci.append(row[3].split(":")[1].split("'")[1].strip().lower())
       	        	
mjesecnilose=0 #mjesečni trošak korištenih resursa
malwaretrosak=0 #trošak malicioznog koda
exploiti=[] # lista koristenih exploita
exploiti0dayCijena=0 #ukupna cijena exploita pod pretpostavkom da su 0 day
exploitiCijena=0 #ukupna cijena exploita pod pretpostavkom da nisu 0 day


#izračun ukupnog troška pod pretpostavkom expoita koji nisu nultog dana
#računanje troška malicioznog koda
#punjenje liste exploita       	        
for element in koristeni:
    for exploit in exploitiIcijene:
    	
        if(exploit[0].strip().lower()==element.strip().lower()):
       	    exploiti.append(exploit) 
    #print("koristenje "+element)
    for cijena in trosak:
        if(element.strip().lower()==cijena[0].strip().lower() and  not isinstance(cijena[2],str)):
           # print(cijena)
            ukupnitrosak+=float(cijena[1])
          
        if(element.strip().lower()==cijena[0].strip().lower() and  isinstance(cijena[2],str)):
            #print(cijena)
            if(float(cijena[1])>malwaretrosak):
                malwaretrosak=float(cijena[1])
            
            
    for mjesecnacijena in mjesecnitrosak:
        if(element.strip().lower()==mjesecnacijena[0].strip().lower()):
           # print("mjesecna cijena je "+str(mjesecnacijena[1]))
            mjesecnilose+=float(mjesecnacijena[1])
            
            
ljudskitrosak=0
ukupnovrijemerada=timedelta(days=0, hours=0, minutes=0);

for row in array_of_rows:
    if(isinstance(row[0],str) and isinstance(row[4],str)):
        if(row[0].strip()=="Action" and row[4].strip()=="Attacker 2"):
            #print(row[3]-row[1])
            ukupnovrijemerada+=row[3]-row[1]
#ukupno vrijeme rada attackera 2
    

satiRada = int(ukupnovrijemerada.total_seconds()) / 3600    
#print("Ukupni sati plaćenog rada "+str(math.ceil(satiRada)))
trosakLjudskeSnage=math.ceil(satiRada) * CIJENASATA #trošak rada

zaradapodaci=0

#print(prodanipodaci)
#print(cijenepodataka)

#izračun prihoda od ukradenih podataka
for podaci in prodanipodaci:
    for cijena in cijenepodataka:
        if(cijena[0].strip().lower().startswith(podaci.strip().lower()) or cijena[0].strip().lower()==podaci.strip().lower()):
            zaradapodaci+=float(cijena[1])
            

#print("mjesecni trosak je "+str(mjesecnilose*months))       	        
#print("malwaretrosak je "+str(malwaretrosak))
#print("zaradapodaci je "+str(zaradapodaci))
ukupnitrosak+=malwaretrosak
ukupnitrosak+=(mjesecnilose*months)
ukupnitrosak+=trosakLjudskeSnage
ukupnazarada+=zaradapodaci
#print("Ukupni trosak je "+str(ukupnitrosak))
#print("Ukupna zarada je "+str(ukupnazarada))
#print(prodanipodaci)
#print("Profit napada iznosi "+str(ukupnazarada-ukupnitrosak))

    
#print(exploiti)
#print(koristeni)
#print(exploitiIcijene)
koristeniE=[] #lista korištenih exploita
for koristen in koristeni:
    #print(koristen)
    for exploitElem in exploitiIcijene:
        
        if koristen.strip().lower()==exploitElem[0].strip().lower():
            koristeniExploit=koristen.strip().lower()
            koristeniE.append(koristeniExploit)   
#print(koristeniE)

#računanje cijene pod pretpostavkom nultog dana i pod suprotnom pretpostavkom
for cijena in trosak:
    if(cijena[0].strip().lower() in koristeniE):
        #print(cijena[0])
        exploitiCijena+=cijena[1]
for cijena in exploitiIcijene:
    if(cijena[0].strip().lower() in koristeniE):
        #print(cijena[0])
        exploiti0dayCijena+=int(cijena[1])
           
#print(exploitiCijena)
#print(exploiti0dayCijena)
ukupnitrosak0=ukupnitrosak-exploitiCijena+exploiti0dayCijena

if len(sys.argv) > 1:
    
    if(sys.argv[1]=="not0"):
        print("Ukupni trošak napada : "+str(ukupnitrosak))
        print("Ukupna zarada: "+str(ukupnazarada))
        print("Ukupna dobit : " +str(ukupnazarada-ukupnitrosak))
    if(sys.argv[1]=="0"):
        print("Ukupni trošak napada : "+str(ukupnitrosak0))
        print("Ukupna zarada: "+str(ukupnazarada))
        print("Ukupna dobit : " +str(ukupnazarada-ukupnitrosak0))
        
    
else:
    print('Upisite zastavicu za pretpostavku cijena exploita!')
