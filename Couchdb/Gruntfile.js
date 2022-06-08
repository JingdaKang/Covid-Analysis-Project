module.exports = function (grunt) {
    grunt
      .initConfig({
        "couch-compile": {
          dbs: {
            files: {
              "/tmp/vax_geo.json": "Vaccine_old",
              "/tmp/covid_vaccine.json": "Vaccine_new"
            }
          }
        },
        "couch-push": {
          options: {
            user: process.env.user,
            pass: process.env.pass
          },
          twitter: {
              files: {
                "http://admin:admin@localhost:5984/vax_geo": "/tmp/vax_geo.json",
                "http://admin:admin@localhost:5984/covid_vaccine": "/tmp/covid_vaccine.json"
              }
          }
        }
      });
  
    
    grunt.loadNpmTasks("grunt-couch");
  };
  