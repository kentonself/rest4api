# rest4dict

For systems with the command line tool dict installed, rest4dict adds a REST API service.

## Requirements

1. dict available on the path
2. Python

# 

rest4dict is built on top of flask in python. 

```
export FLASK_APP=rest4dict.py

flask run
```

By default it runs on the localhost on port 5000. Port and host can be set with
```
flask run --host=0.0.0.0 --port=8123
```

## API calls:

The endpoint is /api/dict 
Input fields are source, target, and word. Source and target are two-letter language codes (en,es,it, etc.) and word is the word to be translated.
On successful return, the xlation contains the definition of the word.

## Test

A test.py script is provided which shows some examples.

## License

GNU GENERAL PUBLIC LICENSE

## TODO

- Clean up two2three so the pylint can call out mutliple-statements (C0321)
- Handle the cases where the lookup fails better. Catch the "did you mean" output and return it.

## Contribution

Please submit pull requests! Before doing so, make sure the test.py passes, and run pylint until it shows 10/10



