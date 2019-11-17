#
# This file is part of pyasn1-modules software.
#
# Created by Russ Housley
# Copyright (c) 2019, Vigil Security, LLC
# License: http://snmplabs.com/pyasn1/license.html
#

import sys
import unittest

from pyasn1.codec.der.decoder import decode as der_decoder
from pyasn1.codec.der.encoder import encode as der_encoder

from pyasn1_modules import pem
from pyasn1_modules import rfc2985
from pyasn1_modules import rfc3125


class SignaturePolicyTestCase(unittest.TestCase):
    pem_text = """\
MIIMYzALBglghkgBZQMEAgEwggwwBgorgR6RmYQFAQICGA8yMDE2MTAwMjAwMDAwMFowgaSk
XjBcMQswCQYDVQQGEwJTSzETMBEGA1UEBwwKQnJhdGlzbGF2YTEiMCAGA1UECgwZTmFyb2Ru
eSBiZXpwZWNub3N0bnkgdXJhZDEUMBIGA1UECwwLU2VrY2lhIElCRVCGQmh0dHA6Ly9lcC5u
YnVzci5zay90cnVzdGVkX2RhdGEvMjAxNjEwMDIwMDAwMDB6c2lnbmF0dXJlcG9saWN5LmRl
cgyBz0VOOiBFbC4gc2lnbmF0dXJlL3NlYWwsIG9wdGlvbmFsIGVsLiB0aW1lLXN0YW1wIG92
ZXIgT0NTUCwgYWNjb3JkaW5nIHRvIFJlZ3VsYXRpb24gKEVVKSBObyA5MTAvMjAxNC4gU0s6
IEVsLiBwb2RwaXMvcGXEjWHFpSwgdm9saXRlxL5uw6EgZWwuIMSNYXNvdsOhIHBlxI1pYXRr
YSBuYWQgT0NTUCwgcG9kxL5hIG5hcmlhZGVuaWEgKEXDmikgxI0uIDkxMC8yMDE0LjCCCpYw
IhgPMjAxNjEwMDIwMDAwMDBaGA8yMDIxMTAwMjAwMDAwMFowggpsoD8wPTA3MC4GCSqGSIb3
DQEJAwYJKoZIhvcNAQkEBgkqhkiG9w0BCQUGCyqGSIb3DQEJEAIvMAChAwoBAjACMACiEjAQ
ow4wDAIBAAIBAAIBAAIBAaSCChMwggoPoIIB/zCCAfswCwYJYIZIAWUDBAIBMAsGCWCGSAFl
AwQCAjALBglghkgBZQMEAgMwCwYJYIZIAWUDBAIGMAsGCWCGSAFlAwQCCDALBglghkgBZQME
AgkwCwYJYIZIAWUDBAIKMA8GCWCGSAFlAwQDAgICCAAwDwYJYIZIAWUDBAMDAgIIADAPBglg
hkgBZQMEAwQCAggAMA8GCWCGSAFlAwQDBgICCAAwDwYJYIZIAWUDBAMHAgIIADAPBglghkgB
ZQMEAwgCAggAMA4GCCqGSM49BAMCAgIBADAOBggqhkjOPQQDAwICAQAwDgYIKoZIzj0EAwQC
AgEAMA8GCWCGSAFlAwQDCgICAQAwDwYJYIZIAWUDBAMLAgIBADAPBglghkgBZQMEAwwCAgEA
MA8GCSqGSIb3DQEBCwICCAAwDwYJKoZIhvcNAQEMAgIIADAPBgkqhkiG9w0BAQ0CAggAMA8G
CWCGSAFlAwQDDgICCAAwDwYJYIZIAWUDBAMPAgIIADAPBglghkgBZQMEAxACAggAMA8GCSqG
SIb3DQEBCgICCAAwDwYJKoZIhvcNAQEBAgIIADANBgcqhkjOPQIBAgIBADAOBggrJAMDAgUC
AQICAQAwDgYIKyQDAwIFBAQCAgEAMA4GCCskAwMCBQQFAgIBADAOBggrJAMDAgUEBgICAQCh
ggH/MIIB+zALBglghkgBZQMEAgEwCwYJYIZIAWUDBAICMAsGCWCGSAFlAwQCAzALBglghkgB
ZQMEAgYwCwYJYIZIAWUDBAIIMAsGCWCGSAFlAwQCCTALBglghkgBZQMEAgowDwYJYIZIAWUD
BAMCAgIIADAPBglghkgBZQMEAwMCAggAMA8GCWCGSAFlAwQDBAICCAAwDwYJYIZIAWUDBAMG
AgIIADAPBglghkgBZQMEAwcCAggAMA8GCWCGSAFlAwQDCAICCAAwDgYIKoZIzj0EAwICAgEA
MA4GCCqGSM49BAMDAgIBADAOBggqhkjOPQQDBAICAQAwDwYJYIZIAWUDBAMKAgIBADAPBglg
hkgBZQMEAwsCAgEAMA8GCWCGSAFlAwQDDAICAQAwDwYJKoZIhvcNAQELAgIIADAPBgkqhkiG
9w0BAQwCAggAMA8GCSqGSIb3DQEBDQICCAAwDwYJYIZIAWUDBAMOAgIIADAPBglghkgBZQME
Aw8CAggAMA8GCWCGSAFlAwQDEAICCAAwDwYJKoZIhvcNAQEKAgIIADAPBgkqhkiG9w0BAQEC
AggAMA0GByqGSM49AgECAgEAMA4GCCskAwMCBQIBAgIBADAOBggrJAMDAgUEBAICAQAwDgYI
KyQDAwIFBAUCAgEAMA4GCCskAwMCBQQGAgIBAKKCAf8wggH7MAsGCWCGSAFlAwQCATALBglg
hkgBZQMEAgIwCwYJYIZIAWUDBAIDMAsGCWCGSAFlAwQCBjALBglghkgBZQMEAggwCwYJYIZI
AWUDBAIJMAsGCWCGSAFlAwQCCjAPBglghkgBZQMEAwICAggAMA8GCWCGSAFlAwQDAwICCAAw
DwYJYIZIAWUDBAMEAgIIADAPBglghkgBZQMEAwYCAggAMA8GCWCGSAFlAwQDBwICCAAwDwYJ
YIZIAWUDBAMIAgIIADAOBggqhkjOPQQDAgICAQAwDgYIKoZIzj0EAwMCAgEAMA4GCCqGSM49
BAMEAgIBADAPBglghkgBZQMEAwoCAgEAMA8GCWCGSAFlAwQDCwICAQAwDwYJYIZIAWUDBAMM
AgIBADAPBgkqhkiG9w0BAQsCAggAMA8GCSqGSIb3DQEBDAICCAAwDwYJKoZIhvcNAQENAgII
ADAPBglghkgBZQMEAw4CAggAMA8GCWCGSAFlAwQDDwICCAAwDwYJYIZIAWUDBAMQAgIIADAP
BgkqhkiG9w0BAQoCAggAMA8GCSqGSIb3DQEBAQICCAAwDQYHKoZIzj0CAQICAQAwDgYIKyQD
AwIFAgECAgEAMA4GCCskAwMCBQQEAgIBADAOBggrJAMDAgUEBQICAQAwDgYIKyQDAwIFBAYC
AgEAo4IB/zCCAfswCwYJYIZIAWUDBAIBMAsGCWCGSAFlAwQCAjALBglghkgBZQMEAgMwCwYJ
YIZIAWUDBAIGMAsGCWCGSAFlAwQCCDALBglghkgBZQMEAgkwCwYJYIZIAWUDBAIKMA8GCWCG
SAFlAwQDAgICCAAwDwYJYIZIAWUDBAMDAgIIADAPBglghkgBZQMEAwQCAggAMA8GCWCGSAFl
AwQDBgICCAAwDwYJYIZIAWUDBAMHAgIIADAPBglghkgBZQMEAwgCAggAMA4GCCqGSM49BAMC
AgIBADAOBggqhkjOPQQDAwICAQAwDgYIKoZIzj0EAwQCAgEAMA8GCWCGSAFlAwQDCgICAQAw
DwYJYIZIAWUDBAMLAgIBADAPBglghkgBZQMEAwwCAgEAMA8GCSqGSIb3DQEBCwICCAAwDwYJ
KoZIhvcNAQEMAgIIADAPBgkqhkiG9w0BAQ0CAggAMA8GCWCGSAFlAwQDDgICCAAwDwYJYIZI
AWUDBAMPAgIIADAPBglghkgBZQMEAxACAggAMA8GCSqGSIb3DQEBCgICCAAwDwYJKoZIhvcN
AQEBAgIIADANBgcqhkjOPQIBAgIBADAOBggrJAMDAgUCAQICAQAwDgYIKyQDAwIFBAQCAgEA
MA4GCCskAwMCBQQFAgIBADAOBggrJAMDAgUEBgICAQCkggH/MIIB+zALBglghkgBZQMEAgEw
CwYJYIZIAWUDBAICMAsGCWCGSAFlAwQCAzALBglghkgBZQMEAgYwCwYJYIZIAWUDBAIIMAsG
CWCGSAFlAwQCCTALBglghkgBZQMEAgowDwYJYIZIAWUDBAMCAgIIADAPBglghkgBZQMEAwMC
AggAMA8GCWCGSAFlAwQDBAICCAAwDwYJYIZIAWUDBAMGAgIIADAPBglghkgBZQMEAwcCAggA
MA8GCWCGSAFlAwQDCAICCAAwDgYIKoZIzj0EAwICAgEAMA4GCCqGSM49BAMDAgIBADAOBggq
hkjOPQQDBAICAQAwDwYJYIZIAWUDBAMKAgIBADAPBglghkgBZQMEAwsCAgEAMA8GCWCGSAFl
AwQDDAICAQAwDwYJKoZIhvcNAQELAgIIADAPBgkqhkiG9w0BAQwCAggAMA8GCSqGSIb3DQEB
DQICCAAwDwYJYIZIAWUDBAMOAgIIADAPBglghkgBZQMEAw8CAggAMA8GCWCGSAFlAwQDEAIC
CAAwDwYJKoZIhvcNAQEKAgIIADAPBgkqhkiG9w0BAQECAggAMA0GByqGSM49AgECAgEAMA4G
CCskAwMCBQIBAgIBADAOBggrJAMDAgUEBAICAQAwDgYIKyQDAwIFBAUCAgEAMA4GCCskAwMC
BQQGAgIBADAABCAaWobQZ1EuANtF/NjfuaBXR0nR0fKnGJ7Z8t/mregtvQ==
"""

    def setUp(self):
        self.asn1Spec = rfc3125.SignaturePolicy()

    def testDerCodec(self):
        substrate = pem.readBase64fromText(self.pem_text)
        asn1Object, rest = der_decoder(substrate, asn1Spec=self.asn1Spec)

        self.assertFalse(rest)
        self.assertTrue(asn1Object.prettyPrint())
        self.assertEqual(substrate, der_encoder(asn1Object))

        svp = asn1Object['signPolicyInfo']['signatureValidationPolicy']
        sr = svp['commonRules']['signerAndVeriferRules']['signerRules']
        msa = sr['mandatedSignedAttr']

        self.assertIn(rfc2985.pkcs_9_at_contentType, msa)
        self.assertIn(rfc2985.pkcs_9_at_messageDigest, msa)
        self.assertIn(rfc2985.pkcs_9_at_signingTime, msa)


suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])

if __name__ == '__main__':
    import sys

    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
