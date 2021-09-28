CREATE TABLE `user` (
  `id` int unsigned PRIMARY KEY,
  `name` varchar(25),
  `login` varchar(50),
  `email` varchar(100),
  `pass` varchar(200)
);

CREATE TABLE `user_preferences` (
  `user_id` int unsigned,
  `gm` tinyint,
  `systems` varchar(300),
  `scenarios` varchar(400),
  `desc` varchar(400)
);

CREATE TABLE `user_relations` (
  `user_0` int unsigned,
  `user_1` int unsigned,
  `swipe_0` tinyint,
  `swipe_1` tinyint
);

CREATE TABLE `party` (
  `party_id` int unsigned PRIMARY KEY,
  `name` varchar(50),
  `desc` varchar(400)
);

CREATE TABLE `party_users` (
  `party_id` int unsigned,
  `user_id` int unsigned,
  `role` tinyint
);

CREATE TABLE `msg` (
  `msg_id` int unsigned PRIMARY KEY,
  `content` varchar(300),
  `by` int unsigned,
  `recipient_type` tinyint,
  `time` datetime
);

CREATE TABLE `msg_to` (
  `msg_id` int unsigned,
  `to` int unsigned
);

ALTER TABLE `user_preferences` ADD FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

ALTER TABLE `user_relations` ADD FOREIGN KEY (`user_0`) REFERENCES `user` (`id`);

ALTER TABLE `user_relations` ADD FOREIGN KEY (`user_1`) REFERENCES `user` (`id`);

ALTER TABLE `party_users` ADD FOREIGN KEY (`party_id`) REFERENCES `party` (`party_id`);

ALTER TABLE `party_users` ADD FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

ALTER TABLE `msg` ADD FOREIGN KEY (`by`) REFERENCES `user` (`id`);

ALTER TABLE `msg_to` ADD FOREIGN KEY (`msg_id`) REFERENCES `msg` (`msg_id`);

ALTER TABLE `msg_to` ADD FOREIGN KEY (`to`) REFERENCES `user` (`id`);
