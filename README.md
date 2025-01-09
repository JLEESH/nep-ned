# NepNed - Nep-Nederlands: Zodat Engelstaligen Nederlands kunnen lezen
Het vertalen van Engels in een spelling die lijkt op Nederlands voor educatie en entertainment.


Vereist ``OPENAI_API_KEY`` in ``.env``.

e.g. ``echo "OPEN_AI_KEY=<your-key-here>" > .env``

# Voorbelden

### Basis voorbeeld: 

``python3.12 nepned.py -gt "We have a serious problem. We are not using nearly enough nep Dutch."``

```
English: We have a serious problem. We are not using nearly enough nep Dutch.

Neperlands: We hebbe een serieus probleem. We üsen niet naarlig genoeg nep nederlands.

Dutch: We hebben een serieus probleem. We gebruiken niet bijna genoeg nep Nederlands.
```

### Voor een willekeurige voorbeeldzin: 

``python3.12 nepned.py -t "(Instead of translating a given sentence give a sample sentence instead)" -v 5``

```
{
    "original": "The garden is full of beautiful flowers and buzzing bees.",
    "hybrid": "De garden is vol van mooie bloemen en buzzing bijen.",
    "translation": "De tuin is vol met mooie bloemen en zoemende bijen."
}
```

(Er worden zowel tekst- als JSON-uitvoer gegenereerd en opgeslagen.)


## Text
```
English: The cat on the roof is very playful.
Neperlands: De kat op de roof is erg speels.
Dutch: De kat op het dak is erg speels.
```

```
English: The beautiful flower in the garden attracts many bees and butterflies.

Neperlands: De mooie flower in de garden trekt veel bees en butterflies aan.

Dutch: De mooie bloem in de tuin trekt veel bijen en vlinders aan.
```
## JSON
```
{
    "original": "The children are playing in the garden during the sunny day.",
    "hybrid": "De kinderen zijn pleijen in de garden tijdens de zonnige dag.",
    "translation": "De kinderen zijn aan het spelen in de tuin tijdens de zonnige dag."
}
```

```
{
    "original": "The sun sets beautifully over the hills during autumn.",
    "hybrid": "De zon set mooi over de heuvels tijdens de herfst.",
    "translation": "De zon ondergaat prachtig over de heuvels tijdens de herfst."
}
```