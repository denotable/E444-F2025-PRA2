# E444-F2025-PRA2
This repo is a clone of [https://github.com/miguelgrinberg/flasky](https://github.com/miguelgrinberg/flasky).

### Notes
This project utilizes Bootstrap 5 instead of Bootstrap 3 to ensure compatibility with newer versions of Python 3 and Flask.

### Docker Build Instructions
#### Step 1 (Build)
```docker build -t flasky .```

#### Step 2 (Run)
```
docker run --rm \
  -e FLASK_APP=hello.py \
  -e FLASK_RUN_HOST=0.0.0.0 \
  -e FLASK_RUN_PORT=5050 \
  -p 5001:5050 \
  --name flasky1 \
  flasky
  ```

