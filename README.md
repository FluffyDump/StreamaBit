# StreamaBit


## Projekto tikslas 
Sukurti dalijimosi failais platformą, kuri leis naudotojams laikinai patalpinti, saugoti ir dalintis įkeltomis nuotraukomis, dokumentais, muzikos ir kitais failais. Platforma palaikys dviejų tipų įkėlimus: privačius ir viešus. Privatūs įkėlimai leis vartotojams privačiai gauti atsisiuntimo nuorodą ir saugiai dalintis ar perkelti failus į kitus įrenginius. Vieši įkėlimai leis failus įkėlusiam naudotojui dalintis jais su visais svetainės klientais, tačiau siekiant išvengti autorinių teisių pažeidimų, viešai patalpinami failai privalės būti patvirtinti administratoriaus ir po patvirtinimo jie bus pasiekiami naviguojant per failų kategorijas (muzika, nuotraukos ir pan.). Kiekvienas įkeltas failas bus pasiekiamas svetainėje pasirinktą laiko tarpą ar tol, kol bus pasiektas naudotojo nustatytas atsisiuntimų skaičius. Kiekvienas įkėlimas turės nuosavą puslapį, kuriame bus galima peržvelgti individualaus failo atsiliepimus. Siekiant užtikrinti klientų saugumą, visi failai turės saugumo atributą, kuris bus gaunamas tikrinant įkeliamus failus antivirusinės pagalba;
 
## Sistemos paskirtis  
Sukurta platforma skirta laikinai, lengvai, saugiai ir greitai dalintis failais tarp skirtingų įrenginių ar vartotojų. Svetainė skirta palengvinti vartotojų failų perdavimo procesą – svetainė leis dalintis ir atsisiųsti failus privačiai be registracijos, o esant poreikiui pasidalinti failais viešai sistemos bibliotekoje su visais svetainės klientais. 

## Funkciniai reikalavimai
1.	Svetainė palaiko vartotojų registracijas, prisijungimus, slaptažodžio atstatymus bei el. pašto patvirtinimus registracijos metu, naudoja JWT žetonus sesijų palaikymui ir juos atnaujina su kiekvienu naudotojo veiksmu;

2.	Svetainė suteikia galimybę asinchroniškai įkelti failus privačiai arba atvirai, nustatyti failų kategorijas bei failo saugojimo sąlygas (tam tikrą laikotarpį ar atsisiuntimo skaičių) ir peržiūrėti failo saugumo, dydžio informaciją, komentarus bei parsisiųsti joje patalpintus failus;

  ### 3.	Svetainėje sukurtos skirtingos vartotojų rolės su skirtingais galimais veiksmais:
                 
        Svečiai - gali įkelti ir dalintis failais privačiai bei juos atsisiųsti;
  	
        Registruoti nariai - gali atlikti svečių rolės veiksmus, be to patalpinti failus viešai prieinamoje failų saugykloje bei juos redaguoti, komentuoti kitų vartotojų viešai pasidalintus failus, peržiūrėti įkeltų failų statistikas, keisti savo paskyros duomenis;
  	
        Administratoriai - gali atlikti visų anksčiau paminėtų vartotojų veiksmus ir be jų galės patvirtinti arba atmesti viešai įkeltus vartotojų failus, blokuoti vartotojus, šalinti kitų vartotojų įkeltus failus, redaguoti kategorijas;

5.	Viešai pasidalinti failai reikalauja administratorių patvirtinimo; 

6.	Hierarchinė failų saugojimo struktūra, naršant kategorijose bus galima pasiekti tokias hierarchines struktūras kaip: StreamaBit.com/music/music_track1. Tokia struktūra suteiks galimybę peržvelgti muzikos kategorijos turinį, peržiūrėti visus muzikinio failo komentarus bei atsisiųsti failą;

7.	Svetainė palaiko apsaugotus atsisiuntimus slaptažodžiu;

8.	Sistemos naudojama antivirusinė programa patikrina ar įkeltas failas yra saugus ir praneša vartotojui prieš jam atsisiunčiant failą.


## Pasirinktų technologijų aprašymas

**Python** – suteikia lengvumo ir paprastumo kuriant serverio pusės logiką. Leidžia lengvai sukurti asinchronines API sąsajas(„FastAPI“), naudojantis papildomomis bibliotekomis manipuliuoti duomenų bazių įrašais.

**SvelteKit** – vienas iš moderniausių kliento pusės karkasų kuris suteikia svetainėms didelį našumą bei supaprastina programavimą.

**PostgreSQL** – viena iš dažniausiai naudojamų duomenų bazių. Pasižymi atviru kodu ir yra reliacinė duomenų bazė.


