# Item Catalog

This project is about catalog of items where users can view items across categories, browse through the latest items and view the details of each item. Upon logging in, user will have privileges to add, edit and delete the items.

### Set up and Project execution

1. Download [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)  to install virtual machine. 
2. Unzip this project and place the ItemCatalog folder in your Vagrant directory
3. Use the below commands to bring the virtual machine online and to login respectively:
	`vagrant up` - which will take several minutes and returns the terminal prompt on success
	`vagrant ssh` - used for logging in to VM
4. Change directory to /vagrant/ItemCatalog
	`$ cd /vagrant/ItemCatalog`
5. Initialize the database
	`$ python database_setup.py`
6. Populate the database tables with few initial values
	`$ python db_rows.py`
7. Launch the ItemCatalog application - This will display the logs on console and runs the    application
	`$ python catalog_items.py`
8. Open the browser and go to [http://localhost:5000/](http://localhost:5000/)

### JSON endpoints

#### Returns JSON of all items
`/catalog.json`
#### Returns JSON of items in specific category
`/catalog/<string:category_name>/items.json`
#### Returns JSON of an item
`/catalog/<string:category_name>/<string:item_name>/detail.json`