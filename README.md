# Examen BentoML Killian KOPP

repo GitHub : https://github.com/karned-formation/datascientest-mlops-bentoml-examen

## Lancement du docker

Pour lancer le docker, créez un script bash et exécutez-le (en lui donnant les droits au préalable)
Le fichier de test est prévu pour se lancer sur le port 3006 si vous modifiez ce port, il faudra également le modifier dans le fichier de test.
```bash
#!/bin/bash

IMAGE_NAME=kopp_lr
PORT=3006

docker load -i bento_image.tar
docker run -d -p $PORT:3000 --name $IMAGE_NAME $IMAGE_NAME
```

## Test de l'API

Pour tester l'API, vous pouvez utiliser le fichier test_api.py.
Positionnez-vous dans le dossier src et exécutez les commandes suivantes
```bash
python3 -m venv kopp_lr
source kopp_lr/bin/activate
pip intall pytest
pip install requests
pytest -v
```

## informations
- les informations de connexion sont "user123/password123"
- en production, il ne faudrait pas les faire apparaître en clair dans le code
- en production, il ne devrait pas y avoir de token dans les tests
- en production, il ne devrait pas y avoir de mot de passe en clair dans les tests
- je n'arrive pas à obtenir une erreur 401 en retour avec un mauvais mot de passe
  - j'ai essayé un middleware sans succès
  - j'ai essayé diverses exceptions de divers modules sans succès
  - j'ai essayé un retour JSON sans succès
  - si vous avez une idée, je suis preneur !
  - le code du cours ne fonctionne pas non plus
  - le test détecte une erreur 500 au lieu de l'erreur 401