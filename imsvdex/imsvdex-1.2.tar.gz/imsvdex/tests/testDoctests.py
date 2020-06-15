import doctest


# Zope testrunner finds this
def test_suite():
    return doctest.DocFileSuite(
        "../vdex.txt", optionflags=doctest.ELLIPSIS + doctest.REPORT_ONLY_FIRST_FAILURE
    )


# setuptools testrunner finds that
def additional_tests():
    return test_suite()
