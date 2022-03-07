# Lettres

Thanks to [Stealthix](https://stealthix.itch.io/) for the tilesets used in this game! And thanks to [Graven - 
Développement](https://www.youtube.com/c/Gravenilvectuto/videos)  for the tutorials 
([1](https://www.youtube.com/watch?v=ooITOxbYVTo) and [2](https://www.youtube.com/watch?v=clcmhmpyYSc&t=3162s))
which help us a lot to start this game :)

> ### Installation
Soit vous avez git, dans ce cas un petit ***git clone***, autrement faudra télécharger le ***.zip***, puis faudra sans 
doute utiliser ***pip install pygame***,
***pip install pytmx*** et ***pip install pyscroll*** qui sont des packages pas présents par défaut (je crois). Après,
un simple ***python main.py*** et le jeu se lancera :) 

> ### Commandes
- Déplacement: flèches directionnelles ou ZQSD (ZQSD est préférable au vu des autres touches).
- Interactions avec les PNJ, objets, portes fermées, panneaux, ... : touche espace.
- Inventaire: E (les touches à utiliser dans l'inventaires sont spécifiées dans le jeu).
- Dans le magasin: les touches de 1 à 0 au dessus du clavier pour acheter (attention à n'appuyer qu'une fois,
autrement en cas de spam de touche vous payerez plusieurs objets (c'est assez sensible)).
- Le monocycle du magasin roule vite: pareil que pour se déplacer, et pour l'activer/le désactiver,
il faut l'utiliser dans l'inventaire (il ne disparaîtra pas contrairement aux autres objets).

> ### Conseils
- Le jeu devrait être stable, mais sauvegarder de temps en temps (à faire quand on est dans l'inventaire),
semble être une bonne idée, on ne sait jamais ^^'
- Les premiers panneaux du jeu expliquent le scénario.
- Pour gagner, il faut réunir les 9 parchemins (en réussissant les quêtes et en battant les 3 boss).
- On est coquins donc on a caché des objets derrières des éléments de décors :3
- Certaines quêtes étaient prévues pour être exécutées en "live", mais le jeu peut se terminer quand même:
une fois la TV allumée, appuyez sur "=", puis espace pour l'éteindre; parlez à Thib vous donnent directement un parchemin.
- Lors des combats, commencez par appuyer sur la touche espace, puis A pour attaquer (puis les touches de 1 à 4
au dessus du clavier pour choisir l'attaque), ou E pour fuir (plus les monstres ont un niveau élevé,
moins vous avez de chance de vous échapper); nous n'avons pas implémenté les objets en combats.
- Les monstres sont de plus en plus fort au fur à mesure des mondes.
- Vous pouvez marcher sur la glace.
- En combat, le texte avec les noms, HP et LVL change de couleur en fonction du status:
  - Noir: aucun status particulier;
  - Mauve: empoisonné (dégâts sur la durée); 
  - Orange: brûlé (dégâts sur la durée (moindre que pour le poison) et moins de dégâts infligés));
  - Jaune: paralysé (des chances de ne pas pouvoir attaquer);
  - Bleu: cerveau gelé (entre un et trois tours en incapacité d'attaquer);
  - Gris: coma (pareil que gelé)).
- Utiliser les sachets d'or, les trésors ou le diamant dans l'inventaire ajoute direct des sous dans la bourse.
- Les quêtes de Chloé et Andréas se réalisent lorsqu'on vient leur parler avec un certain objet dans l'inventaire:
leurs lignes de dialogues changeront alors, et vous obtiendrez un parchemin.
- Le parchemin acheté au magasin reste dans l'inventaire mais n'est pas utilisable.

> ### Attaques
Lorsque le terme "possibilité" est utilisé ci-dessous, c'est qu'il y a une chance aléatoire que l'événement en question
se fasse, mais flemme de détailler plus les attaques au niveau de leur puissance héhé!

Par ailleurs, si le status d'un belligérant n'est pas neutre, alors il ne pourra être changé.

La chance est une stat permettant d'esquiver des attaques; la vitesse indique qui attaquera en premier, l'AD est relatif 
aux attaques physiques, l'AP à celles magiques, avec l'armor et la RM les résistances respectivement liées; 
HP = points de vie.

- Quichon tactique: dégâts magiques (DM).
- Lancer de gobelet: dégâts physiques (DP).
- Jus du Coq: DM + possiblilité d'empoisonner.
- Eyes contact: possibilité de paralyser.
- Affond de trop: possibilité d'endormir.
- Bagarre en Carolo: DP avec dégâts collatéraux.
- Glissade alcoolisée: DM collatéraux + la stat magique monte beaucoup.
- Non habes: si réussie, tue en un coup.
- Bière trop froide: DM + possibilité de geler.
- Dynamogifle: DP + possibilité de brûler.
- Patate de forain: DP.
- Coma éthylique: endort la cible.
- OH DJADJA: DM.
- Blanc de blanc: DM + possibilité d'empoisonner.
- Balayette: DP (en fonction des HP également).
- Danse sur le podium: DM.
- Je t'aime <3: DM + la chance de la source augmente.
- Lance-caca: DP.
- Chante faux: DM + baisse l'AD et la RM de la cible.
- Sieste stratégique: soigne tous les HP et change le status en sommeil.
- Pils chaude: augmente l'armor et la RM.
- Spéciale tempérée: augmente l'armor, la RM et l'AP.
- Une bonne Trappiste: augmente l'armor, la RM, l'AP et l'AD.
- Billet de 10 par terre: augmente la chance.
- Sol trop humide: baisse la vitesse de l'adversaire.
- Bibitive: augmente la vitesse de la source et sa chance.
- Estafette: augmente les HP et l'AD.

