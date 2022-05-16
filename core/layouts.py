mainl = "module.exports = {obras}  \nup: (queryInterface, Sequelize) =>\n    queryInterface.createTable('{table_name}', " \
        "{obras}\n{definition}{cbras}), \n\tdown: (queryInterface, Sequelize) => queryInterface.dropTable('{" \
        "table_name}'), \n{cbras}; "

seedmainl = "module.exports = {obras}  \n\tup: (queryInterface, Sequelize) => {obras}\n\t    await " \
            "queryInterface.bulkInsert('{table_name}', \n\t\t\t[{definition}\n\t\t\t],\n\t{obras}{cbras},\n\t\t\t); \n\t{cbras}, \n\tdown: (" \
            "queryInterface, Sequelize) => queryInterface.bulkDelete('{table_name}', null, {obras}{cbras}), " \
            "\n{cbras}; "
