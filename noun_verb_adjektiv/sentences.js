const sentences = [

/* LEVEL 1 (1–5) simple */
[{text:"Der",type:"other"},{text:"kleine",type:"adjective"},{text:"Hund",type:"noun"},{text:"läuft.",type:"verb"}],
[{text:"Die",type:"other"},{text:"rote",type:"adjective"},{text:"Katze",type:"noun"},{text:"schläft.",type:"verb"}],
[{text:"Ein",type:"other"},{text:"großer",type:"adjective"},{text:"Ball",type:"noun"},{text:"rollt.",type:"verb"}],
[{text:"Das",type:"other"},{text:"fröhliche",type:"adjective"},{text:"Kind",type:"noun"},{text:"lacht.",type:"verb"}],
[{text:"Der",type:"other"},{text:"alte",type:"adjective"},{text:"Mann",type:"noun"},{text:"geht.",type:"verb"}],

/* LEVEL 2 (6–10) + object */
[{text:"Der",type:"other"},{text:"kleine",type:"adjective"},{text:"Hund",type:"noun"},{text:"frisst",type:"verb"},{text:"Futter.",type:"noun"}],
[{text:"Die",type:"other"},{text:"rote",type:"adjective"},{text:"Katze",type:"noun"},{text:"jagt",type:"verb"},{text:"eine",type:"other"},{text:"Maus.",type:"noun"}],
[{text:"Ein",type:"other"},{text:"großer",type:"adjective"},{text:"Junge",type:"noun"},{text:"wirft",type:"verb"},{text:"den",type:"other"},{text:"Ball.",type:"noun"}],
[{text:"Das",type:"other"},{text:"kleine",type:"adjective"},{text:"Kind",type:"noun"},{text:"isst",type:"verb"},{text:"einen",type:"other"},{text:"Apfel.",type:"noun"}],
[{text:"Der",type:"other"},{text:"alte",type:"adjective"},{text:"Mann",type:"noun"},{text:"liest",type:"verb"},{text:"ein",type:"other"},{text:"Buch.",type:"noun"}],

/* LEVEL 3 (11–20) prepositions */
[{text:"Der",type:"other"},{text:"kleine",type:"adjective"},{text:"Hund",type:"noun"},{text:"läuft",type:"verb"},{text:"im",type:"other"},{text:"Garten.",type:"noun"}],
[{text:"Die",type:"other"},{text:"rote",type:"adjective"},{text:"Katze",type:"noun"},{text:"sitzt",type:"verb"},{text:"auf",type:"other"},{text:"dem",type:"other"},{text:"Tisch.",type:"noun"}],
[{text:"Ein",type:"other"},{text:"großer",type:"adjective"},{text:"Vogel",type:"noun"},{text:"fliegt",type:"verb"},{text:"über",type:"other"},{text:"das",type:"other"},{text:"Haus.",type:"noun"}],
[{text:"Das",type:"other"},{text:"kleine",type:"adjective"},{text:"Kind",type:"noun"},{text:"spielt",type:"verb"},{text:"mit",type:"other"},{text:"dem",type:"other"},{text:"Ball.",type:"noun"}],
[{text:"Der",type:"other"},{text:"alte",type:"adjective"},{text:"Mann",type:"noun"},{text:"geht",type:"verb"},{text:"durch",type:"other"},{text:"den",type:"other"},{text:"Park.",type:"noun"}],
[{text:"Die",type:"other"},{text:"kleine",type:"adjective"},{text:"Maus",type:"noun"},{text:"läuft",type:"verb"},{text:"unter",type:"other"},{text:"den",type:"other"},{text:"Tisch.",type:"noun"}],
[{text:"Ein",type:"other"},{text:"schneller",type:"adjective"},{text:"Zug",type:"noun"},{text:"fährt",type:"verb"},{text:"in",type:"other"},{text:"die",type:"other"},{text:"Stadt.",type:"noun"}],
[{text:"Das",type:"other"},{text:"fröhliche",type:"adjective"},{text:"Kind",type:"noun"},{text:"tanzt",type:"verb"},{text:"auf",type:"other"},{text:"der",type:"other"},{text:"Bühne.",type:"noun"}],
[{text:"Der",type:"other"},{text:"große",type:"adjective"},{text:"Bär",type:"noun"},{text:"sitzt",type:"verb"},{text:"am",type:"other"},{text:"Fluss.",type:"noun"}],
[{text:"Die",type:"other"},{text:"junge",type:"adjective"},{text:"Frau",type:"noun"},{text:"steht",type:"verb"},{text:"vor",type:"other"},{text:"dem",type:"other"},{text:"Haus.",type:"noun"}],

/* LEVEL 4 (21–40) 2 adjectives */
[{text:"Der",type:"other"},{text:"kleine",type:"adjective"},{text:"braune",type:"adjective"},{text:"Hund",type:"noun"},{text:"läuft.",type:"verb"}],
[{text:"Die",type:"other"},{text:"schöne",type:"adjective"},{text:"rote",type:"adjective"},{text:"Blume",type:"noun"},{text:"blüht.",type:"verb"}],
[{text:"Ein",type:"other"},{text:"großer",type:"adjective"},{text:"starker",type:"adjective"},{text:"Mann",type:"noun"},{text:"trägt.",type:"verb"},{text:"eine",type:"other"},{text:"Kiste.",type:"noun"}],
[{text:"Das",type:"other"},{text:"kleine",type:"adjective"},{text:"lustige",type:"adjective"},{text:"Kind",type:"noun"},{text:"lacht.",type:"verb"}],
[{text:"Der",type:"other"},{text:"alte",type:"adjective"},{text:"weise",type:"adjective"},{text:"Lehrer",type:"noun"},{text:"spricht.",type:"verb"}],
[{text:"Die",type:"other"},{text:"große",type:"adjective"},{text:"weiße",type:"adjective"},{text:"Katze",type:"noun"},{text:"schläft.",type:"verb"}],
[{text:"Das",type:"other"},{text:"schnelle",type:"adjective"},{text:"rote",type:"adjective"},{text:"Auto",type:"noun"},{text:"fährt.",type:"verb"}],
[{text:"Der",type:"other"},{text:"kleine",type:"adjective"},{text:"schlaue",type:"adjective"},{text:"Fuchs",type:"noun"},{text:"springt.",type:"verb"}],
[{text:"Die",type:"other"},{text:"alte",type:"adjective"},{text:"graue",type:"adjective"},{text:"Eule",type:"noun"},{text:"fliegt.",type:"verb"}],
[{text:"Das",type:"other"},{text:"große",type:"adjective"},{text:"blaue",type:"adjective"},{text:"Haus",type:"noun"},{text:"steht.",type:"verb"}],
[{text:"Der",type:"other"},{text:"schnelle",type:"adjective"},{text:"mutige",type:"adjective"},{text:"Junge",type:"noun"},{text:"rennt.",type:"verb"}],
[{text:"Die",type:"other"},{text:"kleine",type:"adjective"},{text:"freundliche",type:"adjective"},{text:"Maus",type:"noun"},{text:"findet.",type:"verb"},{text:"Käse.",type:"noun"}],
[{text:"Das",type:"other"},{text:"große",type:"adjective"},{text:"grüne",type:"adjective"},{text:"Feld",type:"noun"},{text:"blüht.",type:"verb"}],
[{text:"Der",type:"other"},{text:"alte",type:"adjective"},{text:"kranke",type:"adjective"},{text:"Hund",type:"noun"},{text:"ruht.",type:"verb"}],
[{text:"Die",type:"other"},{text:"schöne",type:"adjective"},{text:"bunte",type:"adjective"},{text:"Blume",type:"noun"},{text:"duftet.",type:"verb"}],
[{text:"Das",type:"other"},{text:"kleine",type:"adjective"},{text:"schnelle",type:"adjective"},{text:"Kind",type:"noun"},{text:"läuft.",type:"verb"}],
[{text:"Der",type:"other"},{text:"große",type:"adjective"},{text:"starke",type:"adjective"},{text:"Bär",type:"noun"},{text:"schwimmt.",type:"verb"}],
[{text:"Die",type:"other"},{text:"alte",type:"adjective"},{text:"weise",type:"adjective"},{text:"Frau",type:"noun"},{text:"liest.",type:"verb"}],
[{text:"Das",type:"other"},{text:"schöne",type:"adjective"},{text:"helle",type:"adjective"},{text:"Zimmer",type:"noun"},{text:"leuchtet.",type:"verb"}],
[{text:"Der",type:"other"},{text:"kleine",type:"adjective"},{text:"fröhliche",type:"adjective"},{text:"Junge",type:"noun"},{text:"singt.",type:"verb"}],
[{text:"Die",type:"other"},{text:"große",type:"adjective"},{text:"schnelle",type:"adjective"},{text:"Katze",type:"noun"},{text:"klettert.",type:"verb"}],
[{text:"Das",type:"other"},{text:"alte",type:"adjective"},{text:"braune",type:"adjective"},{text:"Buch",type:"noun"},{text:"liegt.",type:"verb"}],
[{text:"Der",type:"other"},{text:"schöne",type:"adjective"},{text:"blaue",type:"adjective"},{text:"Vogel",type:"noun"},{text:"fliegt.",type:"verb"}],
[{text:"Die",type:"other"},{text:"kleine",type:"adjective"},{text:"schlaue",type:"adjective"},{text:"Maus",type:"noun"},{text:"versteckt.",type:"verb"}],
[{text:"Das",type:"other"},{text:"große",type:"adjective"},{text:"helle",type:"adjective"},{text:"Haus",type:"noun"},{text:"strahlt.",type:"verb"}],

/* continue pattern progressively… */

/* LEVEL 5 (41–70) longer phrases */
[{text:"Der",type:"other"},{text:"kleine",type:"adjective"},{text:"Hund",type:"noun"},{text:"läuft",type:"verb"},{text:"schnell",type:"other"},{text:"durch",type:"other"},{text:"den",type:"other"},{text:"großen",type:"adjective"},{text:"Garten.",type:"noun"}],
[{text:"Die",type:"other"},{text:"freundliche",type:"adjective"},{text:"Lehrerin",type:"noun"},{text:"erklärt",type:"verb"},{text:"geduldig",type:"other"},{text:"die",type:"other"},{text:"schwere",type:"adjective"},{text:"Aufgabe.",type:"noun"}],
[{text:"Der",type:"other"},{text:"alte",type:"adjective"},{text:"Mann",type:"noun"},{text:"liest",type:"verb"},{text:"ruhig",type:"other"},{text:"in",type:"other"},{text:"dem",type:"other"},{text:"bequemen",type:"adjective"},{text:"Sessel.",type:"noun"}],
[{text:"Das",type:"other"},{text:"kleine",type:"adjective"},{text:"Kind",type:"noun"},{text:"malt",type:"verb"},{text:"fröhlich",type:"other"},{text:"mit",type:"other"},{text:"bunten",type:"adjective"},{text:"Stiften.",type:"noun"}],
[{text:"Die",type:"other"},{text:"schnelle",type:"adjective"},{text:"Katze",type:"noun"},{text:"springt",type:"verb"},{text:"über",type:"other"},{text:"den",type:"other"},{text:"hohen",type:"adjective"},{text:"Zaun.",type:"noun"}],
[{text:"Ein",type:"other"},{text:"großer",type:"adjective"},{text:"Vogel",type:"noun"},{text:"singt",type:"verb"},{text:"laut",type:"other"},{text:"auf",type:"other"},{text:"dem",type:"other"},{text:"alten",type:"adjective"},{text:"Baum.",type:"noun"}],
[{text:"Der",type:"other"},{text:"kleine",type:"adjective"},{text:"Junge",type:"noun"},{text:"rennt",type:"verb"},{text:"schnell",type:"other"},{text:"zu",type:"other"},{text:"seinem",type:"other"},{text:"Freund.",type:"noun"}],
[{text:"Die",type:"other"},{text:"alte",type:"adjective"},{text:"Frau",type:"noun"},{text:"geht",type:"verb"},{text:"langsam",type:"other"},{text:"durch",type:"other"},{text:"den",type:"other"},{text:"Park.",type:"noun"}],
[{text:"Das",type:"other"},{text:"große",type:"adjective"},{text:"Haus",type:"noun"},{text:"steht",type:"verb"},{text:"am",type:"other"},{text:"Ende",type:"noun"},{text:"der",type:"other"},{text:"Straße.",type:"noun"}],
[{text:"Der",type:"other"},{text:"freundliche",type:"adjective"},{text:"Hund",type:"noun"},{text:"spielt",type:"verb"},{text:"mit",type:"other"},{text:"dem",type:"other"},{text:"Ball.",type:"noun"}],
[{text:"Die",type:"other"},{text:"kleine",type:"adjective"},{text:"Katze",type:"noun"},{text:"schläft",type:"verb"},{text:"auf",type:"other"},{text:"dem",type:"other"},{text:"Sofa.",type:"noun"}],
[{text:"Das",type:"other"},{text:"fröhliche",type:"adjective"},{text:"Kind",type:"noun"},{text:"tanzt",type:"verb"},{text:"auf",type:"other"},{text:"der",type:"other"},{text:"Bühne.",type:"noun"}],
[{text:"Der",type:"other"},{text:"große",type:"adjective"},{text:"Bär",type:"noun"},{text:"sitzt",type:"verb"},{text:"am",type:"other"},{text:"Fluss.",type:"noun"}],
[{text:"Die",type:"other"},{text:"junge",type:"adjective"},{text:"Frau",type:"noun"},{text:"steht",type:"verb"},{text:"vor",type:"other"},{text:"dem",type:"other"},{text:"Haus.",type:"noun"}],
[{text:"Das",type:"other"},{text:"kleine",type:"adjective"},{text:"Kind",type:"noun"},{text:"spielt",type:"verb"},{text:"mit",type:"other"},{text:"dem",type:"other"},{text:"Ball.",type:"noun"}],
[{text:"Der",type:"other"},{text:"alte",type:"adjective"},{text:"Mann",type:"noun"},{text:"geht",type:"verb"},{text:"durch",type:"other"},{text:"den",type:"other"},{text:"Park.",type:"noun"}],
[{text:"Die",type:"other"},{text:"kleine",type:"adjective"},{text:"Maus",type:"noun"},{text:"läuft",type:"verb"},{text:"unter",type:"other"},{text:"den",type:"other"},{text:"Tisch.",type:"noun"}],
[{text:"Ein",type:"other"},{text:"schneller",type:"adjective"},{text:"Zug",type:"noun"},{text:"fährt",type:"verb"},{text:"in",type:"other"},{text:"die",type:"other"},{text:"Stadt.",type:"noun"}],
[{text:"Das",type:"other"},{text:"fröhliche",type:"adjective"},{text:"Kind",type:"noun"},{text:"tanzt",type:"verb"},{text:"auf",type:"other"},{text:"der",type:"other"},{text:"Bühne.",type:"noun"}],
[{text:"Der",type:"other"},{text:"große",type:"adjective"},{text:"Bär",type:"noun"},{text:"sitzt",type:"verb"},{text:"am",type:"other"},{text:"Fluss.",type:"noun"}],
[{text:"Die",type:"other"},{text:"junge",type:"adjective"},{text:"Frau",type:"noun"},{text:"steht",type:"verb"},{text:"vor",type:"other"},{text:"dem",type:"other"},{text:"Haus.",type:"noun"}],

/* LEVEL 6 (71–100) complex */
[{text:"Der",type:"other"},{text:"kleine",type:"adjective"},{text:"Hund",type:"noun"},{text:"läuft",type:"verb"},{text:"schnell",type:"other"},{text:"durch",type:"other"},{text:"den",type:"other"},{text:"großen",type:"adjective"},{text:"Garten,",type:"noun"},{text:"weil",type:"other"},{text:"er",type:"other"},{text:"spielen",type:"verb"},{text:"will.",type:"verb"}],
[{text:"Die",type:"other"},{text:"junge",type:"adjective"},{text:"Schülerin",type:"noun"},{text:"lernt",type:"verb"},{text:"fleißig",type:"other"},{text:"für",type:"other"},{text:"die",type:"other"},{text:"schwere",type:"adjective"},{text:"Prüfung,",type:"noun"},{text:"damit",type:"other"},{text:"sie",type:"other"},{text:"besteht.",type:"verb"}]
[{text:"Der",type:"other"},{text:"große",type:"adjective"},{text:"Bär",type:"noun"},{text:"sitzt",type:"verb"},{text:"am",type:"other"},{text:"Fluss",type:"noun"},{text:"und",type:"other"},{text:"beobachtet",type:"verb"},{text:"die",type:"other"},{text:"Fische.",type:"noun"}],
[{text:"Die",type:"other"},{text:"freundliche",type:"adjective"},{text:"Lehrerin",type:"noun"},{text:"erklärt",type:"verb"},{text:"geduldig",type:"other"},{text:"die",type:"other"},{text:"schwere",type:"adjective"},{text:"Aufgabe",type:"noun"},{text:"während",type:"other"},{text:"die",type:"other"},{text:"Schüler",type:"noun"},{text:"zuhören.",type:"verb"}],
[{text:"Das",type:"other"},{text:"kleine",type:"adjective"},{text:"Kind",type:"noun"},{text:"malt",type:"verb"},{text:"fröhlich",type:"other"},{text:"mit",type:"other"},{text:"bunten",type:"adjective"},{text:"Stiften",type:"noun"},{text:"während",type:"other"},{text:"die",type:"other"},{text:"Mutter",type:"noun"},{text:"liest.",type:"verb"}],
[{text:"Die",type:"other"},{text:"schnelle",type:"adjective"},{text:"Katze",type:"noun"},{text:"springt",type:"verb"},{text:"über",type:"other"},{text:"den",type:"other"},{text:"hohen",type:"adjective"},{text:"Zaun",type:"noun"},{text:"weil",type:"other"},{text:"sie",type:"other"},{text:"die",type:"other"},{text:"Vögel",type:"noun"},{text:"sehen",type:"verb"},{text:"will.",type:"verb"}],
[{text:"Ein",type:"other"},{text:"großer",type:"adjective"},{text:"Vogel",type:"noun"},{text:"singt",type:"verb"},{text:"laut",type:"other"},{text:"auf",type:"other"},{text:"dem",type:"other"},{text:"alten",type:"adjective"},{text:"Baum",type:"noun"},{text:"während",type:"other"},{text:"die",type:"other"},{text:"Sonne",type:"noun"},{text:"scheint.",type:"verb"}]
[{text:"Der",type:"other"},{text:"kleine",type:"adjective"},{text:"Hund",type:"noun"},{text:"bellt",type:"verb"},{text:"laut",type:"other"},{text:"weil",type:"other"},{text:"er",type:"other"},{text:"den",type:"other"},{text:"Postboten",type:"noun"},{text:"sieht.",type:"verb"}],
[{text:"Die",type:"other"},{text:"alte",type:"adjective"},{text:"Frau",type:"noun"},{text:"geht",type:"verb"},{text:"langsam",type:"other"},{text:"durch",type:"other"},{text:"den",type:"other"},{text:"Park",type:"noun"},{text:"während",type:"other"},{text:"sie",type:"other"},{text:"mit",type:"other"},{text:"ihrem",type:"other"},{text:"Hund",type:"noun"},{text:"spricht.",type:"verb"}],
[{text:"Das",type:"other"},{text:"große",type:"adjective"},{text:"Haus",type:"noun"},{text:"steht",type:"verb"},{text:"am",type:"other"},{text:"Ende",type:"noun"},{text:"der",type:"other"},{text:"Straße",type:"noun"},{text:"während",type:"other"},{text:"die",type:"other"},{text:"Kinder",type:"noun"},{text:"spielen.",type:"verb"}],
[{text:"Der",type:"other"},{text:"freundliche",type:"adjective"},{text:"Hund",type:"noun"},{text:"spielt",type:"verb"},{text:"mit",type:"other"},{text:"dem",type:"other"},{text:"Ball",type:"noun"},{text:"während",type:"other"},{text:"die",type:"other"},{text:"Sonne",type:"noun"},{text:"scheint.",type:"verb"}],
[{text:"Die",type:"other"},{text:"kleine",type:"adjective"},{text:"Katze",type:"noun"},{text:"schläft",type:"verb"},{text:"auf",type:"other"},{text:"dem",type:"other"},{text:"Sofa",type:"noun"},{text:"während",type:"other"},{text:"der",type:"other"},{text:"Hund",type:"noun"},{text:"bellt.",type:"verb"}],
[{text:"Das",type:"other"},{text:"fröhliche",type:"adjective"},{text:"Kind",type:"noun"},{text:"tanzt",type:"verb"},{text:"auf",type:"other"},{text:"der",type:"other"},{text:"Bühne",type:"noun"},{text:"während",type:"other"},{text:"die",type:"other"},{text:"Musik",type:"noun"},{text:"spielt.",type:"verb"}],
[{text:"Der",type:"other"},{text:"große",type:"adjective"},{text:"Bär",type:"noun"},{text:"sitzt",type:"verb"},{text:"am",type:"other"},{text:"Fluss",type:"noun"},{text:"und",type:"other"},{text:"beobachtet",type:"verb"},{text:"die",type:"other"},{text:"Fische",type:"noun"},{text:"während",type:"other"},{text:"die",type:"other"},{text:"Sonne",type:"noun"},{text:"scheint.",type:"verb"}],
[{text:"Die",type:"other"},{text:"junge",type:"adjective"},{text:"Frau",type:"noun"},{text:"steht",type:"verb"},{text:"vor",type:"other"},{text:"dem",type:"other"},{text:"Haus",type:"noun"},{text:"während",type:"other"},{text:"sie",type:"other"},{text:"telefoniert.",type:"verb"}],

];