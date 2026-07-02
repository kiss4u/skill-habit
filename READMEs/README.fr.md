<h1 align="center">skill-habit</h1>

<h3 align="center">Vos habitudes façonnent vos outils.</h3>

<p align="center">
  Suivez vos habitudes d'utilisation des compétences IA — commandes classées par fréquence, les plus utilisées toujours en premier.<br>
  À chaque session, la bonne compétence est à une touche — sans parcourir la liste, sans deviner.<br>
  Inclut des analyses d'utilisation, une carte thermique d'activité, la prédiction de séquences, la gestion des compétences et un tableau de bord web.
</p>

<p align="center">
  <a href="README.en.md">English</a> |
  <a href="../README.md">简体中文</a> |
  <a href="README.zh-TW.md">繁體中文</a> |
  <a href="README.de.md">Deutsch</a> |
  <a href="README.fr.md">Français</a> |
  <a href="README.ru.md">Русский</a> |
  <a href="README.ko.md">한국어</a> |
  <a href="README.ja.md">日本語</a>
</p>

<p align="center">
  <a href="#-démarrage-rapide"><img src="https://img.shields.io/badge/Quick%20Start-→-blueviolet?style=flat-square" alt="Quick Start"></a>
  <a href="../LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square" alt="MIT License"></a>
  <img src="https://img.shields.io/badge/Claude%20Code-✓-7c3aed?style=flat-square" alt="Claude Code">
  <img src="https://img.shields.io/badge/Python-3.7%2B-3776ab?style=flat-square&logo=python&logoColor=white" alt="Python 3.7+">
  <img src="https://img.shields.io/badge/version-0.0.1-brightgreen?style=flat-square" alt="version">
  <a href="https://github.com/kiss4u/skill-habit/stargazers"><img src="https://img.shields.io/github/stars/kiss4u/skill-habit?style=flat-square&color=orange" alt="GitHub Stars"></a>
</p>

---

## Table des matières

