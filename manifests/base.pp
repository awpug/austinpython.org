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
    "virtualenvwrapper":
        require => Package["python-pip"],
        provider => pip,
        ensure => present;
}



exec {

    "install_vm":
        path => ["/bin", "/usr/local/bin", "/usr/bin"],
        command => "source /usr/local/bin/virtualenvwrapper.sh;mkvirtualenv austinpython.org",
        user => "vagrant",
        require => Package["python-pip", "python-setuptools", "python-dev", "virtualenvwrapper"],
        unless => "/usr/bin/test -d /home/vagrant/.virtualenvs/austinpython.org";

    "install_modules":
        path => ["/bin", "/usr/local/bin", "/usr/bin"],
        command => "source /usr/local/bin/virtualenvwrapper.sh;workon austinpython.org;pip install -r /vagrant/requirements.txt",
        user => "vagrant",
        require => Exec["install_vm"];

}
