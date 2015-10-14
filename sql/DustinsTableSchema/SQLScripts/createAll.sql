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

CREATE TABLE IF NOT EXISTS `mydb`.`pillar` (
  `userid` INT NOT NULL COMMENT '',
  `supportUserId` INT NOT NULL COMMENT '',
  `dateCreated` DATE NULL COMMENT '',
  INDEX `supportUserId_idx` (`supportUserId` ASC, `userid` ASC)  COMMENT '',
  PRIMARY KEY (`supportUserId`, `userid`)  COMMENT '',
  CONSTRAINT `userid`
    FOREIGN KEY ()
    REFERENCES `mydb`.`user` ()
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `supportUserId`
    FOREIGN KEY (`supportUserId` , `userid`)
    REFERENCES `mydb`.`user` (`userid` , `userid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB

CREATE TABLE IF NOT EXISTS `mydb`.`category` (
  `categoryid` INT NOT NULL COMMENT '',
  `categoryName` VARCHAR(100) NOT NULL COMMENT '',
  `active` TINYINT(1) NULL COMMENT '',
  `dateCreated` DATE NULL COMMENT '',
  `createdById` INT NULL COMMENT '',
  PRIMARY KEY (`categoryid`)  COMMENT '',
  INDEX `createdById_idx` (`createdById` ASC)  COMMENT '',
  CONSTRAINT `createdById`
    FOREIGN KEY (`createdById`)
    REFERENCES `mydb`.`user` (`userid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB

CREATE TABLE IF NOT EXISTS `mydb`.`userCategoryPreference` (
  `userid` INT NOT NULL COMMENT '',
  `categoryid` INT NOT NULL COMMENT '',
  PRIMARY KEY (`userid`, `categoryid`)  COMMENT '',
  INDEX `categoryid_idx` (`categoryid` ASC)  COMMENT '',
  CONSTRAINT `userid`
    FOREIGN KEY (`userid`)
    REFERENCES `mydb`.`user` (`userid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `categoryid`
    FOREIGN KEY (`categoryid`)
    REFERENCES `mydb`.`category` (`categoryid`)
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

CREATE TABLE IF NOT EXISTS `mydb`.`categoryOnPost` (
  `postid` INT NOT NULL COMMENT '',
  `categoryid` INT NOT NULL COMMENT '',
  PRIMARY KEY (`postid`, `categoryid`)  COMMENT '',
  INDEX `categoryid_idx` (`categoryid` ASC)  COMMENT '',
  CONSTRAINT `categoryid`
    FOREIGN KEY (`categoryid`)
    REFERENCES `mydb`.`category` (`categoryid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `postid`
    FOREIGN KEY (`postid`)
    REFERENCES `mydb`.`post` (`postid`)
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

CREATE TABLE IF NOT EXISTS `mydb`.`comment` (
  `commentid` INT NOT NULL AUTO_INCREMENT COMMENT '',
  `postid` INT NOT NULL COMMENT '',
  `parentCommentid` INT NULL COMMENT '',
  `userid` INT NULL COMMENT '',
  `deletedByDate` DATE NULL COMMENT '',
  `deletedByUserId` INT NULL COMMENT '',
  `active` INT NULL COMMENT '',
  `dateCreated` DATE NULL COMMENT '',
  `comment` MEDIUMTEXT NULL COMMENT '',
  PRIMARY KEY (`commentid`)  COMMENT '',
  INDEX `deletedByUserId_idx` (`deletedByUserId` ASC)  COMMENT '',
  INDEX `postid_idx` (`postid` ASC)  COMMENT '',
  INDEX `userid_idx` (`userid` ASC)  COMMENT '',
  CONSTRAINT `parentCommentid`
    FOREIGN KEY (`commentid`)
    REFERENCES `mydb`.`comment` (`commentid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `userid`
    FOREIGN KEY (`userid`)
    REFERENCES `mydb`.`user` (`userid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `postid`
    FOREIGN KEY (`postid`)
    REFERENCES `mydb`.`post` (`postid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `deletedByUserId`
    FOREIGN KEY (`deletedByUserId`)
    REFERENCES `mydb`.`user` (`userid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
COMMENT = '		'

CREATE TABLE IF NOT EXISTS `mydb`.`userCommentProperty` (
  `userid` INT NOT NULL COMMENT '',
  `commentid` INT NOT NULL COMMENT '',
  `hidden` TINYINT(1) NULL COMMENT '',
  `liked` INT NULL COMMENT '',
  `reported` INT NULL COMMENT '',
  PRIMARY KEY (`userid`, `commentid`)  COMMENT '',
  INDEX `commentid_idx` (`commentid` ASC)  COMMENT '',
  CONSTRAINT `userid`
    FOREIGN KEY (`userid`)
    REFERENCES `mydb`.`user` (`userid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `commentid`
    FOREIGN KEY (`commentid`)
    REFERENCES `mydb`.`comment` (`commentid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB