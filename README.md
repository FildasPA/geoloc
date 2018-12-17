# Notes

## TODO

- [X] connecter raspberry en ssh
- [X] relier la pile RTC au raspberry en configurant le bus i2c
- [X] connecter raspberry au wifi
- [X] connecter raspberry au module ZigBee
- [ ] Phase de finger printing
	- [ ] BDD
- [ ] Geolocalisation
	- [ ] créer l'interface permettant de localiser l'appareil dans la pièce

## Résumé des séances

### 13 novembre

- Réception & présentation du matériel
- Cartographie de la pièce à l'aide de l'application MagicPlan

### 16 novembre

- connexion par SSH avec le Raspberry
- configuration bus i2c avec la pile RTC
- communication ZigBee/balise (EndDevice) - ZigBee/coordinateur (Raspberry) (pas terminé)

### 19 novembre

- Communication coordinateur / balise (pas terminé)

### 23 novembre

- Réception du RSSI coordinateur / balise + filtrage (seulement notre RSSI)

### 14 décembre

- Recommencé la communication coordinateur / end device en mode AT car le mode API ne fonctionne pas (au niveau des balises). Désormais, les balises changent de PANID pour chaque groupe (1 PANID par coordinateur) pour qu'il n'y ai pas d'"interférences".

---

## [Cours] Positionnement par multilatération : RSS & fingerprinting

### RSSI : Received Signal Strength Indication

Mesure de la puissance en réception d'un signal reçu d'une antenne
Indique l'intensité du signal reçu
Permet de connaître la distance entre les appareils

### Phase de fingerprinting

Constituer une bdd des relevés de puissance pour un ensemble de positions dans la pièce

__Empreinte__ :
RSS(x, y) = [RSS1(x,y), RSS2(x,y), ..., RSSN(x,y)]

N = nombre de balises

-> calculer la moyenne des puissances (?)

-> constituer la radio map
-> L'appareil interrogera la bdd afin d'associer l'empreinte observée à une position dans l'espace
-> tiendra compte des singularités de chaque position : atténuations des murs, du mobilier...

Précision : nb de positions enregistrées + nb de balises déployées

XBEE: cavalier = émetteur = balise

---

## Matériel

- RaspberryPi
	- alimenté par le port USB TO UART
	- connecter par ssh
	- essayer de configurer le wifi
- carte mémoire 16 Gb + Rasbian (OS Debian)
	- y mettre la bdd, faire les calculs, etc.
- Pile RTC (pour connaître le temps en cas de perte du réseau)
- câble HDMI : Raspberry <> écran
- brancher le Raspberry sur la batterie avant de le brancher en USB à l'ordinateur
- coordinateur Zigbee (= l'objet qui se déplace)

---

## Communication RSSI :

- mode API : trames complètes (adresse MAC, RSSI, etc.) (+ fiable) -> extraire la valeur de RSSI de la trame
- commandes AT (transparent, Serial on air) : `+++` envoie seulement l'information demandée

(Envoyer une commande de "réveil" aux balises (on ne le fera pas))

__UART__ : Universal Asynchronous Receive/Transmit

Balise ──────────────── TX_XB ───────────────────── RX_Pi
             RSSI       RX_XB ───────────────────── TX_Pi
                               communication série

---

## Raspberry

### Pin

- Placer les cavaliers sur les pin suivants pour communiquer avec le module Zigbee

```
XB_RX │ XB_TX
P_TX  │  P_RX
```

- Placer le cavalier sur le pin 3V (car ZigBee fonctionne en 3V)

Voir [pinout](https://fr.pinout.xyz/#)


### Mettre à jour Rasbian

```
sudo apt-get update
sudo apt-get dist-upgrade
```

### Se connecter en SSH au Raspberry

Avoir l'adresse IP :

`ifconfig`

[Tutoriel](https://the-raspberry.com/ssh-raspberry-pi)

```
ssh pi@10.120.14.102
```

Mot de passe par défaut : `raspberry`

### Bus i2c (Pile RTC)

[Tutoriel qui marche](https://learn.adafruit.com/adding-a-real-time-clock-to-raspberry-pi/set-rtc-time)

Installer les paquets (normalement déjà installés) :

```
sudo apt-get install i2c-tools
sudo apt-get install python-smbus
```

Ajouter la ligne suivante __à la fin__ de `/boot/config.txt` :

```
dtoverlay=i2c-rtc,pcf8563
```

... [Suivre le tutoriel]


### Communication entre un coordinateur et un EndDevice ZigBee (balise)

#### Configuration des modules ZigBee sous XCTU

__Balise__

- `Channel` : D
- `ID PAN ID` : C133
- `DL` : BC2
- `MY` : BAF2
- `CA` : 28 -DBM
- `CE` : End Device [0]
- `API` : API disabled [0]
- `BD` : 115 200 [7]

__Coordinateur__

- `Channel` : B
- `ID PAN ID` : C233
- `DL` : FFFF
- `MY` : BC2
- `CE` : Coordinator
- `API` : API disabled [0]
- `BD` : 115 200 [7]
- `CHCB`

#### Putty (tester la communication)

Installer Putty :

`sudo apt-get install putty`

Vérifier dans les fichiers :

`nano /boot/config.txt`
-> Ajouter __à la fin__: `dtoverlay=i2c-rtc,pcf8563` (déjà fait, normalement)

`nano /boot/cmdline.txt`
-> enlever toutes les références à `AMA0`

`raspi-config`
-> (5) Interfacing options
	-> P6 Serial
		-> Shell : Non
		-> Port : Oui

`reboot`

__Configuration__ :
- Communication
	`Serial` (9600)
	Serial line : `/dev/ttySS0`
- Terminal
	- Cocher CR
	- Cocher LF
- Serial
	- Parity : `None`
	- Flow control : `None`

Penser à sauvegarder le profil !

#### Commandes AT à l'aide de Python

Coordinateur (Raspberry) => mode AT
Balise => mode API

#### Adresses MAC des balises :

| Truc    |       Truc       |
|:--------|:----------------:|
| BTK     | 0013A200417B740F |
| Balise1 | 0013A200417B7410 |
| Balise2 | 0013A20041511C12 |
| Balise3 | 0013A20041511A59 |
| Balise4 | 0013A20041511D0C |
| Balise5 | 0013A20041512DCD |

---

ATND

respecter le timeout

dmesg | grep tty

AT P0 (RSSI)
