Vagrant::Config.run do |config|

  # Set up basic Lucid 64bit server
  config.vm.box = "lucid64"
  config.vm.box_url = "http://files.vagrantup.com/lucid64.box"

  # Forward HTTP requests to 8080
  config.vm.forward_port "django", 8000, 8000 # for manage.py runserver
  config.vm.forward_port "http", 80, 8080 # for Apache, static, etc.
  # config.vm.share_folder "v-data", "/vagrant_data", "../data"

  # Puppet configuration
  config.vm.provision :puppet do |puppet|
    puppet.manifests_path = "manifests"
    puppet.manifest_file  = "base.pp"
  end

end
