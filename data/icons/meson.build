application_id = 'com.github.yucefsourani.Arfedorawelcome'

scalable_dir = join_paths('hicolor', 'scalable', 'apps')
install_data(
  join_paths(scalable_dir, ('@0@.svg').format(application_id)),
  install_dir: join_paths(get_option('datadir'), 'icons', scalable_dir)
)

symbolic_dir = join_paths('hicolor', 'symbolic', 'apps')
install_data(
  join_paths(symbolic_dir, ('@0@-symbolic.svg').format(application_id)),
  install_dir: join_paths(get_option('datadir'), 'icons', symbolic_dir)
)


install_data(
  join_paths('hicolor', 'com.github.yucefsourani.Arfedorawelcome.png'),
  install_dir: join_paths(get_option('datadir'), 'pixmaps')
)

allsize = ['128x128', '16x16', '192x192', '20x20', '22x22', '24x24', '256x256', '32x32', '36x36', '40x40', '42x42', '48x48', '512x512', '64x64', '72x72', '8x8', '96x96']
foreach size : allsize
    icon_dir = join_paths('hicolor', ('@0@x@1@').format(size,size), 'apps')
    install_data(
      join_paths(icon_dir, ('@0@.png').format(application_id)),
        install_dir: join_paths(get_option('datadir'), 'icons', icon_dir)
     )
endforeach
