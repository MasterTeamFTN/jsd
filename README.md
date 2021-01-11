# Jezici specificni za domen
Projekat iz predmeta Jezici specificni za domen

Tim 4

Clanovi tima:
- Janko Ljubić R2 32/2020
- Boris Šuličenko R2 3/2020
- Nikolina Petrović R2 29/2020

## Specifikacija

Jezik bi sluzio za generisanje SQL koda za kreiranje seme baze podataka. Kroz jezik bi bilo pojednostavljeno predstavljanje
veza medju entitetima, bilo bi moguce definisati zajednicke atribute i predstaviti veze nasledjivanja.  

Unutar ```entity``` se navode imena elemenata, njihovi tipovi kao i dodatni atributi poput unique, notnull, ... Moguce je 
navesti i veze ka drugim tabelama u vidu relacija ```1..1```, ```1..*``` i ```*..*```. Nas interpreter bi sam trebao da 
razresi kako ce se ostvariti ove veze, npr. za ```1..1``` ce se koristiti FK kolona, dok za ```*..*``` bi bila kreirana medju tabela.

Jezik bi sadrzao ```fields``` "strukturu" u kojoj bi se navodile iste stvari kao i za entity, ali za nju se ne bi kreirala 
zasebna tabela. Ovo sluzi za definisanje nekih zajednickih elemenate za vise entiteta. Sa kljucnom recju ```copy``` bi se svi ti elementi prekopirali u odredisni entitet.

Postojao bi jos jedan mehanizam prosirivanja - nasledjivanje. Ovo bi bilo realizovano tako sto jedan entitet moze da nasledi
drugi sa kljucnom recju ```extends```. Za razliku od ```copy```, ```extends``` nece kopirati elemente u entitet vec ce
kreirati referencu (FK) na super entitet.

Primer:  
```
database=mysql

// Sadrzi zajednicke atribute za vise entiteta
fields Details {
    created_at datetime
    updated_at datetime
}

// Entitet fakultet ce pored svojih elemenata imati i elemente iz Details-a
entity Fakultet copy Details {
    // Elementi mogu da imaju svoje atribute koji se navode unutar [ ]
    id integer [pk, increment]
    name varchar
    city varchar

    // Elementi koji bi bili predstavljeni preko FK-a ili medju tabelama
    1..* Student
    1..1 Dekan
}

entity User copy Details {
    id integer [pk]
    ime varchar
    prezime varchar
}

// Student nasledjuje klasu User, sto znaci da ce sadrzati sve njegove elemente
// ali sa njima ce biti povezan preko FK-a
entity Student extends User {
    id integer [pk]
    indeks varchar [unique]
}

entity Dekan extends User {
    id integer [pk]
}
```
