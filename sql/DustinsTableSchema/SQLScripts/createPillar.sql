CREATE TABLE IF NOT EXISTS `mydb`.`pillar` (
  `username` VARCHAR(20) NOT NULL ,
  `supportUsername` VARCHAR(20) NOT NULL,
  `dateCreated` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`supportUsername`, `username`))
ENGINE = InnoDB