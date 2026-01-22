# TP Multithreading

Projet d'architecture distribuée avec communication via queues partagées et proxy HTTP.

## Architecture

```
Boss (Python)
    ↓   
QueueManager (port 50000)
    ↓  
Proxy HTTP (port 8000) ← → Client C++
    ↓
Minions (Python)
```

**Composants :**
- **Boss** : crée les tâches et collecte les résultats
- **QueueManager** : gère deux queues partagées (tâches et résultats)
- **Proxy HTTP** : expose les queues via HTTP (GET pour récupérer une tâche, POST pour renvoyer un résultat)
- **Minions** : workers Python qui traitent les tâches
- **Client C++** : worker C++ qui communique via le proxy HTTP

## Installation

### Dépendances Python

```bash
# Avec uv
uv sync

# Ou avec pip
pip install -r requirements.txt
```

### Compilation du client C++

```bash
# Configuration
cmake -B build -S .

# Compilation
cmake --build build
```

## Utilisation

### Ordre de lancement

Lancer dans cet ordre précis :

```bash
# Terminal 1 - Boss 
python3 boss.py

# Terminal 2 - Proxy HTTP 
python3 proxy.py

# Terminal 3 - Client C++ (optionnel)
./build/low_level

# Terminal 4 - Minions Python (autant que souhaité)
python3 minion.py
```

1. Le boss crée 5 tâches et les met dans la queue
2. Les minions (Python ou C++) récupèrent les tâches, les traitent, et renvoient les résultats
3. Le boss affiche les résultats au fur et à mesure
4. Une fois les 5 tâches terminées, le boss continue de tourner (Ctrl+C pour arrêter)

### Ports utilisés

- **50000** : QueueManager (communication interne)
- **8000** : Proxy HTTP (API REST)

# API du Proxy

### GET /
Récupère une tâche depuis la queue

**Réponse :**
```json
{
  "identifier": 0,
  "n": [1.0, 2.0, 3.0],
  "a": [[1.0, 2.0], [3.0, 4.0]],
  "b": [5.0, 6.0]
}
```

### POST /
Renvoie une tâche complétée

**Requête :**
```json
{
  "identifier": 0,
  "time": 0.0042,
  "x": [1.0, 2.0]
}
```

**Réponse :**
```json
{
  "status": "ok"
}
```