- [🤔 Le problème](#-le-problème)
- [💡 La solution](#-la-solution)
- [✨ Fonctionnalités](#-fonctionnalités)
  - [🔑 Préfixe de raccourci](#-préfixe-de-raccourci)
  - [🔮 Prédiction par association (Ordre intelligent)](#-prédiction-par-association-ordre-intelligent)
  - [📐 Ordre des raccourcis numériques](#-ordre-des-raccourcis-numériques)
  - [🔒 Confidentialité](#-confidentialité)
- [🚀 Démarrage rapide](#-démarrage-rapide)
  - [Installation](#installation)
  - [Mise à niveau](#mise-à-niveau)
  - [Désinstallation](#désinstallation)
  - [Configuration](#configuration)
- [Skills intégrés de skill-habit](#skills-intégrés-de-skill-habit)
- [🖥 Plateforme de gestion](#-plateforme-de-gestion)
  - [🗂 Gestion des compétences](#-gestion-des-compétences)
  - [📊 Analyses](#-analyses)
  - [🛠 Paramètres](#-paramètres)
- [🌐 Support des plateformes](#-support-des-plateformes)
- [🤝 Contribution](#-contribution)
- [📄 Licence](#-licence)

---

## 🤔 Le problème

Vous avez installé de nombreuses compétences. Maintenant, chaque fois que vous tapez `/`, vous faites défiler toute la liste avant de pouvoir en utiliser une seule.

## 💡 La solution

skill-habit enregistre chaque compétence que vous invoquez (métadonnées uniquement — jamais le contenu de vos prompts).

À chaque démarrage de session, il reconstruit un préfixe de raccourci `/sh-*` avec vos meilleures compétences en tête, étiquetées dans la langue de votre choix.

Votre compétence la plus utilisée devient `/sh-<votre-compétence>`, celle que vous n'avez pas touchée depuis des semaines descend vers le bas.

La liste reflète vos compétences les plus utilisées, pas un ordre par défaut sans signification.

---

## ✨ Fonctionnalités

|     | Fonctionnalité                    | Description                                                                                                                                                                                                                                                                                   | Pris en charge sur |
| --- | --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ |
| 📊  | **Classement par fréquence**      | Les raccourcis sont réordonnés à chaque session selon l'utilisation réelle                                                                                                                                                                                                                    | Claude Code        |
| 📌  | **Épingler en haut**              | Forcer une compétence à toujours apparaître en premier, réordonner avec ↑↓                                                                                                                                                                                                                    | Claude Code        |
| 🔮  | **Prédiction par association**    | Suggère les compétences que vous enchaînez habituellement, basé sur votre historique complet                                                                                                                                                                                                  | Claude Code        |
| 🌡   | **Carte thermique d'activité**    | Grille style GitHub montrant votre utilisation des compétences ; plage de temps ajustable                                                                                                                                                                                                     | Claude Code        |
| 🕐  | **Modèles temporels**             | Répartition horaire et par jour de la semaine de vos moments de codage                                                                                                                                                                                                                        | Claude Code        |
| 📝  | **Gestion des compétences**       | Rechercher, trier et modifier les descriptions de toutes les compétences installées                                                                                                                                                                                                           | Claude Code        |
| 🚀  | **Vérification des mises à jour** | Vérifie les mises à jour automatiquement à chaque ouverture de l'interface ; distingue les versions majeures des versions correctives ; affiche les notes de changements en ligne et une bannière rouge persistante pour les mises à jour importantes ; mise à niveau ou fermeture en un clic | Claude Code        |
| 🚫  | **Liste noire**                   | Exclure des compétences spécifiques du classement par fréquence et des raccourcis ; à gérer depuis l'onglet Compétences                                                                                                                                                                       | Claude Code        |
| 🗂   | **Gestion des journaux**          | Suppression automatique des anciens enregistrements (30 jours par défaut) ; nettoyage par N jours ou suppression totale depuis l'interface                                                                                                                                                    | Tous               |
| 🌐  | **Interface multilingue**         | Tableau de bord en chinois, anglais, allemand, français, russe, coréen et japonais, détection automatique                                                                                                                                                                                     | Tous               |
| 🔒  | **Confidentialité avant tout**    | Enregistre uniquement le nom de la compétence, l'heure et l'identifiant de session — jamais le contenu de vos prompts                                                                                                                                                                         | Tous               |
| 🔧  | **Serveur à la demande**          | L'interface de gestion démarre quand vous en avez besoin, se ferme quand vous fermez l'onglet                                                                                                                                                                                                 | Tous               |


### 🔑 Préfixe de raccourci

Le **préfixe de raccourci** est l'espace de noms de tous les raccourcis générés par skill-habit — la valeur par défaut est `sh`. À chaque session, les raccourcis sont construits dans l'un ou les deux modes suivants (configurable) :

| Mode          | Format                        | Exemple (préfixe `sh`)    | Notes                                                                                                                                   |
| ------------- | ----------------------------- | ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| **Numérique** | `/<préfixe><N×rang>`          | `/sh1`, `/sh22`, `/sh333` | Trié par fréquence ; `/sh1` pointe toujours vers la compétence la plus utilisée ; prédiction par association mise à jour chaque session |
| **Commande**  | `/<préfixe>-<nom-compétence>` | `/sh-git-smart`           | Appeler les compétences directement par leur nom ; ordre du menu fixé alphabétiquement par Claude Code, indépendant de la fréquence     |

Allez dans **Paramètres → Général → Préfixe de raccourci**, saisissez une nouvelle valeur et enregistrez — les raccourcis se reconstruisent immédiatement. L'interface détecte les conflits en temps réel et affiche sous le champ des alternatives sans conflit sur lesquelles vous pouvez cliquer pour les appliquer.

**Règles de format :** lettres, chiffres, `-`, `_` uniquement ; 5 caractères maximum.

### 🔮 Prédiction par association (Ordre intelligent)

Lorsque `enable_sequence_prediction` est activé, à chaque démarrage de session le système :

1. Lit la dernière compétence que vous avez utilisée
2. Interroge la matrice de transition historique pour prédire les 3 prochaines compétences les plus probables
3. Propulse ces 3 compétences en tête de la liste de raccourcis

L'efficacité dépend du mode de raccourci :

| Mode                         | Effet                                                                                                                                                     |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Numérique** (`/sh1 /sh2…`) | La prédiction change directement quelle compétence occupe `sh1`/`sh2`. Taper `/sh1` exécute toujours la compétence recommandée. **Pleinement efficace.** |
| **Commande** (`/sh-<name>`)  | L'ordre du menu est fixé alphabétiquement par Claude Code — la prédiction **n'a aucun effet sur l'ordre du menu**.                                        |

> La précision s'améliore au fur et à mesure que les données s'accumulent. Les résultats sont significatifs après 20+ sessions.

### 📐 Ordre des raccourcis numériques

L'autocomplétion de Claude Code classe les suggestions principalement par **longueur totale du nom** — les noms plus courts obtiennent un score plus élevé et apparaissent en premier. skill-habit génère des raccourcis numériques avec des **longueurs de noms strictement croissantes** en répétant chaque chiffre de rang N fois :

| Rang                | Raccourci | Longueur     |
| ------------------- | --------- | ------------ |
| 1 (le plus utilisé) | `sh1`     | 2 caractères |
| 2                   | `sh22`    | 3 caractères |
| 3                   | `sh333`   | 4 caractères |
| 4                   | `sh4444`  | 5 caractères |
| 5                   | `sh55555` | 6 caractères |

Cela garantit que le menu déroulant affiche les raccourcis dans l'ordre de fréquence. Lorsque vos habitudes changent, les attributions se mettent à jour automatiquement au prochain démarrage de session.

Pour invoquer : tapez `/sh1` directement, ou `/sh2` (correspondance floue sur `sh22`) et appuyez sur Entrée.

### 🔒 Confidentialité

skill-habit **n'enregistre jamais** le contenu des prompts, les chemins de fichiers ou les noms de projets.

Les entrées du journal ressemblent à ceci (`~/.skill-habit/skill-usage.log`) :

```jsonc
{
  "v": 1,                    // version du schéma
  "ts": 1719360000,          // horodatage Unix
  "skill": "git-smart",      // nom uniquement — pas ce que vous avez tapé après
  "platform": "claude_code", // quel outil IA a invoqué la compétence
  "hour": 14,                // heure du jour (0–23)
  "weekday": 1,              // 0 = Lundi
  "session_id": "abc123",    // identifie une session de codage continue
  "session_skill_seq": 3,    // position dans la session (1, 2, 3…)
  "project_hash": "a3f2c1",  // hachage à sens unique, non réversible
  "args_len": 42             // nombre de caractères uniquement, jamais le contenu
}
```

Les entrées plus anciennes que `log_retention_days` (par défaut : 30) sont automatiquement supprimées à chaque session. Vous pouvez également nettoyer en entrant un nombre de jours (0 = tout effacer) depuis **Paramètres → Gestion des données**.

---

## 🚀 Démarrage rapide

> **Prérequis :** macOS ou Linux · Python 3.7+ · git
>
> **Windows :** Non pris en charge nativement. Utilisez [WSL](https://learn.microsoft.com/windows/wsl/) comme solution de contournement.

### Installation

**Option A — installation via plugin Claude Code (recommandé)**

```bash
# Étape 1 : Enregistrer le marketplace
claude plugins marketplace add kiss4u/skill-habit

# Étape 2 : Installer le plugin
claude plugins install skill-habit@skill-habit
```

Redémarrez Claude Code après l'installation — le suivi commence immédiatement.

> Un problème avec l'option A ? L'option B fonctionne exactement pareil — utilisez-la à la place.

**Option B — installation en une ligne**

```bash
curl -sSL https://raw.githubusercontent.com/kiss4u/skill-habit/main/scripts/bootstrap.sh | bash
```

> Installation par défaut dans `~/.claude/skills/skill-habit` (le répertoire est créé automatiquement s'il n'existe pas). Pour un chemin personnalisé : `SKILL_HABIT_INSTALL_DIR=/votre/chemin curl -sSL ... | bash`

**Option C — pipx / pip**

> Note : `skill-habit install` synchronise automatiquement les skills intégrés lors de son exécution — fonctionnellement identique aux options A / B.

pipx (recommandé — garde l'environnement isolé) :
```bash
pipx install git+https://github.com/kiss4u/skill-habit
skill-habit install
```

pip :
```bash
pip install git+https://github.com/kiss4u/skill-habit
skill-habit install
```

> Démarrez une nouvelle session Claude Code — le suivi commence immédiatement.

**Autres plateformes**

Cursor, Codex CLI, Gemini CLI et d'autres sont prévus. Consultez la section Contribution pour ajouter un adaptateur.

---

### Mise à niveau

Utilisez la même commande que pour l'installation — chaque méthode gère les mises à niveau automatiquement :

**Option A — Plugin Claude Code**

```bash
claude plugins update skill-habit@skill-habit
```

**Option B — en une ligne**

```bash
curl -sSL https://raw.githubusercontent.com/kiss4u/skill-habit/main/scripts/bootstrap.sh | bash
```

Relancer bootstrap sur une installation existante détecte le répertoire `.git` et exécute `git pull` au lieu de recloner.

**Option C — pipx / pip**

pipx :
```bash
pipx upgrade skill-habit
skill-habit install
```

pip :
```bash
pip install --upgrade git+https://github.com/kiss4u/skill-habit
skill-habit install
```

Vous pouvez également vérifier les mises à jour et effectuer une mise à niveau en un clic directement depuis le panneau **Paramètres → Version & Mise à niveau** dans l'interface de gestion.

---

### Désinstallation

**Option A — Plugin Claude Code**

```bash
/skill-habit:uninstall
```

**Option B — Commande unique**

```bash
/skill-habit:uninstall
```

> Vous serez invité à choisir si vous souhaitez également supprimer l'historique et la configuration (`~/.skill-habit`) — choisissez selon vos besoins.

**Option C — pipx / pip**

pipx :
```bash
skill-habit uninstall
pipx uninstall skill-habit
```

pip :
```bash
skill-habit uninstall
pip uninstall skill-habit
```

---

### Configuration

**Ouvrir l'interface de gestion**

Après l'installation, ouvrez le tableau de bord avec l'une de ces méthodes :

Dans Claude Code (Option A / B) :
```bash
/skill-habit:server
```

Ligne de commande (Option C — pipx / pip) :
```bash
skill-habit server
```


Le navigateur s'ouvre automatiquement. Le serveur se ferme après 5 minutes d'inactivité.

**config.json**

`~/.skill-habit/config.json` — modifiable dans l'interface ou directement :

```jsonc
{
  "prefix": "sh",                      // préfixe de raccourci : /sh-*
  "top_n": 10,                         // max raccourcis nommés générés par session
  "numeric_n": 5,                      // max raccourcis numériques générés (sh1…shN)
  "time_window": "all",                // "today" | "week" | "month" | "all"
  "shortcut_mode": "both",             // "numeric" (/sh1) | "command" (/sh-<name>) | "both"
  "enable_sequence_prediction": true,  // prédiction par association — voir note
  "prediction_n": 5,                   // max candidats à promouvoir (1–5)
  "top_skills_n": 10,                  // lignes dans le graphique Top Skills
  "pinned_skills": [],                 // toujours en premier, quelle que soit la fréquence
  "log_retention_days": 30,            // fenêtre glissante ; 0 = conserver indéfiniment
  "theme": "system",                   // "light" | "dark" | "system"
  "language": "auto",                  // "zh" | "en" | "de" | "fr" | "ru" | "ko" | "ja" | "auto"
  "analytics_cards": {                 // activer/désactiver les cartes individuellement
    "heatmap": true,                   // grille d'activité
    "top_skills": true,                // graphique de fréquence
    "transition_graph": true,          // patterns d'enchaînement
    "hourly_distribution": true,       // heures d'activité
    "weekday_distribution": true       // jours d'activité
  }
}
```

---

## Skills intégrés de skill-habit

Les skills de gestion suivants sont intégrés sous forme de plugin et toujours disponibles, quel que soit le préfixe :

| Skill                  | Description                                             | Quand l'utiliser                                                                                                                                            |
| ---------------------- | ------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/skill-habit:quick`   | Afficher le préfixe actuel et les raccourcis numériques | Préfixe ou correspondance oublié ? Ex. de sortie : `Préfixe : sh`, `/sh1 → git-smart`                                                                       |
| `/skill-habit:server`  | Ouvrir l'interface web de gestion dans le navigateur    | Modifier les paramètres, consulter les analyses, gérer les skills ; le navigateur s'ouvre automatiquement, le serveur s'arrête après 5 minutes d'inactivité. Relancer la commande redémarre le serveur (sans doublon) sur le même port fixe (5027 par défaut) ; port aléatoire en cas de conflit |
| `/skill-habit:rebuild`    | Reconstruire immédiatement les raccourcis               | Après édition manuelle de `~/.skill-habit/config.json` ; les changements sauvegardés via le Web UI déclenchent automatiquement un rebuild                   |
| `/skill-habit:version`    | Afficher la version installée                           | Confirmer la version lors d'un débogage ou d'un rapport de bug                                                                                              |
| `/skill-habit:uninstall`  | Désinstaller skill-habit | Détecte automatiquement la méthode d'installation, nettoie les hooks, raccourcis et données du plugin ; demande si l'historique et la configuration doivent également être supprimés |

---

## 🖥 Plateforme de gestion

### 🗂 Gestion des compétences

<a href="../assets/screenshot-skills.png"><img src="../assets/screenshot-skills.png" width="800" alt="Skills tab"></a>

Ouvrez l'onglet **Compétences** pour :

- **Rechercher & trier** — filtrer par nom/description ; trier par nombre d'utilisations, dernière utilisation ou nom (cliquer à nouveau sur le même bouton pour inverser)
- **Modifier les descriptions** — double-cliquer sur la description pour modifier en ligne (ou cliquer sur l'icône ✏️ au survol) ; Entrée ou clic ailleurs pour sauvegarder, Échap pour annuler
- **Épingler des compétences** — épingler une compétence pour la fixer en tête de vos raccourcis ; utiliser ↑↓ pour réordonner les compétences épinglées
- **Mettre en liste noire** — cliquer sur **Bloquer** sur n'importe quelle ligne pour exclure une compétence du classement par fréquence et des raccourcis ; gérer la liste noire (afficher, paginer, débloquer) dans la section Liste noire repliable en bas de l'onglet
- **Historique d'utilisation** — voir combien de fois vous avez utilisé chaque compétence et quand vous l'avez utilisée pour la dernière fois

> L'onglet Compétences affiche uniquement les compétences que vous avez utilisées au moins une fois. Les compétences proviennent de `~/.claude/skills/`, de tous les plugins installés, et des commandes personnalisées dans `~/.claude/commands/` (regroupées par espace de noms dans la section **Commands** en bas de page).

### 📊 Analyses

<a href="../assets/screenshot-analytics.png"><img src="../assets/screenshot-analytics.png" width="800" alt="Analytics tab"></a>

L'onglet **Analyses** comprend :

- **Carte thermique d'activité** — grille style GitHub ; chaque cellule = invocations ce jour-là ; plage de temps ajustable
- **Meilleures compétences** — graphique en barres pour la période sélectionnée (aujourd'hui / semaine / mois / tout le temps)
- **Distribution horaire** — à quel moment de la journée vous utilisez les compétences
- **Distribution par jour de la semaine** — les jours où vous codez le plus
- **Graphe de transitions** — quelles compétences vous enchaînez (alimente le modèle de prédiction)

Chaque carte peut être activée ou désactivée individuellement dans les Paramètres.

### 🛠 Paramètres

<a href="../assets/screenshot-settings.png"><img src="../assets/screenshot-settings.png" width="800" alt="Settings tab"></a>

L'onglet **Paramètres** couvre trois cartes, les modifications prennent effet immédiatement :

**Général**

| Paramètre                           | Description                                                                                                                                |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Préfixe de raccourci                | Espace de noms pour tous les raccourcis, défaut `sh` ; détecte les conflits en temps réel et suggère des alternatives sans conflit         |
| Fenêtre temporelle                  | Période pour le classement par fréquence : Tout / 6 derniers mois / Ce mois / Cette semaine / Aujourd'hui                                  |
| Mode de raccourci                   | Types de raccourcis à activer : numérique (`/sh1`), nommé (`/sh-name`) ou les deux                                                         |
| Nombre de raccourcis numériques     | Nombre maximum de raccourcis numériques générés (1–9)                                                                                      |
| Nombre de raccourcis nommés         | Nombre maximum de raccourcis nommés générés                                                                                                |
| Lignes du graphique top compétences | Nombre de compétences affichées dans le graphique Analytics                                                                                |
| Intervalle de reconstruction        | Minutes d'inactivité avant reconstruction automatique des raccourcis                                                                       |
| Prédiction de séquence              | Prédit la prochaine compétence probable et la remonte dans la liste                                                                        |
| Exclure soi-même des stats          | Activé : les invocations des commandes `skill-habit:*` ne sont pas comptées dans les statistiques (activé par défaut)                      |
| Profondeur de prédiction            | Combien de compétences la prédiction peut promouvoir (1–5)                                                                                 |
| Thème                               | Clair / Sombre / Système                                                                                                                   |
| Langue                              | Langue de l'interface : Auto / 中文 / English / Deutsch / Français / Русский / 한국어 / 日本語                                             |
| Bascules des cartes d'analyse       | Afficher/masquer individuellement : carte thermique, top compétences, graphe de transition, distribution horaire et par jour de la semaine |

**Gestion des données**

| Paramètre                      | Description                                                                                                            |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------- |
| Jours de conservation des logs | Fenêtre de conservation glissante (0 = conserver indéfiniment) ; nettoyage par nombre de jours ou suppression complète |

**Version & Mise à niveau**

| Statut                      | Comportement                                                                                    |
| --------------------------- | ----------------------------------------------------------------------------------------------- |
| Pas de mise à jour          | Vérification silencieuse, aucune notification                                                   |
| Mise à jour patch           | Notice ambrée dans cette carte uniquement — pas de bannière                                     |
| Mise à jour majeure/mineure | Bannière rouge en haut de la page avec notes de version ; mise à niveau en un clic ou fermeture |

---

## 🌐 Support des plateformes

| Plateforme     | Statut    |
| -------------- | --------- |
| Claude Code    | ✅ v0.0.1 |
| Cursor         | 🔜 prévu  |
| Codex CLI      | 🔜 prévu  |
| Gemini CLI     | 🔜 prévu  |
| GitHub Copilot | 🔜 prévu  |
| OpenCode       | 🔜 prévu  |
| Windsurf       | 🔜 prévu  |

---

## 🤝 Contribution

1. Forkez ce dépôt
2. Choisissez une plateforme dans `adapters/` (ou proposez-en une nouvelle)
3. Implémentez les trois méthodes dans `adapters/base.py`
4. Ouvrez une PR

---

## 📄 Licence

MIT © [kiss4u](https://github.com/kiss4u)
