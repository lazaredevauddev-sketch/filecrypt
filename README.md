# filecrypt

Chiffre et déchiffre un fichier avec un mot de passe. Chiffrement symétrique
(Fernet / AES), et la clé est dérivée du mot de passe avec PBKDF2 pour ne pas
utiliser le mot de passe brut comme clé.

Le sel aléatoire est écrit au début du fichier chiffré, donc même mot de passe
sur deux fichiers = deux résultats différents.

## Install

```
pip install -r requirements.txt
```

## Utilisation

```
python filecrypt.py enc secret.txt      # cree secret.txt.enc
python filecrypt.py dec secret.txt.enc  # cree secret.txt.dec
```

Le mot de passe est demandé au clavier (pas affiché).

Si le mot de passe est faux au déchiffrement, ça plante avec une erreur de
signature invalide. C'est voulu : Fernet vérifie l'intégrité, on ne récupère
pas un fichier corrompu en silence.

## A creuser

- chiffrer un dossier entier
- remplacer le fichier original au lieu de créer un .enc à côté
- comprendre pourquoi 390000 itérations PBKDF2 et à quoi ça sert contre le brute-force
