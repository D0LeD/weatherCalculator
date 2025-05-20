# weatherAdvisor
☀️ Laika padomdevējs
Laika padomdevējs ir konsoles Python lietotne, kas analizē laika prognozi Rīgai, balstoties uz datiem no vietnes AccuWeather, lai noteiktu labākās dienas pastaigām vai aktivitātēm ārpus telpām.
Kā tas darbojas:
1. Datu iegūšana:
   Tiek izmantota `requests` bibliotēka, lai iegūtu HTML lapu katrai dienai. Ar `BeautifulSoup` palīdzību no koda tiek iegūti: datums, laikapstākļu apraksts, temperatūra un nokrišņu iespējamība.
2. Laikapstākļu novērtējums:
   Lietotājs var iestatīt svarus temperatūrai un nokrišņiem (kopā 100%). Katrai dienai tiek aprēķināts vērtējums (score) pēc formulas:
   score = temperatūra × (temperatūras_svars / 100) - nokrišņi × (nokrišņu_svars / 100) / 20
3. Datu glabāšana un kārtošana:
   Dati tiek glabāti lietotāja implementētā `HashTable`, kur atslēga ir score, bet vērtība — `Day` objekts ar laika informāciju.
4. Interfeiss:
   Lietotājs var:
   - izvēlēties dienu skaitu analīzei (1-61),
   - norādīt, cik labākās dienas rādīt,
   - mainīt svara koeficientus.
5. Rezultāts:
   Programma parāda formatētu tabulu ar labākajām dienām, iekļaujot datumu, temperatūru, nokrišņus un aprakstu.
Atkarības:
- `requests`
- `beautifulsoup4`
