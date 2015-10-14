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