application_id = 'xyz.slothlife.diveboard'

scalable_dir = join_paths('hicolor', 'scalable', 'apps')
install_data(
  join_paths(scalable_dir, ('@0@.png').format(application_id)),
  #install_dir: join_paths(get_option('datadir'), scalable_dir)
  install_dir: '/usr/share/icons/hicolor/48x48/apps/'
)

symbolic_dir = join_paths('hicolor', 'symbolic', 'apps')
install_data(
  join_paths(symbolic_dir, ('@0@-symbolic.svg').format(application_id)),
  install_dir: join_paths(get_option('datadir'), symbolic_dir)
)
