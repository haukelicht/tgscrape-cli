import os
import re
import yaml
import json

# entities = '/Users/licht/switchdrive/Documents/work/phd/projects/identitarians/config/tgentities/patrioten_ch.yaml'
entities = '/Users/licht/Dropbox/py/tgscrape/tests/test_entities/chats.json'

def read_entities(entities: str, what: str, check_track=False) -> list:

    err_msg = f"cannot parse {what} entities from '{entities}'"
    assert isinstance(entities, str), err_msg + f": Argument passed to '{what}' is not a string"

    out = list()

    if os.path.isfile(entities):

        if re.search(r'\.yaml$', entities):
            try:
                with open(entities, 'r') as f:
                    data = yaml.load(f, Loader=yaml.FullLoader)
                    f.close()
            except yaml.scanner.ScannerError as e:
                raise ImportError(err_msg + ': Cannot read YAML file!')

        if re.search(r'\.json$', entities):
            try:
                with open(entities, 'r') as f:
                    data = json.load(f)
                    f.close()
            except json.decoder.JSONDecodeError as e:
                raise ImportError(err_msg + ': Cannot read JSON file!')

        for record in data:
            if what in record.keys():
                if check_track:
                    if 'track' in record:
                        if record['track']:
                            out.append(record[what])
                else:
                    out.append(record[what])

    else:
        try:
            out = [e.strip() for e in re.split(r',', entities)]
        except Exception as e:
            raise TypeError(err_msg + ': ' + type(e))

    return out
