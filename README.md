<div align="center">
<img src="./static/images/demo.png" alt="Démo"/>
  
# MoneyTracker

A l'ère du numérique, il est parfois difficile de gérer son argent. MoneyTracker est là pour vous aider à gérer vos finances personnelles. 📊

</div>

# 📖 • Sommaire

- [🚀 • Présentation](#--présentation)
- [📦 • Installation](#--installation)
   - [🐳 • Docker](#--docker)
   - [💻 • Installation manuelle](#--installation-manuelle)
- [📑 • Utilisation](#--utilisation)
- [📃 • Crédits](#--crédits)
- [📝 • License](#--license)

# 🚀 • Présentation

MoneyTracker est un outil de gestion de finances personnelles. Il permet de suivre ses dépenses et ses revenus, de les catégoriser et de les analyser. MoneyTracker est un outil simple et intuitif, qui vous permettra de mieux gérer votre argent.  
Actuellement la seule banque supportée est LCL, mais d'autres banques pourraient être ajoutées à l'avenir.

> [!NOTE]  
> Une démo est disponible [ici](https://money.bayfield.dev/demo).
  
# 📦 • Installation

Pour installer MoneyTracker, vous aurez besoin de [Python](https://www.python.org/) et de [Git](https://git-scm.com/).

1. Clonez le dépôt GitHub :
```bash
git clone https://github.com/PaulBayfield/MoneyTracker.git
```

2. Configuration de l'environnement :
```bash
# API
API_HOST = 0.0.0.0
API_PORT = 5000
API_DOMAIN = http://localhost:5000
API_DEBUG = True

# APP
APP_SECRET = 

# Postgres
POSTGRES_DATABASE =
POSTGRES_USER =
POSTGRES_PASSWORD =
POSTGRES_HOST =
POSTGRES_PORT =

# Data
CACHE = 86400

# Labels
LABEL_ALIMENTATION = CARREFOUR
LABEL_TRANSPORT = SANEF
LABEL_LOGEMENT = EDF
LABEL_ABONNEMENTS = NETFLIX,ORANGE,SFR,BOUYGUES TELECOM,FREE
LABEL_LOISIRS = CINEMA,UGC,GAUMONT
LABEL_RESTAURANTS = RESTAURANT
LABEL_SANTE = PHARMACIE
LABEL_DIVERS = COIFFURE
LABEL_ACHATS = AMAZON
LABEL_EPARGNE = 
```

3. Création d'un profil bancaire :
```bash
cd profiles
mkdir PROFIL_NAME_LOWERCASE
```

4. Création d'un fichier `.env` dans le dossier du profil bancaire :
```bash
ACCOUNT_IDENTIFIER = 
ACCOUNT_ID = 
CONTRACT_ID = 
KEYPAD = 
SESSION_ID = 
```

## 🐳 • Docker

5. Lancez le conteneur Docker :
```bash
docker compose up
```

## 💻 • Installation manuelle

5. Installez les dépendances :
```bash
pip install -r requirements.txt
```

6. Lancez le serveur :
```bash
python __main__.py
```

> [!WARNING]  
> Vous devez aussi installer [PostgreSQL](https://www.postgresql.org/) pour stocker les données.  
> Après l'intallation, créez une base de données et ajoutez les informations de connexion dans le fichier `.env`.  
> Vous devez IMPERATIVEMENT créer un utilisateur pour pouvoir vous connecter à l'application par la suite !
>  
> ```sql
> INSERT INTO users(username, password, account)
> VALUES ('USERNAME', crypt('PASSWORD', gen_salt('bf')), LCL_ACCOUNT_IDENTIFIER);
> ```


# 📑 • Utilisation

1. Connectez-vous à l'application :
```
http://localhost:5000/user/login
```

2. Ouvrez le dashboard :
```
http://localhost:5000
```

# 📃 • Crédits

- [Paul Bayfield](https://github.com/PaulBayfield)

# 📝 • License

MoneyTracker sous licence [Apache 2.0](LICENSE).

```
Copyright 2024 Paul Bayfield

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
