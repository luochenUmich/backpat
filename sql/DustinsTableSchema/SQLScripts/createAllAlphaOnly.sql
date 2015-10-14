CREATE TABLE IF NOT EXISTS `mydb`.`user` (
  `userid` INT NOT NULL AUTO_INCREMENT COMMENT '',
  `email` VARCHAR(255) NOT NULL COMMENT '',
  `password` VARCHAR(45) NOT NULL COMMENT '',
  `username` VARCHAR(45) NULL COMMENT '',
  `active` TINYINT(1) NULL COMMENT '',
  PRIMARY KEY (`userid`)  COMMENT '',
  UNIQUE INDEX `username_UNIQUE` (`username` ASC)  COMMENT '',
  UNIQUE INDEX `email_UNIQUE` (`email` ASC)  COMMENT '')
ENGINE = InnoDB

CREATE TABLE IF NOT EXISTS `mydb`.`permission` (
  `userid` INT NOT NULL COMMENT '',
  `adminLevel` INT ZEROFILL NULL COMMENT '',
  PRIMARY KEY (`userid`)  COMMENT '',
  CONSTRAINT `userid`
    FOREIGN KEY (`userid`)
    REFERENCES `mydb`.`user` (`userid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB

CREATE TABLE IF NOT EXISTS `mydb`.`post` (
  `postid` INT NOT NULL AUTO_INCREMENT COMMENT '',
  `userid` INT NULL COMMENT '',
  `summary` VARCHAR(100) NULL COMMENT '',
  `description` MEDIUMTEXT NULL COMMENT '',
  `dateCreated` DATE NULL COMMENT '',
  `dateLastModified` DATE NULL COMMENT '',
  `active` TINYINT(1) NULL COMMENT '',
  PRIMARY KEY (`postid`)  COMMENT '',
  INDEX `userid_idx` (`userid` ASC)  COMMENT '',
  CONSTRAINT `userid`
    FOREIGN KEY (`userid`)
    REFERENCES `mydb`.`user` (`userid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB

CREATE TABLE IF NOT EXISTS `mydb`.`userPostProperty` (
  `userid` INT NOT NULL COMMENT '',
  `postid` INT NOT NULL COMMENT '',
  `liked` TINYINT(1) ZEROFILL NULL COMMENT '',
  `reported` TINYINT(1) ZEROFILL NULL COMMENT '',
  `timesSeen` INT ZEROFILL NULL COMMENT '',
  `hidden` TINYINT(1) ZEROFILL NULL COMMENT '',
  PRIMARY KEY (`userid`, `postid`)  COMMENT '',
  CONSTRAINT `userid`
    FOREIGN KEY (`userid`)
    REFERENCES `mydb`.`user` (`userid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `postid`
    FOREIGN KEY (`postid`)
    REFERENCES `mydb`.`post` (`postid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB