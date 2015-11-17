CREATE TABLE IF NOT EXISTS `mydb`.`category` (
  `categoryid` INT NOT NULL COMMENT '',
  `categoryName` VARCHAR(100) NOT NULL COMMENT '',
  `active` TINYINT(1) DEFAULT 1 COMMENT '',
  `dateCreated` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '',
  `createdByUsername` VARCHAR(20) NULL COMMENT '',
  PRIMARY KEY (`categoryid`)  COMMENT '',
  INDEX `createdByUsername_idx` (`createdByUsername` ASC)  COMMENT '',
  CONSTRAINT `createdByUsername`
    FOREIGN KEY (`createdByUsername`)
    REFERENCES `mydb`.`user` (`username`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB