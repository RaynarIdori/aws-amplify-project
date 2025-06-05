# AWS Amplify Crypto Platform 🚀

![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![AWS Lambda](https://img.shields.io/badge/AWS%20Lambda-FF9900?style=for-the-badge&logo=awslambda&logoColor=white)
![DynamoDB](https://img.shields.io/badge/Amazon%20DynamoDB-4053D6?style=for-the-badge&logo=Amazon%20DynamoDB&logoColor=white)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
![Version](https://img.shields.io/badge/version-1.0.0-blue)

Une plateforme complète de gestion de cryptomonnaies construite avec AWS Amplify, comprenant un backend serverless avec des fonctions Lambda Python, une base de données DynamoDB, et une API REST sécurisée.

## 📋 Table des Matières

- [Architecture](#-architecture)
- [Fonctionnalités](#-fonctionnalités)
- [Technologies](#-technologies)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Utilisation](#-utilisation)
- [Structure du Projet](#-structure-du-projet)
- [API Endpoints](#-api-endpoints)
- [Fonctions Lambda](#-fonctions-lambda)
- [Base de Données](#-base-de-données)
- [Déploiement](#-déploiement)
- [Contribution](#-contribution)
- [Licence](#-licence)

## 🏗️ Architecture

Cette application utilise une architecture serverless moderne sur AWS :

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   React App     │───▶│   API Gateway    │───▶│  Lambda Functions│
│   (Frontend)    │    │   (REST API)     │    │   (Python)      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                       ┌──────────────────┐    ┌─────────────────┐
                       │   Cognito Auth   │    │   DynamoDB      │
                       │   (Users & Auth) │    │   (Database)    │
                       └──────────────────┘    └─────────────────┘
                                                        │
                                               ┌─────────────────┐
                                               │      S3         │
                                               │   (Storage)     │
                                               └─────────────────┘
```

## ✨ Fonctionnalités

- 🔐 **Authentification sécurisée** avec AWS Cognito
- 📊 **Suivi des cryptomonnaies** en temps réel via l'API CoinGecko
- 👥 **Gestion des utilisateurs** (création, lecture, mise à jour)
- 📈 **Stockage des prix** historiques des cryptomonnaies
- 📄 **Export de données** avec génération d'URLs pré-signées
- 🔄 **Synchronisation automatique** des données crypto (cron job)
- 🛡️ **API REST sécurisée** avec CORS configuré

## 🛠️ Technologies

### Backend
- **AWS Amplify** - Framework de développement fullstack
- **AWS Lambda** - Fonctions serverless (Python 3.13)
- **Amazon DynamoDB** - Base de données NoSQL
- **Amazon S3** - Stockage d'objets
- **AWS Cognito** - Authentification et autorisation
- **API Gateway** - API REST managée

### Frontend
- **React** - Framework JavaScript
- **JavaScript/TypeScript** - Langages de programmation

### Outils et DevOps
- **Pipenv** - Gestion des dépendances Python
- **Git** - Contrôle de version
- **CloudFormation** - Infrastructure as Code

## 📋 Prérequis

- **Node.js** (v14+)
- **Python** (3.13)
- **AWS CLI** configuré
- **Amplify CLI** installé
- **Pipenv** pour la gestion des dépendances Python

```bash
# Installation des outils requis
npm install -g @aws-amplify/cli
pip install pipenv
```

## 🚀 Installation

### 1. Cloner le repository

```bash
git clone https://github.com/RaynarIdori/aws-amplify-project.git
cd aws-amplify-project
```

### 2. Installer les dépendances

```bash
# Dépendances du projet principal
pipenv install

# Dépendances des fonctions Lambda
cd amplify/backend/function/cryptoRyan && pipenv install
cd ../saveUserRyan && pipenv install
cd ../getUsersRyan && pipenv install
cd ../signeDataRyan && pipenv install
```

### 3. Configuration AWS Amplify

```bash
# Initialiser Amplify (si ce n'est pas déjà fait)
amplify configure

# Initialiser le projet
amplify init

# Déployer le backend
amplify push
```

## ⚙️ Configuration

### Variables d'environnement

Les fonctions Lambda utilisent les variables d'environnement suivantes (configurées automatiquement par Amplify) :

- `STORAGE_CRYPTOPRICESRYAN_NAME` - Nom de la table DynamoDB des prix crypto
- `STORAGE_USERS_NAME` - Nom de la table DynamoDB des utilisateurs
- `S3_BUCKET_NAME` - Nom du bucket S3 pour les exports

### Configuration de l'API CoinGecko

La fonction `cryptoRyan` utilise l'API CoinGecko avec une clé API :
```python
"x-cg-demo-api-key": "CG-x6GZDvgEMRyp4JJDjeyuxqJm"
```

## 📖 Utilisation

### Démarrage du projet

```bash
# Lancer l'environnement de développement
amplify serve

# Ou pour tester les fonctions localement
amplify mock
```

### Exemples d'utilisation des API

#### Créer un utilisateur
```bash
curl -X POST https://your-api-id.execute-api.region.amazonaws.com/dev/saveUsersRyan \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com"}'
```

#### Récupérer un utilisateur
```bash
curl "https://your-api-id.execute-api.region.amazonaws.com/dev/getUsers?email=john@example.com"
```

#### Récupérer les données crypto
```bash
curl "https://your-api-id.execute-api.region.amazonaws.com/dev/cryptos"
```

#### Exporter les données
```bash
curl "https://your-api-id.execute-api.region.amazonaws.com/dev/export"
```

## 📁 Structure du Projet

```
aws-amplify-project/
├── amplify/                          # Configuration Amplify
│   ├── backend/
│   │   ├── api/usersRyan/            # Configuration API Gateway
│   │   ├── auth/ryanawse2c93951/     # Configuration Cognito
│   │   ├── function/                 # Fonctions Lambda
│   │   │   ├── cryptoRyan/           # Récupération données crypto
│   │   │   ├── getUsersRyan/         # Lecture utilisateurs
│   │   │   ├── saveUserRyan/         # Création utilisateurs
│   │   │   └── signeDataRyan/        # Export de données
│   │   └── storage/                  # Configuration DynamoDB & S3
│   └── team-provider-info.json       # Configuration des environnements
├── .gitignore                        # Fichiers à ignorer
├── Pipfile                          # Dépendances Python
├── LICENSE                          # Licence MIT
└── README.md                        # Documentation
```

## 🔗 API Endpoints

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `POST` | `/saveUsersRyan` | Créer un nouvel utilisateur |
| `GET` | `/getUsers` | Récupérer un utilisateur par ID ou email |
| `GET` | `/cryptos` | Récupérer les données des cryptomonnaies |
| `GET` | `/export` | Exporter les données crypto vers S3 |

## ⚡ Fonctions Lambda

### 🪙 cryptoRyan
- **Trigger** : Cron job (tous les lundis à 12h30)
- **Fonction** : Récupère les données de l'API CoinGecko
- **Stockage** : DynamoDB table `cryptoPricesRyan`

### 👤 saveUserRyan
- **Trigger** : API Gateway POST
- **Fonction** : Création de nouveaux utilisateurs
- **Stockage** : DynamoDB table `users`

### 👥 getUsersRyan
- **Trigger** : API Gateway GET
- **Fonction** : Récupération d'utilisateurs
- **Paramètres** : `id` ou `email`

### 📊 signeDataRyan
- **Trigger** : API Gateway GET
- **Fonction** : Export des données crypto vers S3
- **Retour** : URL pré-signée pour téléchargement

## 🗄️ Base de Données

### Table `users`
- **Partition Key** : `id` (string)
- **Attributs** : `email`, `name`
- **Index** : `email-index` sur `email`

### Table `cryptoPricesRyan`
- **Partition Key** : `crypto_id` (string)
- **Sort Key** : `timestamp` (string)
- **Attributs** : Données complètes de l'API CoinGecko

### Bucket S3 `cryptoExportBucketRyan`
- **Usage** : Stockage des exports JSON
- **Structure** : `exports/crypto_YYYY-MM-DD_HH-MM-SS.json`

## 🚀 Déploiement

### Déploiement sur AWS

```bash
# Déployer toutes les ressources
amplify push

# Déployer seulement les fonctions
amplify push function

# Déployer l'API
amplify push api
```

### Environnements multiples

```bash
# Créer un nouvel environnement
amplify env add production

# Changer d'environnement
amplify env checkout production

# Lister les environnements
amplify env list
```

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. **Fork** le projet depuis [GitHub](https://github.com/RaynarIdori/aws-amplify-project/fork)
2. **Créer** une branche feature (`git checkout -b feature/amazing-feature`)
3. **Commit** vos changements (`git commit -m 'Add amazing feature'`)
4. **Push** vers la branche (`git push origin feature/amazing-feature`)
5. **Ouvrir** une Pull Request

### Guidelines de développement

- Suivre les conventions de nommage Python (PEP 8)
- Ajouter des tests pour les nouvelles fonctionnalités
- Documenter les changements dans le README
- Respecter la structure des commits conventionnels

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 📞 Support

Pour toute question ou support :

- 📧 **Email** : [contact@example.com](mailto:contact@example.com)
- 🐛 **Issues** : [GitHub Issues](https://github.com/RaynarIdori/aws-amplify-project/issues)
- 📚 **Documentation AWS** : [AWS Amplify Docs](https://docs.amplify.aws/)

---

**Développé avec ❤️ par IDORI** 