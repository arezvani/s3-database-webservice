# s3-database-webservice
Call API, Upload image to s3 in stream way, insert data to databse, login and get data with webservice

## Introduction

### API
First we get data from Get data from API.

```json
{"results":[{"gender":"male","name":{"title":"Mr","first":"سام","last":"نجاتی"},"location":{"street":{"number":5093,"name":"شهید آرش مهر"},"city":"اراک","state":"سیستان و بلوچستان","country":"Iran","postcode":85524,"coordinates":{"latitude":"14.8221","longitude":"-66.8774"},"timezone":{"offset":"-5:00","description":"Eastern Time (US & Canada), Bogota, Lima"}},"email":"sm.njty@example.com","login":{"uuid":"6a38607d-4498-492f-93ca-369819d90283","username":"smallostrich271","password":"circus","salt":"prLILh0M","md5":"dfafa1f6203c7589964d8e39d1dc4beb","sha1":"21996887ab6481a45e9694e6bc9281bf93fc214f","sha256":"c26345cd8199200d0016a03de687a7428df7d6c348a0ce5ec1260b4b3b1ead8b"},"dob":{"date":"1967-09-05T20:28:25.316Z","age":56},"registered":{"date":"2013-11-30T11:00:16.765Z","age":9},"phone":"006-85015204","cell":"0902-142-6178","id":{"name":"","value":null},"picture":{"large":"https://randomuser.me/api/portraits/men/50.jpg","medium":"https://randomuser.me/api/portraits/med/men/50.jpg","thumbnail":"https://randomuser.me/api/portraits/thumb/men/50.jpg"},"nat":"IR"}],"info":{"seed":"834d64feb14ac0ec","results":1,"page":1,"version":"1.4"}}
```

### Upload to s3

Then we use picture.large of json response and upload this image to s3 in stream way that not open and download this file.

### Insert record to DB
After that we insert a record for this person with json response to database.

For this job we have these tables in database:

- persons_auth
  
  ```sql
  CREATE TABLE public.persons_auth (
	  username varchar NOT NULL,
	  "password" varchar NULL,
	  email varchar NOT NULL,
	  uuid varchar NOT NULL,
	  CONSTRAINT persons_auth_pk PRIMARY KEY (uuid)
  );
  ```

- persons_information
  
  ```sql
  CREATE TABLE public.persons_information (
	  uuid varchar NOT NULL,
	  first_name varchar NULL,
	  last_name varchar NULL,
	  gender varchar NULL,
	  "location" jsonb NULL,
	  picture varchar NULL,
	  phone varchar NULL,
	  age varchar NULL,
	  register_date timestamp NULL,
	  email varchar NULL,
	  CONSTRAINT persons_information_pk PRIMARY KEY (uuid)
  );


  -- public.persons_information foreign keys

  ALTER TABLE public.persons_information ADD CONSTRAINT persons_information_fk FOREIGN KEY (uuid) REFERENCES public.persons_auth(uuid) ON DELETE CASCADE ON UPDATE CASCADE;
  ```

![image](https://github.com/arezvani/s3-database-webservice/assets/20871524/2cb4e6f1-f6ed-4c96-a4dc-3537532d96e6)

### Webservice
We use webservice that if user successfully login, can see own information.

Also this webservice have session that user will be login untill log out.

For storing session these options are available:

| Options                  | DESCRIPTION                                                                                                                                             |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SESSION_TYPE             | Specifies which type of session interface to use. Built-in session types: null(default), redis, memcached, filesystem, mongodb, sqlalchemy              |
| SESSION_PERMANENT        | Whether to use a permanent session (default: True)                                                                                                      |
| SESSION_USE_SIGNER       | Whether to sign the session cookie sid or not, if set to True, you have to set flask.Flask.secret_key. (default: False)                                 |
| SESSION_KEY_PREFIX       | A prefix that is added before all session keys. This makes it possible to use the same backend storage server for different apps. (default: “session:”) |
| SESSION_REDIS            | An open Redis session to store session data in.                                                                                                         |
| SESSION_MEMCACHED        | A memcache.Client instance, default connect to 127.0.0.1:11211                                                                                          |
| SESSION_FILE_DIR         | The directory where session files are stored. Default to use flask_session directory under current working directory.                                   |
| SESSION_FILE_MODE        | The file mode wanted for the session files, default 0600                                                                                                |
| SESSION_MONGODB          | A pymongo.MongoClient instance, default connect to 127.0.0.1:27017                                                                                      |
| SESSION_MONGODB_DB       | The MongoDB database you want to use, default “flask_session”                                                                                           |
| SESSION_MONGODB_COLLECT  | The MongoDB collection you want to use, default “sessions”                                                                                              |
| SESSION_SQLALCHEMY       | A flask.ext.sqlalchemy.SQLAlchemy instance whose database connection URI is configured using the SQLALCHEMY_DATABASE_URI parameter                      |
| SESSION_SQLALCHEMY_TABLE | The name of the SQL table you want to use, default “sessions”                                                                                           |

## How to run

### Files:

- `config.py`: configs for api url, s3 and db

- `upload_s3_db.py`: upload images to s3

- `flask`: Webservice

- `requirement.txt`: a file that contains a list of packages or libraries needed to work on a project that can all be installed with the file


### Get data and Upload to S3

### Run Webservice

## to do

* Django webservice
* Fast API webservice
* Multi-Thread and Multi Chunk upload for bigger files

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.
