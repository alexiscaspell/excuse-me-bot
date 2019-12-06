

import json
import datetime

def encoder(o):
    if isinstance(o, datetime.datetime):
        return o.strftime("%Y-%m-%dT%H:%M:%SZ")
    elif isinstance(o, datetime.date):
        return o.strftime("%Y-%m-%d")
    # elif isinstance(o, (decimal.Decimal, ObjectId)):
    #     return str(o)
    elif hasattr(o.__class__, 'to_dict') and callable(getattr(o.__class__, 'to_dict')):
        return o.to_dict()
    else:
        try:
            return dict(o)
        except Exception as e:
            return str(o)

def decoder(some_class):
    def func(o):
        # if type(some_class)==type(datetime.datetime):
        #     return datetime.datetime.strptime(o,"%Y-%m-%dT%H:%M:%SZ")
        # elif type(some_class)==type(datetime.date):
        #     return datetime.datetime.strptime(o,"%Y-%m-%d")
        if type(o.__class__) is not type(dict):
            o = json.loads(o)

        if some_class is dict:
            return o
        else:
            # class_module = getattr(obj, '__module__', None)
            # class_name = f"{some_class.__name__}"
            try:
                # return getattr(class_module, class_name)(object_dict)
                return some_class(o)
            except Exception as e:
                return some_class(**o)

    return func

def to_json(o)->str:
    return json.dumps(o,default=encoder)

def from_json(o,return_class=dict):
    dict_json = json.loads(o)
    converter = decoder(return_class)

    if type(dict_json.__class__) is list:
        return [converter(e) for e in dict_json]
            
    return converter(dict_json)
    # return json.loads(dict_json,object_hook=decoder(return_class))
    # return json.loads(dict_json,object_hook=decoder(return_class))