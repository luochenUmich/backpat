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