from questionary import Validator, ValidationError

class NumberValidator(Validator):
    def validate(self, document):
        if len(document.text) == 0:
            raise ValidationError(
                message = "Please enter a value",
                cursor_position = len(document.text),
            )
        if not document.text.isnumeric():
            raise ValidationError(
                message = "Only numeric value is allowed",
                cursor_position = len(document.text),
            )

class ZipValidator(Validator):
    def validate(self, document):
        if len(document.text) == 0:
            raise ValidationError(
                message = "Please enter a value",
                cursor_position = len(document.text),
            )    
        if not document.text.isnumeric() or len(document.text) != 4:
            raise ValidationError(
                message = "Please enter a valid zipcode",
                cursor_position = len(document.text),
            )
        if int(document.text) < 1001 or int(document.text) > 9990:
            raise ValidationError(
                message = "This zipcode is not allowed"
            )

class YearBuildValidator(Validator):
    def validate(self,document):
        if len(document.text)== 0:
            raise ValidationError(
                message = "Indtast venligst kun numre",
                cursor_position = len(document.text),
            )
        if not document.text.isnumeric() or len(document.text) != 4:
            raise ValidationError(
                message = "Indtast venligst et byggeår på 4 cifre"
        )
        if int(document.text) <1400 or int(document.text) >2030:
            raise ValidationError(
                message = "Indtast venligst et gyldigt byggeår "
        )    
                