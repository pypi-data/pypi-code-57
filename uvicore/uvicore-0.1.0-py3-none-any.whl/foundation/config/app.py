
# App and providers DO run if APP or LIBRARY mode
# Because even if module, it is a dependency graph
# So provider IMPORTER needs to not import things twice

# Providers should be a recursive dependency graph

app = {
    'name': 'uvicore.foundation',
    'version': '1.0.1',

    # Application Service Providers
    'providers': [
        # mRcore Framework
        #'mrcore.support',
    ]
}


# Package config with used as a package library
package = {

}

# class Config:
#     test = 'test-class'
