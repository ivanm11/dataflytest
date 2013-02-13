REQUIREMENTS
============

Please, install latest versions of Fabric and PyYAML packages globally:

    sudo pip install Fabric --upgrade
    sudo pip install PyYAML --upgrade

If you're working with docs, install markdown2 package globally:

    sudo pip install markdown2 --upgrade

Copy config.example.yaml to your project folder and edit:

    cp datafly/config.example.yaml config.yaml

Install project based on type in config:

    cd datafly && fab starter_install

Run it:

    cd script && fab run