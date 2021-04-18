application_id = 'xyz.slothlife.diveboard'

scalable_dir = join_paths('hicolor', 'scalable', 'apps')
target_dir = join_paths('icons', 'hicolor', '48x48', 'apps')
install_data(
  join_paths(scalable_dir, ('@0@.png').format(application_id)),
  install_dir: join_paths(get_option('datadir'), target_dir)
)

symbolic_dir = join_paths('hicolor', 'symbolic', 'apps')
install_data(
  join_paths(symbolic_dir, ('@0@-symbolic.svg').format(application_id)),
  install_dir: join_paths(get_option('datadir'), symbolic_dir)
)
