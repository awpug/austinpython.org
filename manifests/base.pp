group {
    "puppet":
        ensure => present;
}

Package {
    # bug in puppet? Why am I having to force this?
    require => Exec["update_packages"]
}

package {
    "python-dev":
        ensure => present;
    "build-essential":
        ensure => present;
    "python-setuptools":
        ensure => present;
    "python-pip":
        ensure => present;
    "git-core":
        ensure => present;
    "apache2":
        ensure => present;
    "libapache2-mod-wsgi":
        ensure => present;
}

file {

    "apache2-default":
        path => "/etc/apache2/sites-available/default",
        require => Package["apache2"],
        notify => Service["apache2"],
        content => "Alias /static/ /home/austinpython/live/austinpython/ap/static/
        # hack, doesn't include other app static files
        <Directory /home/austinpython/live/austinpython/ap/static>
        Order deny,allow
        Allow from all
        </Directory>

        WSGIScriptAlias / /home/austinpython/live/austinpython/wsgi.py

        <Directory /home/austinpython>
        Order deny,allow
        Allow from all
        </Directory>";
}

service {
    "apache2":
        hasrestart => true,
        ensure => running;
}


exec {

    "install_modules":
        path => ["/bin", "/usr/local/bin", "/usr/bin"],
        command => "pip install -r /home/austinpython/live/requirements.txt",
        require => Package["python-pip", "git-core", "python-dev"];

    "update_packages":
        path => ["/bin", "/usr/local/bin", "/usr/bin"],
        command => "apt-get update";
}
