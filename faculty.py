"""
Load the faculty.csv file as VIVO Faculty Members.

See VCard usage:
https://wiki.duraspace.org/display/VIVO/VCard+usage+diagram

"""

import csv
import json
import sys

import logging
logging.basicConfig(level=logging.INFO)

from rdflib import Graph
from utils import ns_mgr

#Data namespace
ns = "http://vivo.school.edu/individual/"

faculty_ctx = {
    "@context": {
        "@base": ns,
        "a": "@type",
        "uri": "@id",
        "vivo": "http://vivoweb.org/ontology/core#",
        "vcard": "http://www.w3.org/2006/vcard/ns#",
        "obo": "http://purl.obolibrary.org/obo/",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "FacultyMember": "vivo:FacultyMember",
        "label": "rdfs:label",
        "first": "vcard:givenName",
        "last": "vcard:familyName",
        "middle": "vivo:middleName",
        "title": "vcard:title",
        "contact": {
            "@id": "obo:ARG_2000028",
            "@type": "@id",
            "label": "has contact info"
        },
        "vcard:hasName":
            {
            "@id": "vcard:hasName",
            "@type": "@id"
        },
        "vcard:hasTitle":
            {
            "@id": "vcard:hasTitle",
            "@type": "@id"
        },
        "vcard:hasEmail":
            {
            "@id": "vcard:hasEmail",
            "@type": "@id"
        }
    }
}

fac = []

with open(sys.argv[1]) as infile:
    for count, row in enumerate(csv.DictReader(infile)):
        pid = row.get('UID')

        person_uri = 'person-' + pid

        #Our faculty dictionary
        f = {}

        #URI will be person_id plus person prefix.
        f['uri'] = person_uri
        f['a'] = "FacultyMember"
        f['label'] = row.get('FullName')

        #Individual vcard
        vcard_uri = person_uri + '-vcard'
        f['contact'] = vcard_uri
        #Name vcard.
        vcard_name_uri = person_uri + '-vcard-name'
        #Title vcard
        vcard_title_uri = person_uri + '-vcard-title'
        #Email vcard
        vcard_email_uri = person_uri + '-vcard-email'


        #Main Vcard
        vc = {}
        vc['uri'] = vcard_uri
        vc['a'] = 'vcard:Individual'
        vc['vcard:hasName'] = vcard_name_uri
        vc.update(faculty_ctx)
        fac.append(vc)

        n = {}
        n['uri'] = vcard_name_uri
        n['a'] = 'vcard:Name'
        n['first'] = row.get('FirstName')
        n['last'] = row.get('LastName')
        middle = row.get('MidName')
        if middle != "":
            n['middle'] = middle
        n.update(faculty_ctx)
        fac.append(n)

        #Title
        t = {}
        t['uri'] = vcard_title_uri
        t['a'] = "vcard:Title"
        t['title'] = row.get('Title')
        vc['vcard:hasTitle'] = vcard_title_uri
        t.update(faculty_ctx)
        fac.append(t)

        #Email
        email = row.get('Email')
        if email != '':
            e = {}
            e['a'] = "vcard:Email"
            e['a'] = "vcard:Work"
            e['uri'] = vcard_email_uri
            e['vcard:email'] = email
            vc['vcard:hasEmail'] = vcard_email_uri
            e.update(faculty_ctx)
            fac.append(e)

        f.update(faculty_ctx)
        fac.append(f)

raw_jld = json.dumps(fac)
g = Graph().parse(data=raw_jld, format='json-ld')
g.namespace_manager = ns_mgr
print g.serialize(format='turtle')



