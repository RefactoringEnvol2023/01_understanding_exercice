# Message In A Bottle

# Contexte

Le système est pensé pour des acquisitions en milieu difficile d'accès et avec des capteurs de capacité limitée.
Il regroupe les mesures de capteurs pour les stocker dans une mémoire.

## Les capteurs 

* Démarre une acquisition de données
** Uniquement si il est status IDLE
** et les stock dans sa petite mémoire
* Arrête une acquisition de données
* Fournie et libère ses données une à une sur demande

## Les mémoires

La mémoire a une valeur seuil qui est estimée sur le ratio nombre d'éléments sur nombre d'éléments maximal.


## Le runner

Le runner commande l'acquisition des données.

* Il lance une acquisition
* Dès qu'elle est terminée,
** il vérifie l'état de l'acquisition 
** il transfère l'acquisition dans la mémoire.
* Si l'acquisition est vide, le processus s'arrête

* Exceptions
** Si la capteur n'est pas au repos, il lève une exception
** Si la mémoire dépasse une certaine capacité limite, il lève une exception
** Si l'acquisition n'est pas faite après que le capteur a terminé, il lève une exception
** Si l'acquisition n'est pas valide, il lève un exception

## Objectifs

### Donner des noms correctes

### Scinder la boucle  
