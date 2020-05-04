CREATE DATABASE hoplon;

CREATE TABLE game_server_logs (
  userId int NOT NULL,
  action varchar(50) NOT NULL,
  actionDate date NOT NULL,
  actionTime time NOT NULL
);