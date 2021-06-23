subdir('ui')

moduledir = join_paths(pkgdatadir, 'diveboard')

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'diveboard.in',
  output: 'diveboard',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

diveboard_sources = [
  '__init__.py',
  'main.py',
  'define.py',
  'settings.py',
  'preferences.py',
  'dive.py',
  'dive_trip.py',
  'logbook.py',
  'statistics.py',
  'wallet.py',
  'utils.py',
  'login.py',
  'api_manager.py',
  'spot.py',
  'map.py',
  'picture.py',
  'database_manager.py',
  'window.py',
]

install_data(diveboard_sources, install_dir: moduledir)



