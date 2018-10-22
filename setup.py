# coding: utf-8

from cx_Freeze import setup, Executable

executables = [Executable('main.py',
                          targetName='parser.exe',
                          icon='123.ico'
                          )
               ]


#includes = ['time','sys','requests','re','bs4','httplib2','apiclient.discovery','oauth2client.service_account']



options = {
    'build_exe': {
        'include_msvcr': True
        #'includes': includes
    }
}

setup(name='Parser',
      version='0.0.2',
      description='Avito, Domofond, Cian',
      executables=executables,
      options=options)