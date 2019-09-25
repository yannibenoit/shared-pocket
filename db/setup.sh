#!/bin/bash
MONGO_INITDB_DATABASE=${DB_NAME}
MONGODB_USERNAME=${DB_USER}
MONGODB_PASSWORD=${DB_PASSWORD}
echo "=> Creating an ${DB_NAME} user with a password in MongoDB"
mongo << EOF
use $MONGO_INITDB_DATABASE
db.createUser({user: '$MONGODB_USERNAME', pwd: '$MONGODB_PASSWORD', roles:[{role:'readWrite', db:'$MONGO_INITDB_DATABASE'}]})
EOF

mongo << EOF
use $MONGO_INITDB_DATABASE
db.createCollection('users')
EOF

mongo << EOF
use $MONGO_INITDB_DATABASE
db.createCollection('articles')
EOF
