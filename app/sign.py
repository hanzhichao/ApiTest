import hashlib
import json

def sha1(str):
    m = hashlib.sha1()
    m.update(str.encode('utf8'))
    return m.hexdigest()

def sign_params(access_id, access_key, params):
    def _link(params):
        if isinstance(params, dict):
            params = [params]

        _str = ''
        for param in params:
            for k in sorted(param.keys()):
                v = param[k]
                _str = _str + _sort(v) if isinstance(v, dict) or isinstance(v, list) else _str + k + str(v)             
        return _str

    sign = sha1(_link(params) + access_key).upper()
    return [{"appid": access_id, "sign": sign, "auth-type":0}, params]