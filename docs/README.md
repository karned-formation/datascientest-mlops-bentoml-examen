# Bentoml

```
bentoml serve service:lr_service --reload --port 3005
bentoml containerize lr_service:latest
docker save -o bento_image.tar kopp_lr_service
```
