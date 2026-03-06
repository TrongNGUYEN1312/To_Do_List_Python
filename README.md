#  Application To-Do List (Gestionnaire de Tâches)

<img width="1912" height="1010" alt="Screenshot 2026-03-06 122016" src="https://github.com/user-attachments/assets/1d02ae10-cb69-44fb-b68a-91aa9b3a8a57" />

##  À propos du projet

Dans le cadre de notre apprentissage et de notre passion pour le développement logiciel, nous avons conçu cette application **To-Do List**. Bien qu'il existe de nombreuses applications de gestion de tâches, notre objectif était de créer un outil de bureau léger, sans dépendances complexes, et fonctionnant de manière totalement autonome.

**Pourquoi ce projet ?**
* **Simplicité :** Une interface épurée construite avec `tkinter` pour une prise en main immédiate.
* **Fiabilité :** Un système de sauvegarde locale via un fichier texte (`Liste_Tache.txt`) garantit que vos données ne sont jamais perdues, même si vous fermez l'application accidentellement.
* **Praticité :** L'intégration de fonctionnalités avancées, comme le système d'annulation (Undo) avec la touche `Ctrl+Z` et la gestion des priorités, offre une expérience utilisateur très fluide.

Il représente une excellente mise en pratique des concepts d'interface utilisateur (GUI), de la gestion des événements et de la manipulation de fichiers en Python.

##  Fonctionnalités

* ** Ajouter une tâche :** Saisissez une tâche et ajoutez-la à la liste (bouton ou touche `Entrée`).
* ** Supprimer une tâche :** Suppression sécurisée avec une boîte de dialogue de confirmation (bouton ou touche `Suppr`).
* ** Suivi de l'état :** Marquez vos tâches comme "Terminées" ou remettez-les "En cours" (Reprendre).
* ** Gestion des priorités :** Mettez en avant les tâches urgentes (couleur rouge et astérisque) ou remettez-les en statut normal.
* ** Annulation (Undo) :** Vous avez fait une erreur ? Annulez votre dernière action grâce à l'historique intégré (bouton ou raccourci `Ctrl+Z`).
* ** Sauvegarde automatique :** Les tâches sont enregistrées dans un fichier `Liste_Tache.txt` à chaque modification.

##  Technologies utilisées

* **Langage :** Python 
* **Interface Graphique :** `tkinter` (bibliothèque standard Python)
* **Système :** Module `os` pour la gestion des fichiers locaux.

##  Installation et Utilisation

Comme l'application utilise `tkinter` qui est inclus par défaut avec Python, vous n'avez besoin d'installer aucune bibliothèque externe.

