group {
    "puppet":
        ensure => present;
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
        content => "Alias /static/ /vagrant/austinpython/static/

        <Directory /vagrant/austinpython/static>
        Order deny,allow
        Allow from all
        </Directory>

        WSGIScriptAlias / /vagrant/austinpython/wsgi.py

        <Directory /vagrant/austinpython>
        Order deny,allow
        Allow from all
        </Directory>";
}

service {
    "apache2":
        ensure => running,
        subscribe => File["apache2-default"];
}


exec {

    "install_modules":
        path => ["/bin", "/usr/local/bin", "/usr/bin"],
        command => "pip install -r /vagrant/requirements.txt",
        require => Package["python-pip", "git-core", "python-dev"];

}
