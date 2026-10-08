// Kubi Kids School — Slovné druhy (10 slovných druhov)
// 1 = Podstatné mená (substantíva)
// 2 = Prídavné mená (adjektíva)
// 3 = Zámená (pronominá)
// 4 = Číslovky (numeralia)
// 5 = Slovesá (verbá)
// 6 = Príslovky (adverbiá)
// 7 = Predložky (prepozície)
// 8 = Spojky (konjunkcie)
// 9 = Častice (partikuly)
// 10 = Citoslovcia (interjekcie)

const sentences = [

/* =========================================================================
   ÚROVEŇ 1 (1–12): Krátke jednoduché vety
   ========================================================================= */
[
  { text: "Malý", type: "pridavne_meno" },
  { text: "pes", type: "podstatne_meno" },
  { text: "veselo", type: "prislovka" },
  { text: "beží.", type: "sloveso" }
],
[
  { text: "Červené", type: "pridavne_meno" },
  { text: "jablko", type: "podstatne_meno" },
  { text: "spadlo", type: "sloveso" },
  { text: "do", type: "predlozka" },
  { text: "trávy.", type: "podstatne_meno" }
],
[
  { text: "Naša", type: "zameno" },
  { text: "babička", type: "podstatne_meno" },
  { text: "pečie", type: "sloveso" },
  { text: "sladký", type: "pridavne_meno" },
  { text: "koláč.", type: "podstatne_meno" }
],
[
  { text: "Tri", type: "cislovka" },
  { text: "usilovné", type: "pridavne_meno" },
  { text: "včielky", type: "podstatne_meno" },
  { text: "bzučia.", type: "sloveso" }
],
[
  { text: "Aha,", type: "citoslovce" },
  { text: "tam", type: "prislovka" },
  { text: "letí", type: "sloveso" },
  { text: "krásny", type: "pridavne_meno" },
  { text: "motýľ!", type: "podstatne_meno" }
],
[
  { text: "Áno,", type: "castica" },
  { text: "ja", type: "zameno" },
  { text: "mám", type: "sloveso" },
  { text: "novú", type: "pridavne_meno" },
  { text: "knihu.", type: "podstatne_meno" }
],
[
  { text: "Mačka", type: "podstatne_meno" },
  { text: "a", type: "spojka" },
  { text: "pes", type: "podstatne_meno" },
  { text: "oddychujú.", type: "sloveso" }
],
[
  { text: "Hľa,", type: "citoslovce" },
  { text: "vysoko", type: "prislovka" },
  { text: "žiari", type: "sloveso" },
  { text: "zlaté", type: "pridavne_meno" },
  { text: "slnko.", type: "podstatne_meno" }
],
[
  { text: "Iba", type: "castica" },
  { text: "dvaja", type: "cislovka" },
  { text: "chlapci", type: "podstatne_meno" },
  { text: "prišli", type: "sloveso" },
  { text: "včas.", type: "prislovka" }
],
[
  { text: "Fuj,", type: "citoslovce" },
  { text: "táto", type: "zameno" },
  { text: "voda", type: "podstatne_meno" },
  { text: "je", type: "sloveso" },
  { text: "studená!", type: "pridavne_meno" }
],
[
  { text: "Kto", type: "zameno" },
  { text: "videl", type: "sloveso" },
  { text: "tohto", type: "zameno" },
  { text: "bystrého", type: "pridavne_meno" },
  { text: "vtáka?", type: "podstatne_meno" }
],
[
  { text: "Snáď", type: "castica" },
  { text: "dnes", type: "prislovka" },
  { text: "bude", type: "sloveso" },
  { text: "príjemné", type: "pridavne_meno" },
  { text: "počasie.", type: "podstatne_meno" }
],

/* =========================================================================
   ÚROVEŇ 2 (13–26): Vety s predložkami, zámenami a číslovkami
   ========================================================================= */
[
  { text: "Môj", type: "zameno" },
  { text: "starší", type: "pridavne_meno" },
  { text: "brat", type: "podstatne_meno" },
  { text: "má", type: "sloveso" },
  { text: "štyri", type: "cislovka" },
  { text: "zaujímavé", type: "pridavne_meno" },
  { text: "knihy.", type: "podstatne_meno" }
],
[
  { text: "Bác,", type: "citoslovce" },
  { text: "ťažká", type: "pridavne_meno" },
  { text: "lopta", type: "podstatne_meno" },
  { text: "spadla", type: "sloveso" },
  { text: "priamo", type: "prislovka" },
  { text: "na", type: "predlozka" },
  { text: "trávnik!", type: "podstatne_meno" }
],
[
  { text: "Pst,", type: "citoslovce" },
  { text: "malé", type: "pridavne_meno" },
  { text: "dieťa", type: "podstatne_meno" },
  { text: "pokojne", type: "prislovka" },
  { text: "spí", type: "sloveso" },
  { text: "v", type: "predlozka" },
  { text: "izbe.", type: "podstatne_meno" }
],
[
  { text: "Včera", type: "prislovka" },
  { text: "sme", type: "sloveso" },
  { text: "videli", type: "sloveso" },
  { text: "pätoro", type: "cislovka" },
  { text: "malých", type: "pridavne_meno" },
  { text: "šteniatok.", type: "podstatne_meno" }
],
[
  { text: "Nech", type: "castica" },
  { text: "každý", type: "zameno" },
  { text: "žiak", type: "podstatne_meno" },
  { text: "napíše", type: "sloveso" },
  { text: "svoje", type: "zameno" },
  { text: "meno.", type: "podstatne_meno" }
],
[
  { text: "Chlapec", type: "podstatne_meno" },
  { text: "rýchlo", type: "prislovka" },
  { text: "bežal", type: "sloveso" },
  { text: "okolo", type: "predlozka" },
  { text: "veľkého", type: "pridavne_meno" },
  { text: "ihriska.", type: "podstatne_meno" }
],
[
  { text: "Prvý", type: "cislovka" },
  { text: "jazdec", type: "podstatne_meno" },
  { text: "dorazil", type: "sloveso" },
  { text: "do", type: "predlozka" },
  { text: "cieľa", type: "podstatne_meno" },
  { text: "veľmi", type: "prislovka" },
  { text: "skoro.", type: "prislovka" }
],
[
  { text: "Vraj", type: "castica" },
  { text: "zajtra", type: "prislovka" },
  { text: "napadne", type: "sloveso" },
  { text: "čerstvý", type: "pridavne_meno" },
  { text: "biely", type: "pridavne_meno" },
  { text: "sneh.", type: "podstatne_meno" }
],
[
  { text: "Oni", type: "zameno" },
  { text: "prišli", type: "sloveso" },
  { text: "k", type: "predlozka" },
  { text: "nám", type: "zameno" },
  { text: "na", type: "predlozka" },
  { text: "letné", type: "pridavne_meno" },
  { text: "prázdniny.", type: "podstatne_meno" }
],
[
  { text: "Ach,", type: "citoslovce" },
  { text: "tento", type: "zameno" },
  { text: "starý", type: "pridavne_meno" },
  { text: "strom", type: "podstatne_meno" },
  { text: "má", type: "sloveso" },
  { text: "krásne", type: "pridavne_meno" },
  { text: "kvety!", type: "podstatne_meno" }
],
[
  { text: "Mama", type: "podstatne_meno" },
  { text: "položila", type: "sloveso" },
  { text: "tanier", type: "podstatne_meno" },
  { text: "na", type: "predlozka" },
  { text: "drevený", type: "pridavne_meno" },
  { text: "stôl.", type: "podstatne_meno" }
],
[
  { text: "Asi", type: "castica" },
  { text: "sedem", type: "cislovka" },
  { text: "vtákov", type: "podstatne_meno" },
  { text: "sedí", type: "sloveso" },
  { text: "na", type: "predlozka" },
  { text: "tenkom", type: "pridavne_meno" },
  { text: "konári.", type: "podstatne_meno" }
],
[
  { text: "My", type: "zameno" },
  { text: "usilovne", type: "prislovka" },
  { text: "kreslíme", type: "sloveso" },
  { text: "farebné", type: "pridavne_meno" },
  { text: "obrázky.", type: "podstatne_meno" }
],
[
  { text: "Opatrne", type: "prislovka" },
  { text: "prejdi", type: "sloveso" },
  { text: "cez", type: "predlozka" },
  { text: "túto", type: "zameno" },
  { text: "širokú", type: "pridavne_meno" },
  { text: "cestu.", type: "podstatne_meno" }
],

/* =========================================================================
   ÚROVEŇ 3 (27–42): Spojky, častice, číslovky a rozvité vety
   ========================================================================= */
[
  { text: "Chlapec", type: "podstatne_meno" },
  { text: "číta,", type: "sloveso" },
  { text: "lebo", type: "spojka" },
  { text: "chce", type: "sloveso" },
  { text: "všetko", type: "zameno" },
  { text: "dobre", type: "prislovka" },
  { text: "vedieť.", type: "sloveso" }
],
[
  { text: "Slnko", type: "podstatne_meno" },
  { text: "hreje", type: "sloveso" },
  { text: "a", type: "spojka" },
  { text: "v", type: "predlozka" },
  { text: "lese", type: "podstatne_meno" },
  { text: "pekne", type: "prislovka" },
  { text: "spievajú", type: "sloveso" },
  { text: "vtáčiky.", type: "podstatne_meno" }
],
[
  { text: "Bodaj", type: "castica" },
  { text: "by", type: "sloveso" },
  { text: "dnes", type: "prislovka" },
  { text: "nezačalo", type: "sloveso" },
  { text: "silno", type: "prislovka" },
  { text: "pršať!", type: "sloveso" }
],
[
  { text: "Tresk,", type: "citoslovce" },
  { text: "dvere", type: "podstatne_meno" },
  { text: "sa", type: "zameno" },
  { text: "zrazu", type: "prislovka" },
  { text: "zabuchli", type: "sloveso" },
  { text: "od", type: "predlozka" },
  { text: "silného", type: "pridavne_meno" },
  { text: "vetra.", type: "podstatne_meno" }
],
[
  { text: "Desať", type: "cislovka" },
  { text: "šikovných", type: "pridavne_meno" },
  { text: "žiakov", type: "podstatne_meno" },
  { text: "vyriešilo", type: "sloveso" },
  { text: "túto", type: "zameno" },
  { text: "ťažkú", type: "pridavne_meno" },
  { text: "úlohu.", type: "podstatne_meno" }
],
[
  { text: "Hoci", type: "spojka" },
  { text: "husto", type: "prislovka" },
  { text: "snežilo,", type: "sloveso" },
  { text: "išli", type: "sloveso" },
  { text: "sme", type: "sloveso" },
  { text: "do", type: "predlozka" },
  { text: "veľkej", type: "pridavne_meno" },
  { text: "školy.", type: "podstatne_meno" }
],
[
  { text: "Hav-hav,", type: "citoslovce" },
  { text: "hlučne", type: "prislovka" },
  { text: "šteká", type: "sloveso" },
  { text: "náš", type: "zameno" },
  { text: "čierny", type: "pridavne_meno" },
  { text: "pes", type: "podstatne_meno" },
  { text: "pri", type: "predlozka" },
  { text: "bráne.", type: "podstatne_meno" }
],
[
  { text: "Aspoň", type: "castica" },
  { text: "jeden", type: "cislovka" },
  { text: "človek", type: "podstatne_meno" },
  { text: "vždy", type: "prislovka" },
  { text: "ochotne", type: "prislovka" },
  { text: "pomôže.", type: "sloveso" }
],
[
  { text: "Pozorne", type: "prislovka" },
  { text: "počúvaj,", type: "sloveso" },
  { text: "aby", type: "spojka" },
  { text: "si", type: "zameno" },
  { text: "neurobil", type: "sloveso" },
  { text: "zbytočnú", type: "pridavne_meno" },
  { text: "chybu.", type: "podstatne_meno" }
],
[
  { text: "Kiež", type: "castica" },
  { text: "by", type: "sloveso" },
  { text: "sme", type: "sloveso" },
  { text: "zajtra", type: "prislovka" },
  { text: "dostali", type: "sloveso" },
  { text: "samé", type: "zameno" },
  { text: "jednotky!", type: "podstatne_meno" }
],
[
  { text: "On", type: "zameno" },
  { text: "pracoval", type: "sloveso" },
  { text: "pomaly,", type: "prislovka" },
  { text: "ale", type: "spojka" },
  { text: "výsledok", type: "podstatne_meno" },
  { text: "bol", type: "sloveso" },
  { text: "veľmi", type: "prislovka" },
  { text: "pekný.", type: "pridavne_meno" }
],
[
  { text: "Ej,", type: "citoslovce" },
  { text: "to", type: "zameno" },
  { text: "je", type: "sloveso" },
  { text: "veru", type: "castica" },
  { text: "mimoriadne", type: "prislovka" },
  { text: "chutné", type: "pridavne_meno" },
  { text: "jedlo!", type: "podstatne_meno" }
],
[
  { text: "Prišli", type: "sloveso" },
  { text: "traja", type: "cislovka" },
  { text: "kamaráti", type: "podstatne_meno" },
  { text: "a", type: "spojka" },
  { text: "priniesli", type: "sloveso" },
  { text: "nám", type: "zameno" },
  { text: "darček.", type: "podstatne_meno" }
],
[
  { text: "Len", type: "castica" },
  { text: "pokojne", type: "prislovka" },
  { text: "seď", type: "sloveso" },
  { text: "na", type: "predlozka" },
  { text: "svojej", type: "zameno" },
  { text: "stoličke.", type: "podstatne_meno" }
],
[
  { text: "Bum,", type: "citoslovce" },
  { text: "ťažký", type: "pridavne_meno" },
  { text: "kufor", type: "podstatne_meno" },
  { text: "dopadol", type: "sloveso" },
  { text: "na", type: "predlozka" },
  { text: "kamennú", type: "pridavne_meno" },
  { text: "dlažbu.", type: "podstatne_meno" }
],
[
  { text: "Keď", type: "spojka" },
  { text: "odbila", type: "sloveso" },
  { text: "dvanásta", type: "cislovka" },
  { text: "hodina,", type: "podstatne_meno" },
  { text: "všetci", type: "zameno" },
  { text: "odišli", type: "sloveso" },
  { text: "domov.", type: "prislovka" }
],

/* =========================================================================
   ÚROVEŇ 4 (43–58): Pestré vety s viacerými druhmi
   ========================================================================= */
[
  { text: "Naozaj", type: "castica" },
  { text: "máš", type: "sloveso" },
  { text: "v", type: "predlozka" },
  { text: "taške", type: "podstatne_meno" },
  { text: "až", type: "castica" },
  { text: "päť", type: "cislovka" },
  { text: "hrubých", type: "pridavne_meno" },
  { text: "zošitov?", type: "podstatne_meno" }
],
[
  { text: "Jaj,",
    type: "citoslovce" },
  { text: "veľmi", type: "prislovka" },
  { text: "ma", type: "zameno" },
  { text: "bolí", type: "sloveso" },
  { text: "pravé", type: "pridavne_meno" },
  { text: "koleno!", type: "podstatne_meno" }
],
[
  { text: "Učiteľka", type: "podstatne_meno" },
  { text: "trpezlivo", type: "prislovka" },
  { text: "vysvetľuje", type: "sloveso" },
  { text: "učivo,", type: "podstatne_meno" },
  { text: "zatiaľ", type: "prislovka" },
  { text: "čo", type: "spojka" },
  { text: "žiaci", type: "podstatne_meno" },
  { text: "píšu.", type: "sloveso" }
],
[
  { text: "Vari", type: "castica" },
  { text: "si", type: "sloveso" },
  { text: "už", type: "prislovka" },
  { text: "zabudol", type: "sloveso" },
  { text: "na", type: "predlozka" },
  { text: "náš", type: "zameno" },
  { text: "dohodnutý", type: "pridavne_meno" },
  { text: "výlet?", type: "podstatne_meno" }
],
[
  { text: "Chi-chi,", type: "citoslovce" },
  { text: "malá", type: "pridavne_meno" },
  { text: "sestra", type: "podstatne_meno" },
  { text: "sa", type: "zameno" },
  { text: "srdečne", type: "prislovka" },
  { text: "smeje", type: "sloveso" },
  { text: "vtipnej", type: "pridavne_meno" },
  { text: "rozprávke.", type: "podstatne_meno" }
],
[
  { text: "V", type: "predlozka" },
  { text: "záhrade", type: "podstatne_meno" },
  { text: "kvitnú", type: "sloveso" },
  { text: "žlté", type: "pridavne_meno" },
  { text: "narcisy", type: "podstatne_meno" },
  { text: "i", type: "spojka" },
  { text: "červené", type: "pridavne_meno" },
  { text: "tulipány.", type: "podstatne_meno" }
],
[
  { text: "Bŕŕ,", type: "citoslovce" },
  { text: "vonku", type: "prislovka" },
  { text: "fúka", type: "sloveso" },
  { text: "ľadový", type: "pridavne_meno" },
  { text: "severný", type: "pridavne_meno" },
  { text: "vietor!", type: "podstatne_meno" }
],
[
  { text: "Každé", type: "zameno" },
  { text: "ráno", type: "podstatne_meno" },
  { text: "beháme", type: "sloveso" },
  { text: "aspoň", type: "castica" },
  { text: "dva", type: "cislovka" },
  { text: "veľké", type: "pridavne_meno" },
  { text: "okruhy.", type: "podstatne_meno" }
],
[
  { text: "Dokonca", type: "castica" },
  { text: "aj", type: "spojka" },
  { text: "starý", type: "pridavne_meno" },
  { text: "pes", type: "podstatne_meno" },
  { text: "radostne", type: "prislovka" },
  { text: "vyskakoval", type: "sloveso" },
  { text: "od", type: "predlozka" },
  { text: "šťastia.", type: "podstatne_meno" }
],
[
  { text: "Klop-klop,", type: "citoslovce" },
  { text: "niekto", type: "zameno" },
  { text: "zrazu", type: "prislovka" },
  { text: "zaklopal", type: "sloveso" },
  { text: "na", type: "predlozka" },
  { text: "masívne", type: "pridavne_meno" },
  { text: "dvere.", type: "podstatne_meno" }
],
[
  { text: "Mama", type: "podstatne_meno" },
  { text: "kúpila", type: "sloveso" },
  { text: "stogramové", type: "pridavne_meno" },
  { text: "maslo", type: "podstatne_meno" },
  { text: "a", type: "spojka" },
  { text: "desať", type: "cislovka" },
  { text: "čerstvých", type: "pridavne_meno" },
  { text: "rožkov.", type: "podstatne_meno" }
],
[
  { text: "Veru,", type: "castica" },
  { text: "my", type: "zameno" },
  { text: "sme", type: "sloveso" },
  { text: "vyhrali", type: "sloveso" },
  { text: "tento", type: "zameno" },
  { text: "dôležitý", type: "pridavne_meno" },
  { text: "zápas.", type: "podstatne_meno" }
],
[
  { text: "Kráčali", type: "sloveso" },
  { text: "pomaly,", type: "prislovka" },
  { text: "pretože", type: "spojka" },
  { text: "cesta", type: "podstatne_meno" },
  { text: "bola", type: "sloveso" },
  { text: "zľadovatená.", type: "pridavne_meno" }
],
[
  { text: "Hej,", type: "citoslovce" },
  { text: "podaj", type: "sloveso" },
  { text: "mi", type: "zameno" },
  { text: "rýchlo", type: "prislovka" },
  { text: "tú", type: "zameno" },
  { text: "modrú", type: "pridavne_meno" },
  { text: "ceruzku!", type: "podstatne_meno" }
],
[
  { text: "Určite", type: "castica" },
  { text: "dnes", type: "prislovka" },
  { text: "stretneme", type: "sloveso" },
  { text: "mnoho", type: "cislovka" },
  { text: "milých", type: "pridavne_meno" },
  { text: "priateľov.", type: "podstatne_meno" }
],
[
  { text: "Prvý", type: "cislovka" },
  { text: "a", type: "spojka" },
  { text: "druhý", type: "cislovka" },
  { text: "pretekár", type: "podstatne_meno" },
  { text: "bežali", type: "sloveso" },
  { text: "vedľa", type: "predlozka" },
  { text: "seba.", type: "zameno" }
],

/* =========================================================================
   ÚROVEŇ 5 (59–70): Komplexnejšie vety s časticami, citoslovcami a číslovkami
   ========================================================================= */
[
  { text: "Hľa,", type: "citoslovce" },
  { text: "z", type: "predlozka" },
  { text: "hustého", type: "pridavne_meno" },
  { text: "lesa", type: "podstatne_meno" },
  { text: "pomaly", type: "prislovka" },
  { text: "vychádza", type: "sloveso" },
  { text: "veľký", type: "pridavne_meno" },
  { text: "hnedý", type: "pridavne_meno" },
  { text: "jeleň.", type: "podstatne_meno" }
],
[
  { text: "Mňau,", type: "citoslovce" },
  { text: "žalostne", type: "prislovka" },
  { text: "zamňaukalo", type: "sloveso" },
  { text: "malé", type: "pridavne_meno" },
  { text: "mačiatko", type: "podstatne_meno" },
  { text: "pod", type: "predlozka" },
  { text: "naším", type: "zameno" },
  { text: "balkónom.", type: "podstatne_meno" }
],
[
  { text: "Iba", type: "castica" },
  { text: "traja", type: "cislovka" },
  { text: "odvážni", type: "pridavne_meno" },
  { text: "chlapci", type: "podstatne_meno" },
  { text: "vyliezli", type: "sloveso" },
  { text: "na", type: "predlozka" },
  { text: "vysokú", type: "pridavne_meno" },
  { text: "skalu.", type: "podstatne_meno" }
],
[
  { text: "Beda,", type: "citoslovce" },
  { text: "stratili", type: "sloveso" },
  { text: "sme", type: "sloveso" },
  { text: "kľúč", type: "podstatne_meno" },
  { text: "od", type: "predlozka" },
  { text: "nášho", type: "zameno" },
  { text: "nového", type: "pridavne_meno" },
  { text: "bytu!", type: "podstatne_meno" }
],
[
  { text: "Slniečko", type: "podstatne_meno" },
  { text: "pekne", type: "prislovka" },
  { text: "svietilo,", type: "sloveso" },
  { text: "preto", type: "spojka" },
  { text: "deti", type: "podstatne_meno" },
  { text: "veselo", type: "prislovka" },
  { text: "behali", type: "sloveso" },
  { text: "po", type: "predlozka" },
  { text: "dvore.", type: "podstatne_meno" }
],
[
  { text: "Nech", type: "castica" },
  { text: "sa", type: "zameno" },
  { text: "vám", type: "zameno" },
  { text: "všetkým", type: "zameno" },
  { text: "dnes", type: "prislovka" },
  { text: "mimoriadne", type: "prislovka" },
  { text: "darí!", type: "sloveso" }
],
[
  { text: "Ojoj,", type: "citoslovce" },
  { text: "do", type: "predlozka" },
  { text: "našej", type: "zameno" },
  { text: "izby", type: "podstatne_meno" },
  { text: "vletela", type: "sloveso" },
  { text: "veľká", type: "pridavne_meno" },
  { text: "osa!", type: "podstatne_meno" }
],
[
  { text: "Dve", type: "cislovka" },
  { text: "usilovné", type: "pridavne_meno" },
  { text: "dievčatá", type: "podstatne_meno" },
  { text: "rýchlo", type: "prislovka" },
  { text: "vyčistili", type: "sloveso" },
  { text: "celú", type: "pridavne_meno" },
  { text: "školskú", type: "pridavne_meno" },
  { text: "tabuľu.", type: "podstatne_meno" }
],
[
  { text: "Aj", type: "spojka" },
  { text: "keď", type: "spojka" },
  { text: "bol", type: "sloveso" },
  { text: "unavený,", type: "pridavne_meno" },
  { text: "ochotne", type: "prislovka" },
  { text: "nám", type: "zameno" },
  { text: "pomohol.", type: "sloveso" }
],
[
  { text: "Pst,", type: "citoslovce" },
  { text: "v", type: "predlozka" },
  { text: "knižnici", type: "podstatne_meno" },
  { text: "musí", type: "sloveso" },
  { text: "byť", type: "sloveso" },
  { text: "úplné", type: "pridavne_meno" },
  { text: "ticho.", type: "podstatne_meno" }
],
[
  { text: "Vari", type: "castica" },
  { text: "ani", type: "spojka" },
  { text: "ty", type: "zameno" },
  { text: "nevieš", type: "sloveso" },
  { text: "správnu", type: "pridavne_meno" },
  { text: "odpoveď?", type: "podstatne_meno" }
],
[
  { text: "Stovky", type: "cislovka" },
  { text: "divákov", type: "podstatne_meno" },
  { text: "nadšene", type: "prislovka" },
  { text: "tlieskali", type: "sloveso" },
  { text: "šikovným", type: "pridavne_meno" },
  { text: "hercom.", type: "podstatne_meno" }
],

/* =========================================================================
   ÚROVEŇ 6 (71–80): Zložené súvetia a majstrovské vety
   ========================================================================= */
[
  { text: "Hoci", type: "spojka" },
  { text: "vonku", type: "prislovka" },
  { text: "husto", type: "prislovka" },
  { text: "pršalo,", type: "sloveso" },
  { text: "my", type: "zameno" },
  { text: "sme", type: "sloveso" },
  { text: "sa", type: "zameno" },
  { text: "veselo", type: "prislovka" },
  { text: "hrali", type: "sloveso" },
  { text: "v", type: "predlozka" },
  { text: "teplej", type: "pridavne_meno" },
  { text: "izbe.", type: "podstatne_meno" }
],
[
  { text: "Aha,", type: "citoslovce" },
  { text: "tam", type: "prislovka" },
  { text: "za", type: "predlozka" },
  { text: "kopcom", type: "podstatne_meno" },
  { text: "sa", type: "zameno" },
  { text: "zrazu", type: "prislovka" },
  { text: "objavila", type: "sloveso" },
  { text: "nádherná", type: "pridavne_meno" },
  { text: "farebná", type: "pridavne_meno" },
  { text: "dúha!", type: "podstatne_meno" }
],
[
  { text: "Prvý", type: "cislovka" },
  { text: "deň", type: "podstatne_meno" },
  { text: "sme", type: "sloveso" },
  { text: "usilovne", type: "prislovka" },
  { text: "pracovali,", type: "sloveso" },
  { text: "ale", type: "spojka" },
  { text: "druhý", type: "cislovka" },
  { text: "deň", type: "podstatne_meno" },
  { text: "sme", type: "sloveso" },
  { text: "dobre", type: "prislovka" },
  { text: "oddychovali.", type: "sloveso" }
],
[
  { text: "Kiež", type: "castica" },
  { text: "by", type: "sloveso" },
  { text: "všetci", type: "zameno" },
  { text: "ľudia", type: "podstatne_meno" },
  { text: "na", type: "predlozka" },
  { text: "svete", type: "podstatne_meno" },
  { text: "žili", type: "sloveso" },
  { text: "v", type: "predlozka" },
  { text: "pokoji", type: "podstatne_meno" },
  { text: "a", type: "spojka" },
  { text: "priateľstve!", type: "podstatne_meno" }
],
[
  { text: "Bác,", type: "citoslovce" },
  { text: "veľký", type: "pridavne_meno" },
  { text: "balík", type: "podstatne_meno" },
  { text: "spadol", type: "sloveso" },
  { text: "na", type: "predlozka" },
  { text: "zem,", type: "podstatne_meno" },
  { text: "ale", type: "spojka" },
  { text: "našťastie", type: "prislovka" },
  { text: "sa", type: "zameno" },
  { text: "nič", type: "zameno" },
  { text: "nerozbilo.", type: "sloveso" }
],
[
  { text: "Päť", type: "cislovka" },
  { text: "malých", type: "pridavne_meno" },
  { text: "vtáčat", type: "podstatne_meno" },
  { text: "nedočkavo", type: "prislovka" },
  { text: "otváralo", type: "sloveso" },
  { text: "zobáčiky,", type: "podstatne_meno" },
  { text: "keď", type: "spojka" },
  { text: "priletela", type: "sloveso" },
  { text: "ich", type: "zameno" },
  { text: "mama.", type: "podstatne_meno" }
],
[
  { text: "Veru,", type: "castica" },
  { text: "tento", type: "zameno" },
  { text: "múdry", type: "pridavne_meno" },
  { text: "učiteľ", type: "podstatne_meno" },
  { text: "vždy", type: "prislovka" },
  { text: "ochotne", type: "prislovka" },
  { text: "pomôže", type: "sloveso" },
  { text: "každému", type: "zameno" },
  { text: "žiakovi.", type: "podstatne_meno" }
],
[
  { text: "Chi-chi,", type: "citoslovce" },
  { text: "veselé", type: "pridavne_meno" },
  { text: "deti", type: "podstatne_meno" },
  { text: "sa", type: "zameno" },
  { text: "hlasno", type: "prislovka" },
  { text: "smiali,", type: "sloveso" },
  { text: "pretože", type: "spojka" },
  { text: "šašo", type: "podstatne_meno" },
  { text: "robil", type: "sloveso" },
  { text: "smiešne", type: "pridavne_meno" },
  { text: "kúsky.", type: "podstatne_meno" }
],
[
  { text: "Iba", type: "castica" },
  { text: "dve", type: "cislovka" },
  { text: "hodiny", type: "podstatne_meno" },
  { text: "nám", type: "zameno" },
  { text: "zostávajú", type: "sloveso" },
  { text: "do", type: "predlozka" },
  { text: "odchodu", type: "podstatne_meno" },
  { text: "rýchleho", type: "pridavne_meno" },
  { text: "vlaku.", type: "podstatne_meno" }
],
[
  { text: "Hľa,", type: "citoslovce" },
  { text: "naša", type: "zameno" },
  { text: "krajina", type: "podstatne_meno" },
  { text: "je", type: "sloveso" },
  { text: "krásna", type: "pridavne_meno" },
  { text: "a", type: "spojka" },
  { text: "všetci", type: "zameno" },
  { text: "ju", type: "zameno" },
  { text: "veľmi", type: "prislovka" },
  { text: "ľúbime.", type: "sloveso" }
]

];
