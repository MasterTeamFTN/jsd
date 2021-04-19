# Jezici specificni za domen
Projekat iz predmeta Jezici specificni za domen

Tim 4

Clanovi tima:
- Janko Ljubic R2 32/2020
- Boris Sulicenko R2 3/2020
- Nikolina Petrovic R2 29/2020

## Uputstvo za koriscenje

```
$ git clone https://github.com/MasterTeamFTN/jsd.git
$ cd jsd
$ python -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
$ cd sql_generator
$ python main.py -srcSg ./input-file.sg -sql ./out/db.sql -dot ./out/er.dot
```

Parametri za pokretanje ```main.py```:
- ```-srcSg``` - specificira gde se nalazi izvorni .sg fajl
- ```-sql``` - specificira gde da se sacuva generisana .sql skripta 
- ```-dot``` - specificira gde da se sacuva generisani .dot fajl
- ```--dot-only``` - generisanje samo .dot fajla
- ```--sql-only``` - generisanje samo .sql fajla

## Specifikacija

Jezik bi sluzio za generisanje SQL koda za kreiranje seme baze podataka i ER diagrama (dot fajl). Kroz jezik bi bilo pojednostavljeno predstavljanje veza medju entitetima, bilo bi moguce definisati zajednicke atribute i predstaviti veze nasledjivanja.  

Unutar ```entity``` se navode imena elemenata, njihovi tipovi kao i dodatni atributi poput pk, unique i notnull. Moguce je 
navesti i veze ka drugim tabelama u vidu relacija ```1..1```, ```1..*``` i ```*..*```. Nas interpreter bi sam trebao da 
razresi kako ce se ostvariti ove veze, npr. za ```1..1``` ce se koristiti FK kolona, dok za ```*..*``` bi bila kreirana medju tabela.

Jezik bi sadrzao ```fields``` "strukturu" u kojoj bi se navodile iste stvari kao i za entity, ali za nju se ne bi kreirala 
zasebna tabela. Ovo sluzi za definisanje nekih zajednickih elemenate za vise entiteta. Sa kljucnom recju ```copy``` bi se svi ti elementi prekopirali u odredisni entitet.

Postojao bi jos jedan mehanizam prosirivanja - nasledjivanje. Ovo bi bilo realizovano tako sto jedan entitet moze da nasledi
drugi sa kljucnom recju ```extends```. Za razliku od ```copy```, ```extends``` nece kopirati elemente u entitet vec ce
kreirati referencu (FK) na super entitet.

Nas jezik bi podrzavao dve baze podataka ```mysql``` i ```postgresql```. Na pocetku fajla bi se navodilo za koju bazu zelimo da generisemo SQL skriptu.

Jezik bi omogucavao i dupli prolaz kroz fajl cime ne sprecavamo korisnika da kreira entitete u redosledu njihovog koriscenja (entitet se moze koristiti i pre njegovog definisanja). 

Sam interpreter bi imao 3 ugradjenja tipa ```integer```, ```string``` i ```float``` koji se direktno mapiraju na odgovarajuce tipove
dostupnih baza. Ako korisnik zeli da koristi neki drugi tip postoji nacin da to sam uradi koriscenjem ```type``` izraza sa cime kreira "custom" tip.

Primer:  
```
database=mysql

type date="DATETIME"

// Sadrzi zajednicke atribute za vise entiteta
fields Details {
    created_at date
    updated_at date
}

// Entitet fakultet ce pored svojih elemenata imati i elemente iz Details-a
entity Fakultet copy Details {
    // Elementi mogu da imaju svoje atribute koji se navode unutar [ ]
    id integer [pk]
    name string
    city string

    // Elementi koji bi bili predstavljeni preko FK-a ili medju tabelama
    1..* Student student
    1..1 Dekan dekan
}

entity User copy Details {
    id integer [pk]
    ime string
    prezime string
}

// Student nasledjuje klasu User, sto znaci da ce sadrzati sve njegove elemente
// ali sa njima ce biti povezan preko FK-a
entity Student extends User {
    id integer [pk]
    indeks string [unique]
}

entity Dekan extends User {
    id integer [pk]
}
```
