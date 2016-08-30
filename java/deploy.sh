#!/bin/bash

./mvnw clean package
scp -i ../tsubasa_id_rsa target/isuxi-0.0.1-SNAPSHOT.jar tsubasa@104.199.198.11:/home/isucon/webapp/java/target/isuxi-0.0.1-SNAPSHOT.jar
