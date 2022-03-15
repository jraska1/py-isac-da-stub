import os.path
import fnmatch
from lxml import etree

DASTA_V4_NAMESPACES = {
    'ds':   'urn:cz-mzcr:ns:dasta:ds4:ds_dasta',
    'dsip': 'urn:cz-mzcr:ns:dasta:ds4:ds_ip',
    'ido':  'urn:cz-mzcr:ns:dasta:ds4:ds_ido',
}

messages = {
}

if __path__:
    for fn in os.listdir(__path__[0]):
        full_path = os.path.join(__path__[0], fn)
        if fnmatch.fnmatch(fn, "*.xml"):
            full_path = os.path.join(__path__[0], fn)
            doc = etree.parse(full_path)
            ip = doc.find("./ds:is/dsip:ip", namespaces=DASTA_V4_NAMESPACES)
            if ip is not None:
                id_pac = ip.attrib.get('id_pac')
                if id_pac:
                    messages[id_pac] = full_path
                for ku_z in ip.findall("./dsip:ku/dsip:ku_z", namespaces=DASTA_V4_NAMESPACES):
                    idku = ku_z.attrib.get('idku')
                    if idku:
                        messages[idku] = full_path
                for ku_z in ip.findall("./dsip:ku/dsip:ku_z/dsip:ku_z_soupis/dsip:ku_z_soupis_u", namespaces=DASTA_V4_NAMESPACES):
                    idku = ku_z.attrib.get('idku')
                    if idku:
                        messages[idku] = full_path
            else:
                zzs = doc.find("./ds:is/ido:ido/ido:zzs_vl_z", namespaces=DASTA_V4_NAMESPACES)
                if zzs is not None:
                    messages['beds'] = full_path
        elif fnmatch.fnmatch(fn, "*.json"):
            messages[os.path.splitext(fn)[0]] = full_path
