project('diveboard',
          version: '0.1.0',
    meson_version: '>= 0.59.0',
  default_options: [ 'warning_level=2',
                   ],
)

i18n = import('i18n')

dependency('glib-2.0', version: '>= 2.74')
dependency('gio-2.0', version: '>= 2.74')
dependency('gobject-introspection-1.0', version: '>=1.74.0')
dependency('gtk4', version: '>=4.8.0')
dependency('libadwaita-1', version: '>=1.2.0')

subdir('data')
subdir('src')
subdir('po')

meson.add_install_script('build-aux/meson/postinstall.py')
