from backend.app.parser import Parser


forms = {
    "name": "NYPD Arrest Warrant",
    "warrants": ["warrant1", "warrant2"]
}


def analyze(forms: dict) -> Parser:
    return Parser(
        name=forms["name"],
        warrants=forms["warrant 1"],
        description="YOU ARE HEREBY COMMANDED to arrest JOHN DOE and bring him before the nearest magistrate to answer to the charge of theft of property. This warrant is issued upon probable cause that JOHN DOE has committed the offense of theft of property, in violation of the laws of this jurisdiction. You are authorized to use reasonable force if necessary to effectuate this arrest. This warrant is valid for a period of 30 days from the date of issuance."
    )

def analyze(forms: dict) -> Parser:
    return Parser(
        name=forms["name"],
        warrants=forms["warrant 2"],
        description="YOU ARE HEREBY COMMANDED to arrest JANEDOE and bring her before the nearest magistrate to answer to the charge of theft of property. This warrant is issued upon probable cause that JOHN DOE has committed the offense of theft of property, in violation of the laws of this jurisdiction. You are authorized to use reasonable force if necessary to effectuate this arrest. This warrant is valid for a period of 30 days from the date of issuance."
    )
