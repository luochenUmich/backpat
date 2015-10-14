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