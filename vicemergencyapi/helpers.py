import json


# Why?
# Some floats in the JSON are encoded as strings!
class Decoder(json.JSONDecoder):

    def decode(self, s):
        result = super().decode(s)
        return self._decode(result)

    def _decode(self, o):
        if isinstance(o, str):

            # Check if o contains a decimal point and tryparse as float
            if '.' in o:
                try:
                    return float(o)
                except:
                    return o

            try:
                return int(o)
            except:
                pass

            return o

        elif isinstance(o, dict):
            return {k: self._decode(v) for k, v in o.items()}
        elif isinstance(o, list):
            return [self._decode(v) for v in o]
        else:
            return o
