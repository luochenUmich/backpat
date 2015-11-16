CREATE TABLE IF NOT EXISTS `mydb`.`userCategoryPreference` (
  `username` VARCHAR(20) NOT NULL COMMENT '',
  `categoryid` INT NOT NULL COMMENT '',
  PRIMARY KEY (`username`, `categoryid`)  COMMENT '',
  INDEX `categoryid_idx` (`categoryid` ASC)  COMMENT '',
  CONSTRAINT `categoryid`
    FOREIGN KEY (`categoryid`)
    REFERENCES `mydb`.`category` (`categoryid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `username`
    FOREIGN KEY (`username`)
    REFERENCES `mydb`.`user` (`username`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB