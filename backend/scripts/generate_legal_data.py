import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, PageBreak

LEGAL_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "legal_data"))
os.makedirs(LEGAL_DATA_DIR, exist_ok=True)

def create_pdf(filename, title, act_meta, sections):
    filepath = os.path.join(LEGAL_DATA_DIR, filename)
    doc = SimpleDocTemplate(
        filepath,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0f2062'),
        spaceAfter=8,
        alignment=1
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#475569'),
        spaceAfter=15,
        alignment=1
    )
    sec_title_style = ParagraphStyle(
        'SecTitle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#1b3cb5'),
        spaceBefore=12,
        spaceAfter=4
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=8
    )
    
    story = []
    story.append(Paragraph(title, title_style))
    story.append(Paragraph(act_meta, subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2b52db'), spaceAfter=15))
    
    for sec_num, sec_heading, sec_content in sections:
        story.append(Paragraph(f"<b>{sec_num}: {sec_heading}</b>", sec_title_style))
        story.append(Paragraph(sec_content, body_style))
        story.append(Spacer(1, 4))
        
    doc.build(story)
    print(f"Generated: {filepath}")

# 1. Bharatiya Nyaya Sanhita 2023 Excerpts
bns_sections = [
    ("Section 1", "Short title, extent and commencement", 
     "(1) This Act may be called the Bharatiya Nyaya Sanhita, 2023. (2) It extends to the whole of India. (3) It shall come into force on the 1st day of July, 2024."),
    ("Section 2", "Definitions", 
     "In this Sanhita, unless the context otherwise requires: (1) 'act' denotes as well a series of acts as a single act; (2) 'court' means a Judge who is empowered by law to act judicially; (14) 'injury' denotes any harm whatever illegally caused to any person, in body, mind, reputation or property; (26) 'public servant' denotes every person belonging to the defense forces, judges, officers of courts, and persons in the service or pay of the government."),
    ("Section 4", "Punishments", 
     "The punishments to which offenders are liable under the provisions of this Sanhita are: First—Death; Secondly—Imprisonment for life; Thirdly—Imprisonment, which is of two descriptions, namely: (1) Rigorous, that is with hard labour; (2) Simple; Fourthly—Forfeiture of property; Fifthly—Fine; Sixthly—Community service."),
    ("Section 103", "Punishment for Murder", 
     "(1) Whoever commits murder shall be punished with death or imprisonment for life, and shall also be liable to fine. (2) When a group of five or more persons acting in concert commits murder on the ground of race, caste or community, sex, place of birth, language, personal belief or any other similar ground, each member of such group shall be punished with death or with imprisonment for life, and shall also be liable to fine."),
    ("Section 115", "Voluntarily Causing Hurt", 
     "(1) Whoever does any act with the intention of thereby causing hurt to any person, or with the knowledge that he is likely thereby to cause hurt to any person, and does thereby cause hurt to any person, is said 'voluntarily to cause hurt'. (2) Whoever commits voluntarily causing hurt shall be punished with imprisonment of either description for a term which may extend to one year, or with fine which may extend to ten thousand rupees, or with both."),
    ("Section 189", "Unlawful Assembly", 
     "An assembly of five or more persons is designated an 'unlawful assembly', if the common object of the persons composing that assembly is: First—To overawe by criminal force the Central or State Government or public servant; Second—To resist the execution of any law; Third—To commit any mischief or criminal trespass; Fourth—By means of criminal force to enforce any right or supposed right. Whoever is a member of an unlawful assembly shall be punished with imprisonment up to six months, or fine, or both."),
    ("Section 303", "Theft", 
     "(1) Whoever, intending to take dishonestly any movable property out of the possession of any person without that person's consent, moves that property in order to such taking, is said to commit theft. (2) Whoever commits theft shall be punished with imprisonment of either description for a term which may extend to three years, or with fine, or with both, or with community service in case of first-time offense where the value of stolen property is less than five thousand rupees."),
    ("Section 318", "Cheating", 
     "(1) Whoever, by deceiving any person, fraudulently or dishonestly induces the person so deceived to deliver any property to any person, or to consent that any person shall retain any property, is said to 'cheat'. (2) Whoever cheats shall be punished with imprisonment of either description for a term which may extend to three years, or with fine, or with both. (4) Whoever cheats and thereby dishonestly induces the person deceived to deliver any property shall be punished with imprisonment up to seven years and fine."),
    ("Section 351", "Criminal Intimidation", 
     "(1) Whoever threatens another with any injury to his person, reputation or property, or to the person or reputation of any one in whom that person is interested, with intent to cause alarm to that person, commits criminal intimidation. (2) Whoever commits the offence of criminal intimidation shall be punished with imprisonment of either description for a term which may extend to two years, or with fine, or with both; and if the threat be to cause death or grievous hurt, with imprisonment up to seven years.")
]

# 2. Right to Information Act 2005
rti_sections = [
    ("Section 2", "Definitions", 
     "In this Act, unless the context otherwise requires: (f) 'information' means any material in any form, including records, documents, memos, e-mails, opinions, advices, press releases, circulars, orders, logbooks, contracts, reports, papers, samples, models, data material held in any electronic form; (h) 'public authority' means any authority or body or institution of self-government established or constituted by or under the Constitution, by any law made by Parliament or State Legislature, or by notification issued by the Government; (j) 'right to information' means the right to inspection of work, documents, records, taking notes, extracts or certified copies of documents."),
    ("Section 3", "Right to Information", 
     "Subject to the provisions of this Act, all citizens shall have the right to information."),
    ("Section 4", "Obligations of Public Authorities", 
     "(1) Every public authority shall maintain all its records duly catalogued and indexed in a manner and form which facilitates the right to information; and ensure that all records that are appropriate to be computerised are, within a reasonable time, computerised and connected through a network all over the country on different systems so that access to such records is facilitated. Every public authority shall publish within one hundred and twenty days of enactment the particulars of its organisation, functions, powers and duties of its officers and employees."),
    ("Section 6", "Request for Obtaining Information", 
     "(1) A person, who desires to obtain any information under this Act, shall make a request in writing or through electronic means in English or Hindi or in the official language of the area accompanying such fee as may be prescribed, to the Central Public Information Officer or State Public Information Officer. (2) An applicant making request for information shall not be required to give any reason for requesting the information or any other personal details except those that may be necessary for contacting him."),
    ("Section 7", "Disposal of Request", 
     "(1) The Central Public Information Officer or State Public Information Officer on receipt of a request under section 6 shall, as expeditiously as possible, and in any case within thirty days of the receipt of the request, either provide the information on payment of prescribed fee or reject the request: Provided that where the information sought concerns the life or liberty of a person, the same shall be provided within forty-eight hours of the receipt of the request. (2) If the decision is not provided within 30 days, it shall be deemed refusal."),
    ("Section 8", "Exemption from Disclosure of Information", 
     "(1) Notwithstanding anything contained in this Act, there shall be no obligation to give any citizen: (a) information, disclosure of which would prejudicially affect the sovereignty and integrity of India, security, strategic, scientific or economic interests of the State; (b) information expressly forbidden to be published by any court of law; (d) information including commercial confidence, trade secrets or intellectual property; (e) information available to a person in his fiduciary relationship, unless larger public interest warrants; (g) information which would endanger the life or physical safety of any person; (j) personal information which has no relationship to any public activity or interest."),
    ("Section 19", "Appeals", 
     "(1) Any person who does not receive a decision within the specified time under sub-section (1) or clause (a) of sub-section (3) of section 7, or is aggrieved by a decision of the Central Public Information Officer or State Public Information Officer, may within thirty days prefer an appeal to such officer who is senior in rank to the Central Public Information Officer or State Public Information Officer. (3) A second appeal against the decision shall lie within ninety days to the Central Information Commission or the State Information Commission."),
    ("Section 20", "Penalties", 
     "(1) Where the Central Information Commission or State Information Commission at the time of deciding any complaint or appeal is of the opinion that the Public Information Officer has without any reasonable cause refused to receive an application or has not furnished information within specified time or malafidely denied the request, it shall impose a penalty of two hundred and fifty rupees each day till application is received or information is furnished, so however, the total amount of such penalty shall not exceed twenty-five thousand rupees.")
]

# 3. Information Technology Act 2000
it_sections = [
    ("Section 2", "Definitions", 
     "In this Act, unless the context otherwise requires: (o) 'data' means a representation of information, knowledge, facts, concepts or instructions which are being prepared or have been prepared in a formalised manner; (r) 'electronic form' with reference to information, means any information generated, sent, received or stored in media, magnetic, optical, computer memory; (w) 'intermediary' with respect to any particular electronic records, means any person who on behalf of another person receives, stores or transmits that record or provides any service with respect to that record including telecom service providers, network service providers, internet service providers, web-hosting service providers, search engines, online payment sites, online-auction sites."),
    ("Section 43", "Penalty and Compensation for Damage to Computer System", 
     "If any person without permission of the owner or any other person who is incharge of a computer, computer system or computer network: (a) accesses or secures access to such computer; (b) downloads, copies or extracts any data, computer data base; (c) introduces or causes to be introduced any computer contaminant or computer virus; (d) damages or causes to be damaged any computer; (e) disrupts or causes disruption of any computer; he shall be liable to pay damages by way of compensation to the person so affected."),
    ("Section 43A", "Compensation for Failure to Protect Sensitive Personal Data", 
     "Where a body corporate, possessing, dealing or handling any sensitive personal data or information in a computer resource which it owns, controls or operates, is negligent in implementing and maintaining reasonable security practices and procedures and thereby causes wrongful loss or wrongful gain to any person, such body corporate shall be liable to pay damages by way of compensation to the person so affected."),
    ("Section 66", "Computer Related Offences", 
     "If any person, dishonestly or fraudulently, does any act referred to in section 43, he shall be punishable with imprisonment for a term which may extend to three years or with fine which may extend to five lakh rupees or with both."),
    ("Section 66C", "Punishment for Identity Theft", 
     "Whoever, fraudulently or dishonestly make use of the electronic signature, password or any other unique identification feature of any other person, shall be punished with imprisonment of either description for a term which may extend to three years and shall also be liable to fine which may extend to rupees one lakh."),
    ("Section 66D", "Punishment for Cheating by Personation by Using Computer Resource", 
     "Whoever, by means of any communication device or computer resource cheats by personating, shall be punished with imprisonment of either description for a term which may extend to three years and shall also be liable to fine which may extend to one lakh rupees."),
    ("Section 66E", "Punishment for Violation of Privacy", 
     "Whoever, intentionally or knowingly captures, publishes or transmits the image of a private area of any person without his or her consent, under circumstances violating the privacy of that person, shall be punished with imprisonment which may extend to three years or with fine not exceeding two lakh rupees, or with both."),
    ("Section 67", "Punishment for Publishing Obscene Information in Electronic Form", 
     "Whoever publishes or transmits or causes to be published or transmitted in the electronic form, any material which is lascivious or appeals to the prurient interest shall be punished on first conviction with imprisonment of either description for a term which may extend to three years and with fine which may extend to five lakh rupees and in the event of second or subsequent conviction with imprisonment up to five years and fine up to ten lakh rupees."),
    ("Section 79", "Exemption from Liability of Intermediary in Certain Cases", 
     "(1) An intermediary shall not be liable for any third party information, data, or communication link made available or hosted by him. (2) The provisions of sub-section (1) shall apply if: (a) the function of the intermediary is limited to providing access to a communication system; (b) the intermediary does not initiate transmission, select the receiver, or select or modify information; (c) the intermediary observes due diligence while discharging duties under this Act.")
]

# 4. Constitution of India - Fundamental Rights
const_sections = [
    ("Article 12", "Definition of State", 
     "In this Part, unless the context otherwise requires, 'the State' includes the Government and Parliament of India and the Government and the Legislature of each of the States and all local or other authorities within the territory of India or under the control of the Government of India."),
    ("Article 13", "Laws Inconsistent with Fundamental Rights", 
     "(1) All laws in force in the territory of India immediately before the commencement of this Constitution, in so far as they are inconsistent with the provisions of this Part, shall, to the extent of such inconsistency, be void. (2) The State shall not make any law which takes away or abridges the rights conferred by this Part and any law made in contravention of this clause shall, to the extent of the contravention, be void."),
    ("Article 14", "Equality Before Law", 
     "The State shall not deny to any person equality before the law or the equal protection of the laws within the territory of India. This article guarantees parity of treatment and prohibits arbitrary state action."),
    ("Article 19", "Protection of Certain Rights Regarding Freedom of Speech, etc.", 
     "(1) All citizens shall have the right: (a) to freedom of speech and expression; (b) to assemble peaceably and without arms; (c) to form associations or unions or co-operative societies; (d) to move freely throughout the territory of India; (e) to reside and settle in any part of the territory of India; and (g) to practise any profession, or to carry on any occupation, trade or business. (2) Nothing in sub-clause (a) shall affect operation of reasonable restrictions in the interests of sovereignty and integrity of India, security of State, friendly relations with foreign States, public order, decency or morality, contempt of court, defamation or incitement to an offence."),
    ("Article 20", "Protection in Respect of Conviction for Offences", 
     "(1) No person shall be convicted of any offence except for violation of a law in force at the time of the commission of the act (prohibition against ex-post facto laws). (2) No person shall be prosecuted and punished for the same offence more than once (protection against double jeopardy). (3) No person accused of any offence shall be compelled to be a witness against himself (right against self-incrimination)."),
    ("Article 21", "Protection of Life and Personal Liberty", 
     "No person shall be deprived of his life or personal liberty except according to procedure established by law. The Supreme Court of India in K.S. Puttaswamy v. Union of India (2017) affirmed that the Right to Privacy is an intrinsic part of the Right to Life and Personal Liberty under Article 21."),
    ("Article 21A", "Right to Education", 
     "The State shall provide free and compulsory education to all children of the age of six to fourteen years in such manner as the State may, by law, determine."),
    ("Article 22", "Protection Against Arrest and Detention", 
     "(1) No person who is arrested shall be detained in custody without being informed, as soon as may be, of the grounds for such arrest nor shall he be denied the right to consult, and to be defended by, a legal practitioner of his choice. (2) Every person who is arrested and detained in custody shall be produced before the nearest magistrate within a period of twenty-four hours of such arrest."),
    ("Article 32", "Remedies for Enforcement of Rights Conferred by this Part", 
     "(1) The right to move the Supreme Court by appropriate proceedings for the enforcement of the rights conferred by this Part is guaranteed. (2) The Supreme Court shall have power to issue directions or orders or writs, including writs in the nature of habeas corpus, mandamus, prohibition, quo warranto and certiorari, whichever may be appropriate, for the enforcement of any of the rights conferred by this Part.")
]

# 5. Digital Personal Data Protection Act 2023
dpdp_sections = [
    ("Section 4", "Grounds for Processing Digital Personal Data", 
     "(1) A person may process the personal data of an individual only in accordance with the provisions of this Act and for a lawful purpose: (a) for which the Data Principal has given her consent; or (b) for certain legitimate uses as specified in section 7."),
    ("Section 5", "Notice", 
     "(1) Every request made to a Data Principal for consent shall be accompanied or preceded by a notice given by the Data Fiduciary informing the Data Principal of: (i) the personal data sought to be collected and the purpose for processing; (ii) the manner in which she may exercise her rights under section 11 and make a complaint to the Board."),
    ("Section 6", "Consent", 
     "(1) The consent given by the Data Principal shall be free, specific, informed, unconditional and unambiguous with a clear affirmative action, and shall signify an agreement for the processing of her personal data for the specified purpose. (4) The Data Principal shall have the right to withdraw her consent at any time."),
    ("Section 9", "Processing of Personal Data of Children", 
     "(1) The Data Fiduciary shall, before processing any personal data of a child or a person with disability, obtain verifiable consent of the parent of such child or lawful guardian. (2) A Data Fiduciary shall not undertake tracking or behavioural monitoring of children or targeted advertising directed at children."),
    ("Section 11", "Right to Access Information about Personal Data", 
     "(1) The Data Principal shall have the right to obtain from the Data Fiduciary to whom she had previously given consent, a summary of personal data which is being processed and the processing activities undertaken, the identities of all other Data Fiduciaries and Data Processors with whom the personal data has been shared."),
    ("Section 12", "Right to Correction and Erasure of Personal Data", 
     "(1) A Data Principal shall have the right to correction, completion, updating and erasure of her personal data for the processing of which she had previously given consent. (2) A Data Fiduciary shall, upon receipt of a request, correct inaccurate or misleading personal data, complete incomplete personal data, and erase personal data that is no longer necessary for the purpose."),
    ("Section 13", "Right of Grievance Redressal", 
     "(1) A Data Principal shall have the right to have readily available means of grievance redressal provided by a Data Fiduciary or Consent Manager in respect of any act or omission."),
    ("Section 33", "Penalties for Breach", 
     "(1) If the Board determines on conclusion of an inquiry that non-compliance is significant, it may impose monetary penalties: Up to 250 crore rupees for failure to take reasonable security safeguards to prevent personal data breach under section 8(5); Up to 200 crore rupees for failure to notify the Board and affected Data Principals of personal data breach.")
]

if __name__ == "__main__":
    create_pdf("Bharatiya_Nyaya_Sanhita_2023.pdf", 
               "THE BHARATIYA NYAYA SANHITA, 2023", 
               "Act No. 45 of 2023 [Ministry of Law and Justice, Government of India]", 
               bns_sections)
    create_pdf("Right_to_Information_Act_2005.pdf", 
               "THE RIGHT TO INFORMATION ACT, 2005", 
               "Act No. 22 of 2005 [Ministry of Personnel, Public Grievances and Pensions]", 
               rti_sections)
    create_pdf("Information_Technology_Act_2000.pdf", 
               "THE INFORMATION TECHNOLOGY ACT, 2000", 
               "Act No. 21 of 2000 [Ministry of Electronics and Information Technology]", 
               it_sections)
    create_pdf("Constitution_of_India_Fundamental_Rights.pdf", 
               "THE CONSTITUTION OF INDIA - PART III: FUNDAMENTAL RIGHTS", 
               "Articles 12 to 35 [Ministry of Law and Justice, Government of India]", 
               const_sections)
    create_pdf("Digital_Personal_Data_Protection_Act_2023.pdf", 
               "THE DIGITAL PERSONAL DATA PROTECTION ACT, 2023", 
               "Act No. 22 of 2023 [Ministry of Electronics and Information Technology]", 
               dpdp_sections)
    print("All legal documents successfully created!")
