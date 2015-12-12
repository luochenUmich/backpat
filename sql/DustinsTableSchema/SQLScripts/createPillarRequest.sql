CREATE TABLE IF NOT EXISTS `mydb`.`pillar_request` (
  `username` VARCHAR(20) NOT NULL ,
  `supportUsername` VARCHAR(20) NOT NULL,
  `requestedByUsername` VARCHAR(20) NOT NULL,
  `dateCreated` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `dateAccepted` TIMESTAMP ,
  `reason` MEDIUMTEXT NULL, 
  `isTwoWay` bit DEFAULT 0,
  PRIMARY KEY (`supportUsername`, `username`))
ENGINE = InnoDB