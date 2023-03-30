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

allsize = ['8','16','22','24','32','36','42','64','72','96','128','256','512']
foreach size : allsize
    icon_dir = join_paths('hicolor', ('@0@x@1@').format(size,size), 'apps')
    install_data(
      join_paths(icon_dir, ('@0@.png').format(application_id)),
        install_dir: join_paths(get_option('datadir'), 'icons', icon_dir)
     )
endforeach
