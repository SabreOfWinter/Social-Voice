db.createUser(
    {
      user: "root",
      pwd: "mongoadmin",
      roles: [ "readWrite", "dbAdmin" ]
    }
 );