pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), 'arfedora_welcome')
moduledir = join_paths(pkgdatadir, 'arfedora_welcome')
gnome = import('gnome')

gnome.compile_resources('arfedora-welcome',
  'arfedora-welcome.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'arfedora-welcome.in',
  output: 'arfedora-welcome',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

arfedora_welcome_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'about.py',
  'main_page.py',
  'utils.py',
  'classesplugin.py',
  'gui_widgets.py',
  'output_page.py'
]

install_data(arfedora_welcome_sources, install_dir: moduledir)

install_subdir(
      'plugins',
      install_dir : pkgdatadir
)

install_subdir(
      'images',
      install_dir : pkgdatadir
)
