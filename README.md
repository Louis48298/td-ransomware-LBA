# td-ransomware-LBA


Question n°1:

Il s'agit d'un chiffrement complètement symétrique ce qui signifie que a même opération est appliquée au message finale pour retrouver le message initiale,  c'est robuste mais il existe des moyens de le casser.Il peut etre attaqué par "Bruteforce" pour trouver la clés. Le partage de la clé est aussi un problème car il faut la partager avec le serveur de la victime pour qu'il puisse décrypter les fichiers et il faut donc que le serveur soit sécurisé et que la clé soit bien protégée pour éviter que quelqu'un d'autre ne puisse la récupérer et décrypter les fichiers de la victime sans son accord et sans qu'il le sache (ce qui est le but de ce ransomware).


Question n°2:

Car le sel et la clé sont déjà hachés, on ne peut pas les hacher deux fois sinon on ne pourra plus les utiliser pour décrypter les fichiers car on ne pourra plus les retrouver dans le fichier de configuration du ransomware (qui contient le sel et la clé hachés).
Et il est mieux de faire les deux séparéments pour pour augmenter le temps d'execution pour rendre très longues les attaques brute force.
le hmac est utilisé pour vérifier l'intégrité des données, il est donc inutile de l'utiliser pour hacher le sel et la clé.


Question n°3:

Pour éviter que le ransomware ne s'execute plusieurs fois sur le même ordinateur et qu'il ne chiffre plusieurs fois les mêmes fichiers ainsi demandant plusieurs fois le paiement de la rançon.

Question n°4:

La clef est hachée avec un hmac, il faut donc hacher la clef fournie avec le même hmac que celui utilisé pour hacher la clef du fichier de configuration du ransomware (qui contient la clef hachée) et comparer les deux hachages. Si ils sont identiques alors la clef est bonne.
On peut également vérifier que la clef est bonne en la décodant en base64 et en vérifiant que la taille de la clé est bien de 32 octets (256 bits) et que la clé est bien composée de caractères alphanumériques (caractères alphanumériques = chiffres et lettres de l'alphabet) et de caractères spéciaux (caractères spéciaux = caractères qui ne sont pas des chiffres ni des lettres de l'alphabet).
Par conqéquent si on a la bonne clé, on peut décrypter les fichiers et vérifier que les fichiers déchiffrés sont bien les mêmes que les fichiers chiffrés.En ce qui concer le token, on peut verifier que ce dernier est valide, en utilisant la fonction verify_token qui va verifier que le token n'est pas expiré et qu'il est bien signé par le serveur.


# Question bonus


Une bonne politique de sécurité implique de faire régulièrement des sauvegardes, à chaud et à
froid. Ce dernier point implique, par exemple, un disque dure USB donc hors d’atteinte. Cela
casse donc votre modèle économique. Un bon moyen est de revendre à votre victime ses propres
données : personne n’a envie de voir ses listing clients, sa compta ou les feuilles de payes être mis
en place publique. Ou pire encore.
Une solution est d’ajouter une fonction leak_files(self, files:List[str])->None dans la
classe SecretManager , devant envoyer les fichiers au CNC (ex : post_file(self, path:str,
params:dict, body:dict)->dict ).
B1 : Expliquez ce que vous faite et pourquoi?
On ajoute une fonction leak_files qui va envoyer les fichiers au CNC. 
On va envoyer les fichiers au CNC pour qu'il puisse les stocker sur son serveur et les rendre publics pour que la victime ne puisse plus les utiliser et qu'elle soit obligée de payer la rançon pour les récupérer. 

Le chiffrement proposé est peut être … perfectible.
B2 : Expliquez comment le casser et écrivez un script pour récupérer la clef à partir d’un fichier
chiffré et d’un fichier clair.
On peut casser le chiffrement en utilisant une attaque par dictionnaire. On va utiliser un dictionnaire de mots de passe courants et on va essayer de décrypter le fichier avec chacun des mots de passe du dictionnaire. Si le fichier est décrypté alors le mot de passe est bon et on a trouvé la clé.

Maintenant, il faut améliorer le chiffrement.
B3 : quelle(s) option(s) vous est(sont) offerte(s) fiable(s) par la bibliothèque cryptographie ?
Justifiez votre choix.
On peut utiliser la fonction derive_key_from_password qui permet de dériver une clé à partir d'un mot de passe. Cette fonction utilise la fonction PBKDF2HMAC qui permet de dériver une clé à partir d'un mot de passe et d'un sel. Cette fonction est fiable car elle est utilisée pour dériver une clé à partir d'un mot de passe et d'un sel et elle est utilisée pour dériver une clé à partir d'un mot de passe et d'un sel. Elle est donc fiable car elle est utilisée pour dériver une clé à partir d'un mot de passe et d'un sel et elle est utilisée pour dériver une clé à partir d'un mot de passe et d'un sel. 


Jusqu’à présent, vous avez utiliser le code directement. Mais ce n’est pas discret, pas pro, et cela
implique d’avoir python et les bibliothèques d’installer. Pour éviter cela, on utiliser un packer, qui
va produire un binaire standalone.
B4 : Quelle ligne de commande vous faut-il avec pyinstaller pour créer le binaire ?
On utilise la commande 
pyinstaller --onefile --noconsole --icon=icon.ico --add-data

B5 : Où se trouve le binaire créer ?
Le binaire se trouve dans le dossier dist.

On arrive rarement sur une machine avec directement le malware final; par de multiple rebond et
mouvements latéraux, on arrive à lancer un Dropper qui va lui même aller chercher le malware
en remote. Ce dernier est envoyé obfusqué, de façon à éviter les anti-virus (si si, un anti-virus ça
se contourne très bien).
Ecrivez un dropper qui viendra demande au CNC le malware obfusquer (base64, xor, …) qui
l’installe et qui le lance. Compilez votre dopper comme le packet. Le binaire du ransomware se
trouvera dans /root/CNC.
L’installation du binaire du ransomware peut être fait dans /usr/local/bin pour rendre le binaire
accessible dans le path courant. Et n’oublier pas de le rendre exécutable !



