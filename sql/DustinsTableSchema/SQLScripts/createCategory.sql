CREATE TABLE IF NOT EXISTS `mydb`.`category` (
  `categoryid` INT NOT NULL ,
  `categoryName` VARCHAR(100) NOT NULL ,
  `active` TINYINT(1) DEFAULT 1 ,
  `dateCreated` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ,
  `createdByUsername` VARCHAR(20) NULL ,
  PRIMARY KEY (`categoryid`) ,
  INDEX `createdByUsername_idx` (`createdByUsername` ASC),
  CONSTRAINT `createdByUsername`
    FOREIGN KEY (`createdByUsername`)
    REFERENCES `mydb`.`user` (`username`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB