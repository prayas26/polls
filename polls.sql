CREATE TABLE `polling` (
  `un_id` int(5) NOT NULL,
  `question` varchar(100) NOT NULL,
  `op1` varchar(20) NOT NULL,
  `op2` varchar(20) NOT NULL,
  `op1count` int(5) NOT NULL,
  `op2count` int(5) NOT NULL,
  `userid` varchar(20) NOT NULL
)


CREATE TABLE `users` (
  `userid` varchar(20) NOT NULL,
  `user_pass` varchar(200) NOT NULL
)

ALTER TABLE `polling`
  ADD PRIMARY KEY (`un_id`);

ALTER TABLE `users`
  ADD PRIMARY KEY (`userid`);

ALTER TABLE `polling`
  MODIFY `un_id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
