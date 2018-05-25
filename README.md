# Web semantic project

Pasi pentru utilizarea proiectului:
- se instaleaza rdf4j Server (optional si Workbench, pentru debugging) pe masina locala, sub Tomcat8, portul 8080
- se creeaza un repository nou si se face upload la fisierul bands.trig (din folderul static)
- se instaleaza Python (> 3.5 de preferat), se adauga la PATH, se instaleaza utilitarul pip
- in proiectul de fata, se executa comanda `pip install -R requirements.txt` pentru a instala pachetele necesare
- se porneste dev.py (`python dev.py`)
- site-ul este accesibil http://127.0.0.1:5000, paginile sunt HTML/RDFa (cod HTML distilabil)

## Sitemap:
- `/bands` - se afiseaza formatiile 
- `/artists` - se afiseaza artistii, formatiile din care fac parte si cei activi in prezent sunt subliniati cu verde (in functie de relatia `:isMemberOf` sau `:wasMemberOf`)
- `/addband` - permite adaugarea de formatii noi, exista validare doar de UI; 
